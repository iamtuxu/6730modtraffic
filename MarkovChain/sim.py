from car import *
import datetime
import time
import matplotlib.pyplot as plt
import globalVariable


def simMain(aimSetting, numberOfCars):
    stringStartTime = stringTimestamp()
    cars = []
    initialSpeed = 0
    initialAcceleration = 0
    initialPosition = 0
    aimSetting.SD = aimSetting.calculateStandardDeviation() # calculate the SD again, in case sigma changed

    for i in range(numberOfCars):
        # initialization of the car
        newCar = carMarkov(aimSetting, initialPosition, initialSpeed, initialAcceleration)
        newCar.setting = aimSetting
        if i > 0:
            newCar.leader = cars[i - 1]  # attach the leader
        initialPosition -= aimSetting.jamSpacing  # initial position
        flag = True  # on the road
        print("Processing Vehicle " + str(i + 1))  # for debug

        # while loop
        while flag:
            flag = newCar.update()

        # put the car in array
        newCar.outputSingleFile("./output/" + stringStartTime + "_" + str(i + 1) + ".csv")
        cars.append(newCar)

    maxTrajectoryLength = 0
    for i in range(len(cars)):
        if len(cars[i].trajectories) > maxTrajectoryLength:
            maxTrajectoryLength = len(cars[i].trajectories)

    # let us prepare the plot
    timeSeries = []
    for j in range(maxTrajectoryLength):
        timeSeries.append(j * aimSetting.simulationTimeStep)

    # the positions
    plotPositions = [[] for i in range(len(cars))]
    for j in range(maxTrajectoryLength):
        for i in range(len(cars)):
            if j < len(cars[i].trajectories):
                plotPositions[i].append(cars[i].trajectories[j].position)
            else:
                plotPositions[i].append(cars[i].trajectories[len(cars[i].trajectories) - 1].position)

    # plot
    for i in range(len(cars)):
        plt.plot(timeSeries, plotPositions[i])
    plt.ylim([initialPosition, aimSetting.roadLength])

    plt.xlabel('Simulation Time (s)')
    plt.ylabel('Distance (m)')
    plt.title('Time-Distance Diagram of ' + str(numberOfCars) + ' Cars with Sigma of ' + str(round(aimSetting.sigma,2)))
    plt.show()

    # do the aggregated output
    # open and print the headline
    fileOut = open('./output/' + stringStartTime + "_Total.csv", 'w')
    print("StateID,Time(s)", file=fileOut, end="")
    for i in range(len(cars)):
        print(",Position%d(m)" % (i + 1), file=fileOut, end="")
    print("", file=fileOut)

    # iteration
    for j in range(maxTrajectoryLength):
        print("%d,%.1f" % ((j + 1), (j + 1) * aimSetting.simulationTimeStep), file=fileOut, end="")
        for i in range(len(cars)):
            if j < len(cars[i].trajectories):
                print(",%.2f" % cars[i].trajectories[j].position, file=fileOut, end="")
            else:
                print(",%.2f" % cars[i].trajectories[len(cars[i].trajectories) - 1].position, file=fileOut, end="")
        print("", file=fileOut)

    fileOut.close()


def stringTimestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%m%d%y%H%M%S')
    return st
