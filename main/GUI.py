from tkinter import *
import time

root = Tk()
simTime=StringVar()
temperatureVar = StringVar()
pressureVar = StringVar()
foreCast = StringVar()
bedroomVals = (StringVar(), StringVar(), StringVar(), StringVar())
livingRoomVals = (StringVar(), StringVar(), StringVar(), StringVar())
kitchenVals = (StringVar(), StringVar(), StringVar(), StringVar())
bathroomVals = (StringVar(), StringVar(), StringVar(), StringVar())
energyConsumptionVar=StringVar()
energyProduceVar=StringVar()
energyBattery=StringVar()
energyCostDay=StringVar()
energyCostMonth=StringVar()
energyAvailableInfo=StringVar()

SHOULD_CLOSE_WINDOW = "You should close the window!\n The Room has a good air quality and it is cold outside."
SHOULD_OPEN_WINDOW = "Bad air quality! You should open a window!"
ENERGY_AVAILABLE_INFO = "You hava a lot of Energy available and the Weather seems to getting worse. So better use your Energy now!"

rowCount = 0


def newRow():
    global rowCount
    rowCount = rowCount + 1


def initWindow():
    Label(root, text="    Dashboard    ", font=("Courier", 16)).grid(row=rowCount, columnspan=5)
    newRow()
    Label(root, text="  ").grid(column=0, row=rowCount)
    newRow()
    Label(root, text="  ").grid(column=0, row=rowCount)

    Label(root, text="Simulation Time: ").grid(column=0, row=rowCount, sticky=NE)
    Label(root, textvariable=simTime).grid(column=1, row=rowCount, sticky=NW)

    newRow()
    Label(root, text="  ").grid(column=0, row=rowCount)
    newRow()
    Label(root, text="  ").grid(column=0, row=rowCount)

    Label(root, text="Outside temperature: ").grid(column=0, row=rowCount, sticky=NE)
    Label(root, textvariable=temperatureVar).grid(column=1, row=rowCount, sticky=NW)
    newRow()
    Label(root, text="Barometric pressure (Ø): ").grid(column=0, row=rowCount, sticky=NE)
    Label(root, textvariable=pressureVar).grid(column=1, row=rowCount, sticky=NW)
    newRow()
    Label(root, text="Weather forecast: ").grid(column=0, row=rowCount, sticky=NE)
    Label(root, textvariable=foreCast).grid(column=1, row=rowCount, sticky=NW)

    newRow()
    Label(root, text="  ").grid(column=0, row=rowCount)
    newRow()
    Label(root, text="  ").grid(column=0, row=rowCount)

    Label(root, text="Enery consumption: ").grid(column=0, row=rowCount, sticky=NE)
    Label(root, textvariable=energyConsumptionVar).grid(column=1, row=rowCount, sticky=NW)
    newRow()
    Label(root, text="Photovoltaic produce: ").grid(column=0, row=rowCount, sticky=NE)
    Label(root, textvariable=energyProduceVar).grid(column=1, row=rowCount, sticky=NW)
    newRow()
    Label(root, text="Battery state: ").grid(column=0, row=rowCount, sticky=NE)
    Label(root, textvariable=energyBattery).grid(column=1, row=rowCount, sticky=NW)
    newRow()
    Label(root, text="Yesterday energy cost: ").grid(column=0, row=rowCount, sticky=NE)
    Label(root, textvariable=energyCostDay).grid(column=1, row=rowCount, sticky=NW)
    newRow()
    Label(root, text="Last month energy cost: ").grid(column=0, row=rowCount, sticky=NE)
    Label(root, textvariable=energyCostMonth).grid(column=1, row=rowCount, sticky=NW)
    newRow()
    Label(root, textvariable=energyAvailableInfo, foreground="green").grid(row=rowCount, columnspan=5)

    newRow()
    Label(root, text="  ").grid(column=0, row=rowCount)

    newRow()
    Label(root, text="Bedroom air quality: ").grid(column=0, row=rowCount, sticky=NE)
    Label(root, textvariable=bedroomVals[0]).grid(column=1, row=rowCount, sticky=NW)
    newRow()
    Label(root, text="Bedroom window state: ").grid(column=0, row=rowCount, sticky=NE)
    Label(root, textvariable=bedroomVals[1]).grid(column=1, row=rowCount, sticky=NW)
    newRow()
    Label(root, textvariable=bedroomVals[2], foreground="red").grid(row=rowCount, columnspan=5)
    newRow()
    Label(root, textvariable=bedroomVals[3], foreground="red").grid(row=rowCount, columnspan=5)

    newRow()
    Label(root, text="  ").grid(column=0, row=rowCount)
    newRow()
    Label(root, text="  ").grid(column=0, row=rowCount)

    newRow()
    Label(root, text="Kitchen air quality: ").grid(column=0, row=rowCount, sticky=NE)
    Label(root, textvariable=kitchenVals[0]).grid(column=1, row=rowCount, sticky=NW)
    newRow()
    Label(root, text="Kitchen window state: ").grid(column=0, row=rowCount, sticky=NE)
    Label(root, textvariable=kitchenVals[1]).grid(column=1, row=rowCount, sticky=NW)
    newRow()
    Label(root, textvariable=kitchenVals[2], foreground="red").grid(row=rowCount, columnspan=5)
    newRow()
    Label(root, textvariable=kitchenVals[3], foreground="red").grid(row=rowCount, columnspan=5)

    newRow()
    Label(root, text="  ").grid(column=0, row=rowCount)
    newRow()
    Label(root, text="  ").grid(column=0, row=rowCount)

    newRow()
    Label(root, text="Bathroom air quality: ").grid(column=0, row=rowCount, sticky=NE)
    Label(root, textvariable=bathroomVals[0]).grid(column=1, row=rowCount, sticky=NW)
    newRow()
    Label(root, text="Bathroom window state: ").grid(column=0, row=rowCount, sticky=NE)
    Label(root, textvariable=bathroomVals[1]).grid(column=1, row=rowCount, sticky=NW)
    newRow()
    Label(root, textvariable=bathroomVals[2], foreground="red").grid(row=rowCount, columnspan=5)
    newRow()
    Label(root, textvariable=bathroomVals[3], foreground="red").grid(row=rowCount, columnspan=5)

    newRow()
    Label(root, text="  ").grid(column=0, row=rowCount)
    newRow()
    Label(root, text="  ").grid(column=0, row=rowCount)

    newRow()
    Label(root, text="Living room air quality: ").grid(column=0, row=rowCount, sticky=NE)
    Label(root, textvariable=livingRoomVals[0]).grid(column=1, row=rowCount, sticky=NW)
    newRow()
    Label(root, text="Living room window state: ").grid(column=0, row=rowCount, sticky=NE)
    Label(root, textvariable=livingRoomVals[1]).grid(column=1, row=rowCount, sticky=NW)
    newRow()
    Label(root, textvariable=livingRoomVals[2], foreground="red").grid(row=rowCount, columnspan=5)
    newRow()
    Label(root, textvariable=livingRoomVals[3], foreground="red").grid(row=rowCount, columnspan=5)

    root.mainloop()


