from xrk_wrapper import *
import math

OIL_RPM_LIMIT = 500
OIL_RPM_THRESHOLD = 2000

class Analyze():
    def __init__(self, wrapper:XrkWrapper):
        self.wrapper = wrapper

    def getMin(self, index: int):
        data = self.wrapper.getChannelSamples(index)

        m = min(data.samples)
        return m

    def getMax(self, index: int):
        data = self.wrapper.getChannelSamples(index)

        m = max(data.samples)
        return m

    def getAvg(self, index: int):
        data = self.wrapper.getChannelSamples(index)

        return sum(data.samples)/self.wrapper.getChannelSamplesCount(index)

def oilPress(wrapper:XrkWrapper, oilPsiIndex:int, rpmIndex:int):
    #TODO check that all indexes exist
        
    oilPsiSamples = wrapper.getChannelSamples( oilPsiIndex )
    # TODO check if index returns anything

    rpmSamples = wrapper.getChannelSamples( rpmIndex )




wrap = XrkWrapper()
wrap.loadFile(os.path.dirname(__file__) + "\\" + "test.xrk")
a = Analyze(wrap)

print(wrap.getTrackName())

index = 10

print(a.wrapper.getChannelName(index))
print("min: " + str(a.getMin(index)))
print("avg: " + str(a.getAvg(index)))
print("max: " + str(a.getMax(index)))