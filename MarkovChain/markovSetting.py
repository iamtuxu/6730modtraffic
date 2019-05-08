import math


class MarkovSetting(object):
    def __init__(self):
        self.simulationTimeStep = 1.2  # in sec
        self.beta = 250
        self.targetSpeed = 100  # in km/h
        self.jamDensity = 150  # veh/km
        self.jamSpacing = 1 / self.jamDensity * 1000
        self.sigmaDimensionless = 0.02
        self.roadLength = 2000  # in meter
        self.SD = self.calculateStandardDeviation()
        self.sigma = self.sigmaDimensionless * math.sqrt(self.beta) * self.targetSpeed

    def calculateStandardDeviation(self):
        denominator = math.sqrt(2)
        self.sigma = self.sigmaDimensionless * math.sqrt(self.beta) * self.targetSpeed
        numeratorNumerator = 3 + math.exp(-2 * self.simulationTimeStep / 3600 * self.beta) - 4 * math.exp(
            -1 * self.simulationTimeStep / 3600 * self.beta) - 2 * self.simulationTimeStep / 3600 * self.beta
        numeratorDenominator = -1 * self.beta * self.beta * self.beta
        numerator = math.sqrt((numeratorNumerator / numeratorDenominator)) * self.sigma
        return numerator / denominator * 1000
