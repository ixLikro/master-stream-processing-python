from streamz import Stream
from main.PhotovoltaicProducerSensor import *
from main.BatterySensor import *
from main.EnergyConsumptionSensor import *
from main.GUI import *
from main.BarometerSensor import *
from main.AirSensor import airExtractor
from main.WindowSensor import windowExtraction
from main.OutliersFilter import negativeFilter, rangeFilter
from main.TemperatureSensor import extractTemperature, convertFromKToDegrees
from main.TimeSensor import simTimeExtractor
from main.Util import debug

import math

# const
# Wolfenbüttel: 77 m üNn
WOLFENBUETELL_HIGHT = 77
# source: https://rechneronline.de/barometer
TEMPERATURE_GRADIENT = 0.0065 / WOLFENBUETELL_HIGHT
# a placeholder for an invalid number
INVALID = -999999999999999

ENERGY_PRICE_IMPORT = 0.2686
ENERGY_PRICE_EXPORT = 0.1037

BAD_WEATHER_THRESHOLD = 990
BAD_AIR_THRESHOLD = 1200
GOOD_AIR_THRESHOLD = 550
COLD_THRESHOLD = 11

messageCounter = 0

# define steams
simulationTimeSensor = Stream.from_tcp(54000).map(simTimeExtractor)
temperatureSensor = Stream.from_tcp(54001).map(extractTemperature).map(convertFromKToDegrees).map(rangeFilter)
barometer1Sensor = Stream.from_tcp(54002).map(barometerExtractor).map(rangeFilter)
barometer2Sensor = Stream.from_tcp(54003).map(barometerExtractor).map(rangeFilter)
barometer3Sensor = Stream.from_tcp(54004).map(barometerExtractor).map(rangeFilter)
livingAirSensor = Stream.from_tcp(54005).map(airExtractor).map(rangeFilter)
bathroomAirSensor = Stream.from_tcp(54006).map(airExtractor).map(rangeFilter)
bedroomAirSensor = Stream.from_tcp(54007).map(airExtractor).map(rangeFilter)
kitchenAirSensor = Stream.from_tcp(54009).map(airExtractor).map(rangeFilter)
livingWindowSensor = Stream.from_tcp(54010).map(windowExtraction)
bathWindowSensor = Stream.from_tcp(54011).map(windowExtraction)
bedWindowSensor = Stream.from_tcp(54012).map(windowExtraction)
kitchenWindowSensor = Stream.from_tcp(54013).map(windowExtraction)
energyConsumptionSensor = Stream.from_tcp(54014).map(energyConsumptionExtractor).map(negativeFilter)
energyPhotovoltaicProduceSensor = Stream.from_tcp(54015).map(produceExtractor).map(negativeFilter)
energyBatterySensor = Stream.from_tcp(54016).map(batteryExtractor)

weatherForecastStream = None
onlyTemp = None


def sumDay(bigTupel):
    # bigTupel[0] : consumption
    # bigTupel[1] : produce
    # bigTupel[2] : % charge
    sumCost = 0
    sumProduce = 0

    for measuring in bigTupel:
        if (measuring[0] is None or measuring[1] is None or measuring[2] is None):
            continue
        if (measuring[2] <= 0.5 and measuring[0] > measuring[1]):
            sumCost = sumCost + (((measuring[1] - measuring[0]) / 60) * ENERGY_PRICE_IMPORT)
        if (measuring[2] >= 99.5 and measuring[0] < measuring[1]):
            sumProduce = sumProduce + (((measuring[0] - measuring[1]) / 60) * ENERGY_PRICE_EXPORT)
    return (sumCost, sumProduce)


def energyPerDayAndMonth():
    dayCost = energyConsumptionSensor.combine_latest(energyPhotovoltaicProduceSensor, energyBatterySensor) \
        .map(lambda x: (x[0][1], x[1][1], (x[2][1] / x[2][3]) * 100.)) \
        .partition(60 * 24) \
        .map(sumDay) \
        .map(lambda x: x[0] - x[1]) \
        .map(lambda x: x / 100)

    monthCost = dayCost.partition(30).map(sum).sink(updateEnergyCostMonth)
    dayCost.sink(updateEnergyCostDay)

    dayCost.start()
    monthCost.start()


