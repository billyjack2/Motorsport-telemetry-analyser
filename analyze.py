from xrk_wrapper import *
from vehicleConfig import *
import math

# Analyze contains the logic for looking through the data provided by the XRK Wrapper. All logic, both generic (min, max, avg, etc)
# specific (RPM limit, coolant limit, etc), and custom (define channel and limit) occur here. 

OIL_RPM_LIMIT = 500
OIL_RPM_THRESHOLD = 2000

class Analyze():
    def __init__(self, wrapper:XrkWrapper):
        self.wrapper = wrapper

    def getMin(self, index: int):
        data = self.wrapper.getChannelData(index)

        m = min(data.samples)
        return m

    def getMax(self, index: int):
        data = self.wrapper.getChannelData(index)

        m = max(data.samples)
        return m

    def getAvg(self, index: int):
        data = self.wrapper.getChannelData(index)

        return sum(data.samples)/self.wrapper.getChannelSamplesCount(index)

    
    

    def oilPress(self, oilPsiIndex:int, rpmIndex:int):
        #TODO check that all indexes exist
        
        oilPsiSamples = self.wrapper.getChannelSamples( oilPsiIndex )
        # TODO check if index returns anything
        
        rpmSamples = self.wrapper.getChannelSamples( rpmIndex )
        
    # Check if rpm limit ever exceeded threshold    
    def rpmLimit(self, rpmIndex: int):
        
        #data pair of samples and times
        exceededSamples = list()
        exceededTimes = list()
        
        #get RPM data
        data = self.wrapper.getChannelData(rpmIndex)
        
        for index, sample in enumerate(data.samples):
            if sample > MAX_RPM:
                exceededSamples.append(data.samples[index])
                exceededSamples.append(data.times[index])
        
        # build channel data object
        exceededData = ChannelData(self.wrapper.getChannel(rpmIndex), exceededSamples, exceededTimes)        
                
        return ExceededLimits(exceededData, MAX_RPM )

# class for containing list of exceeded limits of a given channel
class ExceededLimits():
     def __init__(self, channelData: ChannelData, limit: int):
        self.limit = limit
        self.data = channelData
         




wrap = XrkWrapper()
wrap.loadFile(os.path.dirname(__file__) + "\\test-files\\" + "test.xrk")
a = Analyze(wrap)

print(wrap.getTrackName())

index = 10

exceeded = a.rpmLimit(index)
print("Channel: " + wrap.getChannelName(index))
print("Exceeded samples: " + str(exceeded.data.samples.__len__()))
print("min: " + str(a.getMin(index)))
print("avg: " + str(a.getAvg(index)))
print("max: " + str(a.getMax(index)))
print(wrap.closeFile())