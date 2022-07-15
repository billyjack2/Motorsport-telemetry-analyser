from array import ArrayType
from asyncio.windows_events import NULL
from ctypes import *
import ctypes
import os.path
import string

# Class that loads a DLL for pulling telemetry data and contains all wrapper functions and definitions 
# that are included in the dll. 
class XrkWrapper():

    def __init__(self, path:str):
        dllName = "MatLabXRK-2017-64-ReleaseU.dll"
        self.dll = cdll.LoadLibrary(path)
        # Try loading library via path
        try:
            self.dll = cdll.LoadLibrary(path)
        except FileNotFoundError:
            print("file not found")
            self.dll = cdll.LoadLibrary(os.path.dirname(__file__) + "\\lib\\" + dllName)
        except:
            print("Error - Unable to load XRK DLL")
            return

        self.defineFunctions()

    def __init__(self):
        dllName = "MatLabXRK-2017-64-ReleaseU.dll"
        self.dll = cdll.LoadLibrary(os.path.dirname(__file__) + "\\lib\\" + dllName)

        self.defineFunctions()

    def defineFunctions(self):

        # Get Library Date
        self.dll.get_library_date.argtypes = []
        self.dll.get_library_date.restype = c_char_p

        # Get Library Time
        self.dll.get_library_time.argtypes = []
        self.dll.get_library_time.restype = c_char_p

        # Get Vehicle Name
        self.dll.get_vehicle_name.argtypes = []
        self.dll.get_vehicle_name.restype = c_char_p

        # Track Name
        self.dll.get_track_name.argtypes = [ctypes.c_int]
        self.dll.get_track_name.restype = c_char_p

        # Racer Name
        self.dll.get_racer_name.argtypes = [ctypes.c_int]
        self.dll.get_racer_name.restype = c_char_p

        # Championship Name
        self.dll.get_championship_name.argtypes = [ctypes.c_int]
        self.dll.get_championship_name.restype = c_char_p

        # Venue type
        self.dll.get_venue_type_name.argtypes = [ctypes.c_int]
        self.dll.get_venue_type_name.restype = c_char_p

        # Date and time
        self.dll.get_date_and_time.argtypes = [ctypes.c_int]
        self.dll.get_date_and_time.restype = c_char_p

        # Get Laps Count
        self.dll.get_laps_count.argtypes = [ctypes.c_int]
        self.dll.get_laps_count.restype = ctypes.c_int

        # Get Lap info
        self.dll.get_lap_info.argtypes = [ctypes.c_int, ctypes.c_int, POINTER(c_double), POINTER(ctypes.c_double)]
        self.dll.get_lap_info.restype = ctypes.c_void_p

        # Channel Count
        self.dll.get_channels_count.argtypes = [ctypes.c_int]
        self.dll.get_channels_count.restype = c_int

        # Get Channel Name
        self.dll.get_channel_name.argtypes = [ctypes.c_int, ctypes.c_int]
        self.dll.get_channel_name.restype = c_char_p

        # Get Channel Units
        self.dll.get_channel_units.argtypes = [ctypes.c_int, ctypes.c_int]
        self.dll.get_channel_units.restype = c_char_p

        # Get Channel Samples
        self.dll.get_channel_samples.argtypes = [ctypes.c_int, ctypes.c_int, POINTER(ctypes.c_double), POINTER(ctypes.c_double), ctypes.c_int]
        self.dll.get_channel_samples.restype = c_int

        # Get Channel Sample Count
        self.dll.get_channel_samples_count.argtypes = [ctypes.c_int, ctypes.c_int]
        self.dll.get_channel_samples_count.restype = ctypes.c_void_p

        # Get lap channel samples count

        # Get lap channel samples

        # Get GPS channels count

        # Get GPS channel name
    
        # Get GPS Channel Units

        # Get GPS channel samples count

        # Get GPS channel samples

    def loadFile(self, filePath):

        try:
            self.retval = self.dll.open_file(str.encode(filePath))
        except:
            print("Error: File not found.")
        else:
            if self.retval < 0:
                print("File not found.")
        return

    def getLibraryDate(self):

        date = self.dll.get_library_date().decode("utf-8")
        return date

    def getLibraryTime(self):
        time = self.dll.get_library_time().decode("utf-8")
        return time

    def getTrackName(self):
        trackName = self.dll.get_track_name(self.retval).decode("utf-8")
        return trackName

    def getRacerName(self):
        racerName = self.dll.get_racer_name(self.retval).decode("utf-8")
        return racerName

    def getChampionshipName(self):
        name = self.dll.get_championship_name(self.retval).decode("utf-8")
        return name

    def getVenueTypeName(self):
        name = self.dll.get_venue_type_name(self.retval).decode("utf-8")
        return name

    def getChannelsCount(self):
        channelCnt = self.dll.get_channels_count(self.retval)
        return channelCnt

    def getChannelsList(self):
        chList = None
        for ch in range(self.getChannelsCount()):
            channel = Channel(ch, self.getChannelName(ch), self.getChannelUnits(ch))
            chList.append(channel)
        return chList

    def getChannelName(self, index):
        # TODO: index validation check

        channelName = self.dll.get_channel_name(self.retval,index).decode("utf-8")
        return channelName

    def getChannelUnits(self, index):
        # TODO: index validation check

        channelUnits = self.dll.get_channel_units(self.retval,index).decode("utf-8")
        return channelUnits

    def getChannelSamples(self, index):
        # TODO: index validation check

        count = self.getChannelSamplesCount(index)

        samples = (c_double * count)()
        times = (c_double * count)()
        self.dll.get_channel_samples(self.retval, index, times, samples, count)
        
        channel = Channel(index, self.getChannelName(index), self.getChannelUnits(index))
        channelData = ChannelData(channel,samples, times)
        return channelData

    def getChannelSamplesCount(self, index):
        # TODO: index validation check

        sampleCount = self.dll.get_channel_samples_count(self.retval,index)
        return sampleCount

    def getLapsCount(self):
        lapsCount = self.dll.get_laps_count(self.retval)
        return lapsCount

    def getLapInfo(self, index):
        # TODO: index validation check
        
        start = ctypes.c_double()
        duration = ctypes.c_double()

        self.dll.get_lap_info(self.retval, index, start, duration)
        return LapInfo(start.value, duration.value)

    def channelExists(self, index):
        # TODO: index validation
        return True

    def closeFile(self):
        self.dll.close_file_i(1)


