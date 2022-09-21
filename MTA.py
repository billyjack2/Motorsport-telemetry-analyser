import sys
import argparse

# Orchestration of console version of Motorsport Telemetry Analyser

# Instantiate the parser
parser = argparse.ArgumentParser(description='Motorsport Telemetry Analyser')

parser.add_argument("-c", "--car", help="Display car information", action="store_true")

test = parser.parse_args()

# Arguments
args = sys.argv[1:]
print(args)

def printHelp():
        print("Motorsport Telemetry Analyser")
        print("This tool is used to bulk analyze AIM based telemetry files to determine if specific limits are exceeded and to analyze performance.\n")
        print("Usage:")
        print("MTA.py [options] [file...]")
        print("")
        print("Anaylse telemetry files passed. By default the configuration used will be the vehicle name of first file.")
        print("It is recommened to specify the vehicle config explicitly.")
        print("Example: MTA.py NP01 testfile1.xrk testfile2.xrk")
        print("")
        print("Options:")
        print("-h, --help      Display this help message")
        print("--config        Enter config editor, the telemetry file will be used to assist")
        print("--channels      Display channels in file")
        print("-t, --track: Display track information")
        print("-c, --car: Display car information")
        print("-d, --data: Display data")
        print("File: The telemetry file to analyse")
    
def printCar():
    print("car")

if test.car:
    print("cars")
    
# If no arguments present help
if len(args) == 0:
    printHelp()
    sys.exit()




