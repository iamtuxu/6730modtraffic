from globalVariable import *
from basicFunction import *
import math


class trajectory(object):
    def __init__(self, initialPosition=0, initialSpeed=0, initialAcceleration=0):
        self.speed = initialSpeed  # in km/h
        self.position = initialPosition  # in meter
        self.acceleration = initialAcceleration  # in m/s^2
        self.expectedDeisiredPosition = 0  # in meter
        self.deviatedDisplacement = 0  # in meter
        self.constrainedPosition = 0  # in meter
        self.desiredPosition = 0  # in meter

    def updatePosition(self):
        self.position = min(self.desiredPosition, self.constrainedPosition)


class carMarkov(object):
    def __init__(self, objectiveSetting = defaultSetting, initialPosition=0, initialSpeed=0, initialAcceleration=0):
        self.trajectories = []
        '''
        self.position = 0
        self.speed = 0
        self.lastAcceleration = 0
        self.lastPosition = 0
        '''
        newTrajectory = trajectory(initialPosition, initialSpeed, initialAcceleration)
        self.trajectories.append(newTrajectory)
        self.currentTrajectory = newTrajectory # use this as the current position and speed
        self.leader = None # attached later
        self.currentStateID = 0
        self.setting = objectiveSetting

    def desiredNewPosition(self, newTrajectory):

        # desired speed calculated in 2 steps
        desiredDisplacement = self.currentTrajectory.speed - self.setting.targetSpeed + (
                (self.setting.targetSpeed - self.currentTrajectory.speed) * math.exp(
            -1 * self.setting.simulationTimeStep / 3600 * self.setting.beta)) + (
                                      self.setting.simulationTimeStep / 3600 * self.setting.targetSpeed * self.setting.beta)  # divider
        desiredDisplacement = desiredDisplacement / self.setting.beta  # in km

        # desired position with random variance
        newTrajectory.expectedDeisiredPosition = self.currentTrajectory.position + (desiredDisplacement * 1000)
        newTrajectory.deviatedDisplacement = randomDisplacementDeviation((desiredDisplacement * 1000), self.setting.SD)

        newTrajectory.desiredPosition = self.currentTrajectory.position + newTrajectory.deviatedDisplacement

    def constrainedNewPosition(self, newTrajectory):
        if self.leader is not None:
            if self.currentStateID == 0:
                newTrajectory.constrainedPosition = self.currentTrajectory.position
            elif len(self.leader.trajectories) >= self.currentStateID:
                newTrajectory.constrainedPosition = self.leader.trajectories[
                                                        self.currentStateID - 1].position - self.setting.jamSpacing
            else:
                newTrajectory.constrainedPosition = 2 * self.setting.roadLength # this is basically infinite
        else:
            newTrajectory.constrainedPosition = 2 * self.setting.roadLength # this is basically infinite

    def newPosition(self, newTrajectory):
        newTrajectory.updatePosition()
        newTrajectory.speed = (
                                      newTrajectory.position - self.currentTrajectory.position) / self.setting.simulationTimeStep * 3.6
        self.currentTrajectory.acceleration = newTrajectory.speed - self.currentTrajectory.speed

    def update(self):
        newTrajectory = trajectory(self.currentTrajectory.position)
        self.desiredNewPosition(newTrajectory)
        self.constrainedNewPosition(newTrajectory)
        self.newPosition(newTrajectory)
        self.trajectories.append(newTrajectory)
        self.currentStateID += 1
        self.currentTrajectory = self.trajectories[self.currentStateID]
        if self.currentTrajectory.position > self.setting.roadLength:
            return False # it needs to exit the simulation
        else:
            return True # it stays in the system

    def outputSingleFile(self, aimFileAddress):
        fileOut = open(aimFileAddress, 'w')
        print(
            "StateID,Time(s),Position(m),Speed(m/s),Acceleration(m/s^2),constrainedPosition(m),desiredPosition(m),expectedDeisiredPosition(m),deviatedDesiredDisplacement(m)",
            file=fileOut)
        for i in range(len(self.trajectories)):
            print("%d,%.1f," % (i, i * self.setting.simulationTimeStep), file=fileOut, end="")
            print("%.2f,%.2f," % (self.trajectories[i].position, self.trajectories[i].speed / 3.6), file=fileOut,
                  end="")
            print("%.2f," % (self.trajectories[i].acceleration / 3.6), file=fileOut, end="")
            print("%.2f,%.2f," % (self.trajectories[i].constrainedPosition, self.trajectories[i].desiredPosition),
                  file=fileOut, end="")
            print("%.2f,%.2f" % (
            self.trajectories[i].expectedDeisiredPosition, self.trajectories[i].deviatedDisplacement),
                  file=fileOut)
        fileOut.close()
