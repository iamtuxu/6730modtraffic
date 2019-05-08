from sim import *

simMain(globalVariable.defaultSetting, 20)

newSetting = globalVariable.defaultSetting
newSetting.sigmaDimensionless = 0.1

simMain(newSetting, 20)