# LapInfo contains the start time and duration of each lap
class LapInfo:
    def __init__(self, startTime, duration):
        self.startTime = startTime
        self.duration = duration


class Channel:
    """ Contains the name and units of a channel """
    def __init__(self, index: int, channelName: str, channelUnits: str):
        """Init Channel when all values are known"""
        self.index = index
        self.name = channelName
        self.units = channelUnits



class ChannelData:
    """Stores data and information of a given channel"""

    def __init__(self, channel: Channel, samples: ArrayType, times: ArrayType):
        self.channel = channel
        self.samples = samples
        self.times = times
        






#wrapper = XrkWrapper()
#path = os.path.dirname(__file__) + "\\" + "test.xrk"
#wrapper.loadFile(path)
#print("Lib Date:" + wrapper.getLibraryDate())
#print("Lib Time:" + wrapper.getLibraryTime())
#print("Track Name: " + wrapper.getTrackName())
#print("Racer Name: " + wrapper.getRacerName())
#print("Ch Count: " + str(wrapper.getChannelsCount()))
#print("Ch Name: " + wrapper.getChannelName(2))
#print(wrapper.getChannelUnits(2))
#print(wrapper.getChannelSamplesCount(2))
#print("Laps Cnt: " + str(wrapper.getLapsCount()))
#print("Start: " + str(wrapper.getLapInfo(2).startTime) + "  Duration: " + str(wrapper.getLapInfo(2).duration))
#print("Championship: " + wrapper.getChampionshipName())
#print("Venue Type: " + wrapper.getVenueTypeName())
#sample = wrapper.getChannelSamples(2)
#print(sample.channel.name + ": " + sample.channel.units)
#for i in range(8000,8025):
#    time = sample.times[i]
#    data = sample.samples[i]
#    txt = "{:.3f} - {:.3f}"
#    print(txt.format(time,data))