def weatherForecast():
    global weatherForecastStream, onlyTemp

    # source temperatureSensor (extracted and filtered)
    #     - get only the value
    #     - convert a None as value to INVALID
    onlyTemp = temperatureSensor \
        .map(lambda x: x[1]) \
        .map(lambda x: x if x is not None else INVALID)

    # source barometer1Sensor (extracted and filtered)
    #     - combine it with barometer2Sensor and barometer3Sensor
    #     - get the average of the 3 values or None
    #     - convert a None as value to INVALID
    #     - combine it with the onlyTemp stream
    #     - use the formula from https://rechneronline.de/barometer/ to forecast the weather
    weatherForecastStream = barometer1Sensor \
        .combine_latest(barometer2Sensor, barometer3Sensor) \
        .map(averagePressure) \
        .map(lambda x: x if x is not None else INVALID) \
        .combine_latest(onlyTemp) \
        .map(lambda x: x[0] / math.pow(1 - TEMPERATURE_GRADIENT * WOLFENBUETELL_HIGHT / (
            (x[1] + 273.15) + (TEMPERATURE_GRADIENT * WOLFENBUETELL_HIGHT)), 0.03416 / TEMPERATURE_GRADIENT))

    onlyTemp.start()

    weatherForecastPrint = weatherForecastStream.sink(updatePressure)
    weatherForecastPrint.start()


def newMassage(x):
    global messageCounter
    messageCounter = messageCounter + 1
    return messageCounter


def infoEnergyAvailable():
    # source energyBatterySensor (extracted and filtered)
    #     - calculate charge in %
    #     - combine the stream with the weather forecast
    #     - return true if battery is full and weather seems to getting worse otherwise false
    #     - update warning on the dashboard
    infoEnergy = energyBatterySensor \
        .map(lambda x: (x[1] / x[3]) * 100) \
        .combine_latest(weatherForecastStream) \
        .map(lambda x: True if x[0] >= 99.5 and x[1] < BAD_WEATHER_THRESHOLD else False) \
        .sink(updateEnergyAvailableInfo)

    infoEnergy.start()


def buildBadAirWarning(windowStream, airQualityStream):
    # source airQualityStream (extracted and filtered)
    #     - replace None values with INVALID
    #     - return true if the air quality is bad otherwise false
    #     - combine with the window states stream
    #     - return True if the air is bad and all windows are closed
    return airQualityStream \
        .map(lambda x: x[1] if x[1] is not None else INVALID) \
        .map(lambda x: True if x > BAD_AIR_THRESHOLD else False) \
        .combine_latest(windowStream) \
        .map(lambda x: True if (x[0] and not x[1][2]) else False)


def initBadAirWarnings():
    livingWarning = buildBadAirWarning(livingWindowSensor, livingAirSensor) \
        .sink(updateLivingRoomOpenWindowWarning)
    livingWarning.start()

    kitchenWarning = buildBadAirWarning(kitchenWindowSensor, kitchenAirSensor) \
        .sink(updateKitchenOpenWindowWarning)
    kitchenWarning.start()

    bathroomWarning = buildBadAirWarning(bathWindowSensor, bathroomAirSensor) \
        .sink(updateBathRoomOpenWindowWarning)
    bathroomWarning.start()

    bedroomWarning = buildBadAirWarning(bedWindowSensor, bedroomAirSensor) \
        .sink(updateBedRoomOpenWindowWarning)
    bedroomWarning.start()


def buildCloseWindowWarning(windowStream, airSensor):
    # source airQualityStream (extracted and filtered)
    #     - replace None values with INVALID
    #     - return true if the air quality is good otherwise false
    #     - combine with the window states stream
    #     - return True if the air is good and at least one window is open
    #     - combine with the window state stream
    #     - return True if the air is good and at least one window is open and it is cold outside
    return airSensor \
        .map(lambda x: x[1] if x[1] is not None else INVALID) \
        .map(lambda x: True if 0 < x < GOOD_AIR_THRESHOLD else False) \
        .combine_latest(windowStream) \
        .map(lambda x: True if x[0] and x[1][2] else False) \
        .combine_latest(onlyTemp) \
        .map(lambda x: True if (x[0] and -50 < x[1] < COLD_THRESHOLD) else False)