def updateTemperature(newValue):
    if(newValue > -999999):
        temperatureVar.set(str(round(newValue, 2)) + " C°")

def updatePressure(newValue):
    if (newValue > -999999):
        pressureVar.set(str(round(newValue, 2)) + " hPa")

def updateWeatherForecast(newValue):
    foreCast.set(newValue)

def updateSimTim(newValue):
    simTime.set(str(time.ctime(round(newValue/1000))))

def updateEnergyConsumption(newValue):
    if (newValue > -999999):
        energyConsumptionVar.set(str(round(newValue, 2)) + " kW")

def updateEnergyProduce(newValue):
    if (newValue > -999999):
        energyProduceVar.set(str(round(newValue, 2)) + " kW")

def updateEnergyBattery(newValue):
    energyBattery.set(str(round(newValue, 2)) + " %")

def updateEnergyCostDay(newValue):
    energyCostDay.set(str(round(newValue, 2)) + " €")

def updateEnergyCostMonth(newValue):
    energyCostMonth.set(str(round(newValue, 2)) + " €")

def updateEnergyAvailableInfo(show):
    if show:
        energyAvailableInfo.set(ENERGY_AVAILABLE_INFO)
    else:
        energyAvailableInfo.set("")


def updateBedRoomAirQuality(newValue):
    if (newValue > -999999):
        bedroomVals[0].set(str(round(newValue, 2)) + " ppm")


def updateKitchenAirQuality(newValue):
    if (newValue > -999999):
        kitchenVals[0].set(str(round(newValue, 2)) + " ppm")


def updateBathRoomAirQuality(newValue):
    if (newValue > -999999):
        bathroomVals[0].set(str(round(newValue, 2)) + " ppm")


def updateLivingRoomAirQuality(newValue):
    if (newValue > -999999):
        livingRoomVals[0].set(str(round(newValue, 2)) + " ppm")


def updateBedRoomWindowState(isOpen):
    if isOpen:
        bedroomVals[1].set(" open")
    else:
        bedroomVals[1].set(" closed")


def updateKitchenWindowState(isOpen):
    if isOpen:
        kitchenVals[1].set(" open")
    else:
        kitchenVals[1].set(" closed")


def updateBathRoomWindowState(isOpen):
    if isOpen:
        bathroomVals[1].set(" open")
    else:
        bathroomVals[1].set(" closed")


def updateLivingRoomWindowState(isOpen):
    if isOpen:
        livingRoomVals[1].set(" open")
    else:
        livingRoomVals[1].set(" closed")


def updateBedRoomCloseWindowWarning(show):
    if show:
        bedroomVals[2].set(SHOULD_CLOSE_WINDOW)
    else:
        bedroomVals[2].set("")


def updateKitchenCloseWindowWarning(show):
    if show:
        kitchenVals[2].set(SHOULD_CLOSE_WINDOW)
    else:
        kitchenVals[2].set("")


def updateBathRoomCloseWindowWarning(show):
    if show:
        bathroomVals[2].set(SHOULD_CLOSE_WINDOW)
    else:
        bathroomVals[2].set("")


def updateLivingRoomCloseWindowWarning(show):
    if show:
        livingRoomVals[2].set(SHOULD_CLOSE_WINDOW)
    else:
        livingRoomVals[2].set("")


def updateBedRoomOpenWindowWarning(show):
    if show:
        bedroomVals[3].set(SHOULD_OPEN_WINDOW)
    else:
        bedroomVals[3].set("")


def updateKitchenOpenWindowWarning(show):
    if show:
        kitchenVals[3].set(SHOULD_OPEN_WINDOW)
    else:
        kitchenVals[3].set("")


def updateBathRoomOpenWindowWarning(show):
    if show:
        bathroomVals[3].set(SHOULD_OPEN_WINDOW)
    else:
        bathroomVals[3].set("")


def updateLivingRoomOpenWindowWarning(show):
    if show:
        livingRoomVals[3].set(SHOULD_OPEN_WINDOW)
    else:
        livingRoomVals[3].set("")
