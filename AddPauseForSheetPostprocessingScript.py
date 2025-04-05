#!/usr/bin/python
import sys
import re
import os
import logging
#import debugpy
import argparse
import time

# Global Regex
RGX_FIND_G1Z = r"G1.* [zZ]([-0-9.]+)"



# # Listen on a specific port (e.g., 5678)
# debugpy.listen(5678)

# # # Wait for a debugger to attach
# print("Waiting for debugger to attach...")
# debugpy.wait_for_client()
# print("Debugger attached, continuing execution...")
# breakpoint()


def main(sourceFile,offset,message,speed,liftDistance):
    gcodeLineBrim = ";TYPE:Skirt/Brim\n"
    gcodeLinePerimeter = ";TYPE:"
    state = 0
    #0 Pre brim
    # copy line to output
    # if il is equal to gcodeLineBrim 
    #   change state to 1
    #
    # 1 Before first perimeter
    #   if oline with gcodeLinePerimeter
    #       insert change toolhead speed to speed to of
    #       insert move to offset
    #       insert pause command to of with the message message
    #       insert move back to LastZ
    #       set state to 2
    #   regex for g1 and save last z pos
    #   if match replace lastz with regex match
    #   copy line to ofile
    #
    #2: post external permitere
    # copy if line to of inconditinably

    # Read the ENTIRE g-code file into memory
    try:
        with open(sourceFile, "r") as f:
            lines = f.readlines()
        f.close()
    except UnicodeDecodeError:
        print("ERROR: Binary Code is not supported for postprocessing scripts")
        logging.exception("message")
        time.sleep(10)
        exit()
    except:    
        print("ERROR: Something Went wrong")
        logging.exception("message")
        time.sleep(10)
        exit()

    lastZ = -0.0
    with open(sourceFile, "w") as of:
        for lIndex in range(len(lines)):
            oline = lines[lIndex]
            match state:
                case 0:
                    of.write(oline)
                    if oline == gcodeLineBrim:
                        state = 1
                case 1:
                    #if 'Z' in oline:
                        #breakpoint()
                    if oline.startswith(gcodeLinePerimeter):
                        state = 2
                        of.write(";Pause for print sheet\n")
                        of.write("G1 F{0} ;set Move Speed\n".format(speed))
                        of.write("G1 Z{:f} ; Lift for sheet\n".format(liftDistance))
                        of.write("M300 S440 P200; make some noise\n")
                        of.write(";Pause Print")
                        of.write("M0 {0} \n".format(message))
                        of.write("M290 Z{0} ; move up{0}mm on the Z axis\n".format(offset))
                        of.write("G1 Z{0:f} ;return toolhead to previous height\n".format(lastZ))
                    m = re.match(RGX_FIND_G1Z,oline)
                    if m != None:
                        lastZ = float(m.group(1))
                    of.write(oline)
                case 2:
                    of.write(oline)
    of.close()

# -offset 0.10 -message "Place sheet" -speed 2400 -liftDistance 50.0
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Post-process G-code for adding a pause after the brim.")
    parser.add_argument("input_file", help="Path to the input G-code file")
    parser.add_argument("-offset", type=float, default=0.10, help="Change Z offset to compesate for sheet thickness")
    parser.add_argument("-message", type=str, default="Place sheet" , help="Message to be put in the pause message")
    parser.add_argument("-speed", type=float, default=2400.0, help="Change Z offset to compesate for sheet thickness")
    parser.add_argument("-liftDistance", type=float, default=50.0, help="Change Z offset to compesate for sheet thickness")
    args = parser.parse_args()
    main(sourceFile=args.input_file,offset=args.offset,message=args.message,speed=args.speed,liftDistance=args.liftDistance)
