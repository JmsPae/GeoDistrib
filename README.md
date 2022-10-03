# GeoDistrib
Basic tool for interpolating cell/zonal statistics among contained features based on a user defined weight attribute.

## Background
This little tool came about primarily to distribute population statistics from a population grid to individual building polygons for a simulation project. Population data per household is difficult to come by and I didn't need anything too precise so this seemed like a decent compromise. 

## Functionality
GeoDistrib is currently configured as a command line tool with basic functionality. You can either check the example folder or `python3 -m geodistrib --help`

What features receive the statistics/data from which source cell is currently decided by centroid.

## Future
The present tool was designed (not really *designed*, but it sounds clever) for a very specific purpose at the time. At whilst that makes this a very simple tool, it has the potential to become greatly expanded in complexity, and thus, hopefully, functionality. Performance isn't fantastic either.

The current plan is to add a json pipeline input, which lets the user define what and how the data from any number of fields will be distributed to any destination features. 