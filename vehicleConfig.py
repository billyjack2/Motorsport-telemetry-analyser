
MAX_RPM = 14000
MAX_COOLANT_TEMP = 90 #*C
MAX_OIL_TEMP = 100 #*C
MIN_OIL_PRESS = 20 #PSI
MIN_OIL_PRESS_RPM = 2000 #RPM above which to check oil pressure

class VehicleConfig:
    # create a vehicleConfig from the file based on the vehicleName
    # Search for and key off of the vehicleName
    def __init__(self, vehicleName: str, file= None):
        self.vehicleName = None
        self.limits = list()
        
        if file:
            # get the vehicle config file
            with open(file, 'r') as f:
                for line in f:
                    
                    # if self.vehicleConfig is set and we hit a blank we have grabbed the config
                    if self.vehicleName and line == "\n":
                        break

                    # find vehicle name
                    if line.startswith("VehicleConfig"):
                        
                        # if matches target vehicle name
                        if line.split(":")[1].strip() == vehicleName:
                            self.vehicleName = line.split(":")[1].strip()
                            continue
                        else:
                            continue
                    # get the limit
                    if self.vehicleName and line.startswith("Limit:"):
                        limit = line.split(" ")
                        self.addLimit(Limit(limit[1], limit[2], float(limit[3].strip())))
                
            # if we finished the file and vehicleName is not set then the vehicle is not in the config
            if not self.vehicleName:
                raise Exception("Vehicle not found in config file")
        
        
        
    
    def __str__(self):
        s = "VehicleConfig: " + self.vehicleName + "\n"
        
        for limit in self.limits:
            s += str(limit) + "\n"
        
        return s

    def addLimit(self, limit):
        self.limits.append(limit)

  


class Limit:
    def __init__(self, chName: str, unit: str, maxLimit: float):
        self.chName = chName
        self.unit = unit
        self.maxLimit = maxLimit

    def __str__(self):
        return "Limit: " + self.chName + " " + self.unit + " " + str(self.maxLimit)
    
    

# TODO enum for unit's and conversions otherwise user will always have to make the limit the same as the data


# TEST code
#config = VehicleConfig("NP01")
#config.addLimit(Limit("RPM", "RPM", 14000))
#config.addLimit(Limit("Coolant", "C", 100))


c = VehicleConfig("Adria Kart", "test.txt")
    
print(c)
  