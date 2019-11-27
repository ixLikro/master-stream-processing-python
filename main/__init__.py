from streamz import Stream
from streamz.dataframe import DataFrame
from main.PhotovoltaicProducerSensor import *
from main.BatterySensor import *
from main.EnergyConsumptionSensor import *
from main.GUI import *
from main.BarometerSensor import *
from main.OutliersFilter import negativeFilter, rangeFilter
from main.TemperatureSensor import extractTemperature
from main.Util import debug

import math

#const
#Wolfenbüttel: 77 m üNn
WOLFENBUETELL_HIGHT=77
#source: https://rechneronline.de/barometer
TEMPERATURE_GRADIENT=0.0065/WOLFENBUETELL_HIGHT
# a placeholder for an invalid number
INVALID=-99999913701999999

messageCounter = 0

# define steams
temperatureSensor = Stream.from_tcp(54001).map(extractTemperature).map(rangeFilter)
barometer1Sensor = Stream.from_tcp(54002).map(barometerExtractor).map(rangeFilter)
barometer2Sensor = Stream.from_tcp(54003).map(barometerExtractor).map(rangeFilter)
barometer3Sensor = Stream.from_tcp(54004).map(barometerExtractor).map(rangeFilter)
livingAirSensor = Stream.from_tcp(54005)
bathroomAirSensor = Stream.from_tcp(54006)
bedroomAirSensor = Stream.from_tcp(54007)
kitchenAirSensor = Stream.from_tcp(54009)
livingWindowSensor = Stream.from_tcp(54010)
bathWindowSensor = Stream.from_tcp(54011)
bedWindowSensor = Stream.from_tcp(54012)
kitchenWindowSensor = Stream.from_tcp(54013)
energyConsumptionSensor = Stream.from_tcp(54014).map(energyConsumptionExtractor).map(negativeFilter)
energyPhotovoltaicProduceSensor = Stream.from_tcp(54015).map(produceExtractor).map(negativeFilter)
energyBatterySensor = Stream.from_tcp(54016).map(batteryExtractor)

weatherForecastStream = None

def sumDay(bigTupel):
    #bigTupel[0] : consumption
    # bigTupel[1] : produce
    # bigTupel[2] : % charge
    sumCost=0
    sumProduce=0

    for measuring in bigTupel:
        if( measuring[0] is None or measuring[1] is None or measuring[2] is None):
            continue
        if(measuring[2] <= 0.5 and measuring[0] > measuring[1]):
            sumCost = sumCost + (((measuring[1] - measuring[0]) / 60) * 0.2686)
        if(measuring[2] >= 99.5 and measuring[0] < measuring[1]):
            sumProduce = sumProduce + (((measuring[0] - measuring[1]) / 60) * 0.1037)
    return (sumCost, sumProduce)

def energyPerDayAndMonth():
    dayCost = energyConsumptionSensor.zip(energyPhotovoltaicProduceSensor, energyBatterySensor)\
        .map(lambda x: (x[0][1], x[1][1], (x[2][1] / x[2][3]) * 100. ))\
        .partition(60 * 24)\
        .map(sumDay)\
        .map(lambda x: x[0] - x[1])\
        .map(lambda x: x / 100)

    monthCost = dayCost.partition(30).map(sum).sink(print)
    dayCost.sink(print)

    dayCost.start()
    monthCost.start()


def weatherForecast():
    global weatherForecastStream

    # source temperatureSensor (extracted and filtered)
    #     - get only the value
    #     - convert a None as value to INVALID
    onlyTemp = temperatureSensor\
        .map(lambda x: x[1])\
        .map(lambda x: x if x is not None else INVALID)

    # source barometer1Sensor (extracted and filtered)
    #     - combine it with barometer2Sensor and barometer3Sensor
    #     - get the average of the 3 values or None
    #     - convert a None as value to INVALID
    #     - combine it with the onlyTemp stream
    #     - use the formula from https://rechneronline.de/barometer/ to forecast the weather
    weatherForecastStream = barometer1Sensor\
        .zip(barometer2Sensor, barometer3Sensor)\
        .map(averagePressure)\
        .map(lambda x: x if x is not None else INVALID)\
        .zip(onlyTemp)\
        .map(lambda x: x[0] / math.pow(1- TEMPERATURE_GRADIENT * WOLFENBUETELL_HIGHT / (x[1] + (TEMPERATURE_GRADIENT * WOLFENBUETELL_HIGHT)), 0.03416 / TEMPERATURE_GRADIENT))\

    onlyTemp.start()

    weatherForecastStream.start()
    weatherForecastPrint = weatherForecastStream.sink(print)
    weatherForecastPrint.start()



def newMassage(x):
    global messageCounter
    messageCounter = messageCounter +1
    return messageCounter

def combineAll():
    global messageCounter
    all = temperatureSensor.union(energyBatterySensor,
                                  energyPhotovoltaicProduceSensor,
                                  energyConsumptionSensor,
                                  kitchenWindowSensor,
                                  bedWindowSensor,
                                  bathWindowSensor,
                                  livingWindowSensor,
                                  kitchenAirSensor,
                                  bedroomAirSensor,
                                  bathroomAirSensor,
                                  livingAirSensor,
                                  barometer3Sensor,
                                  barometer2Sensor,
                                  barometer1Sensor)\
        .map(newMassage)\
        .sink(print)\
        .start()

def infoEnergyAvailable():

    infoEnergy = energyBatterySensor \
        .map(lambda x: (x[1] / x[3]) * 100) \
        .combine_latest(weatherForecastStream) \
        .map(lambda x: True if x[0] >= 99.5 and x[1] < 990 else False) \
        .sink(print)

    infoEnergy.start()

if __name__ == "__main__":
    #combineAll()
    #energyPerDayAndMonth()
    weatherForecast()
    infoEnergyAvailable()
    initWindow()

