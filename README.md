# PrusaPPSInsertPauseForPrintSheet
Post processing script for prusaslicer that adds a M0 Pause after the brim to allow to place a color transfer sheet

Inspired by this video, I decided to create a script that makes placing a transfer sheet easier, whithout having to manually editing the gcode
https://www.youtube.com/watch?v=Jq13diBRQcA&t=13s

# Usage
## Ensure you have python 3.18 or newer installed
if not please install python from https://www.python.org/

## Ensure your printer IS NOT using binary mode
Go to:

Printers -> Firmware
 
uncheck Supports Binary G-code

## Add the post-processing script to the slicer
Go to:

Print settings -> Output options -> Post-processing scripts

Add the following line, replacing the Brackets <> with the right contents

```"<Path/To/Python313/python>" "<Path/to/AddPauseForSheetPostprocessingScript.py>" -offset 0.10 -message "Place sheet" -speed 2400 -liftDistance 50.00000```


# Arguments
```-offset 0.10```
  
  After pausing the printer will use a Z offset defined by this argument, this is due the transfer sheet having some thickness
  
```-message "Place sheet"```
  
  Message to display when pausing the print
  
```-speed 2400```
  
  Speed for the lift and drop
  
```-liftDistance 50.00000```
  
  Lift Distance to allow for Transfer Sheet to be placed down on the print bed

# To Do
+ Add arguments for tone pitch and duration