def initCloseWindowWarning():
    livingCloseWarning = buildCloseWindowWarning(livingWindowSensor, livingAirSensor) \
        .sink(updateLivingRoomCloseWindowWarning)
    livingCloseWarning.start()

    kitchenCloseWarning = buildCloseWindowWarning(kitchenWindowSensor, kitchenAirSensor) \
        .sink(updateKitchenCloseWindowWarning)
    kitchenCloseWarning.start()

    bathroomCloseWarning = buildCloseWindowWarning(bathWindowSensor, bathroomAirSensor) \
        .sink(updateBathRoomCloseWindowWarning)
    bathroomCloseWarning.start()

    bedroomCloseWarning = buildCloseWindowWarning(bedWindowSensor, bedroomAirSensor) \
        .sink(updateBedRoomCloseWindowWarning)
    bedroomCloseWarning.start()


def convertToWeather(value):
    if value < 500:
        # invalid
        return ""
    if value < 980:
        return "High Precipitation"
    if value < 1000:
        return "Low Precipitation"
    if value < 1020:
        return "Cloudy"
    if value < 1040:
        return "Slightly Cloudy"
    return "clear Sky"


def startLiveOutput():
    timeToDashboard = simulationTimeSensor\
        .map(lambda x: x[1])\
        .sink(updateSimTim)\
        .start()
    tempToDashboard = onlyTemp\
        .sink(updateTemperature)\
        .start()
    foreCastToDashboard = weatherForecastStream\
        .map(convertToWeather)\
        .sink(updateWeatherForecast)\
        .start()

    energyConsumptionToDash = energyConsumptionSensor \
        .map(lambda x: x[1] if x[1] is not None else INVALID) \
        .sink(updateEnergyConsumption) \
        .start()
    energyProduceToDash = energyPhotovoltaicProduceSensor \
        .map(lambda x: x[1] if x[1] is not None else INVALID) \
        .sink(updateEnergyProduce) \
        .start()
    batteryToDashboard = energyBatterySensor \
        .map(lambda x: (x[1] / x[3]) * 100) \
        .sink(updateEnergyBattery) \
        .start()

    livingWindowToDashboard = livingWindowSensor\
        .map(lambda x: x[2])\
        .sink(updateLivingRoomWindowState)\
        .start()
    kitchenWindowToDashboard = kitchenWindowSensor\
        .map(lambda x: x[2])\
        .sink(updateKitchenWindowState)\
        .start()
    bathWindowToDashboard = bathWindowSensor\
        .map(lambda x: x[2])\
        .sink(updateBathRoomWindowState)\
        .start()
    bedWindowToDashboard = bedWindowSensor\
        .map(lambda x: x[2])\
        .sink(updateBedRoomWindowState)\
        .start()

    livingAirToDashboard = livingAirSensor \
        .map(lambda x: x[1]) \
        .map(lambda x: x if x is not None else INVALID) \
        .sink(updateLivingRoomAirQuality)\
        .start()
    kitchenAirToDashboard = kitchenAirSensor \
        .map(lambda x: x[1]) \
        .map(lambda x: x if x is not None else INVALID) \
        .sink(updateKitchenAirQuality)\
        .start()
    bathAirToDashboard = bathroomAirSensor \
        .map(lambda x: x[1]) \
        .map(lambda x: x if x is not None else INVALID) \
        .sink(updateBathRoomAirQuality)\
        .start()
    bedAirToDashboard = bedroomAirSensor \
        .map(lambda x: x[1]) \
        .map(lambda x: x if x is not None else INVALID) \
        .sink(updateBedRoomAirQuality)\
        .start()


if __name__ == "__main__":
    weatherForecast()
    energyPerDayAndMonth()
    infoEnergyAvailable()
    initBadAirWarnings()
    initCloseWindowWarning()
    startLiveOutput()
    initWindow()
