

import sys
from datetime import datetime
from enum import Enum
import pandas as pd
import ctypes

import clr
clr.AddReference( r"S:\Corporate Strategy\Infrastructure Strategies\Simulations\Software Libraries\IOLibrary\IOLibrary\bin\x64\Release\IOLibrary.dll")
#clr.AddReference( r"S:\Corporate Strategy\Infrastructure Strategies\Simulations\Software Libraries\Statistics\Statistics\bin\x64\Release\Statistics.dll")
clr.AddReference( r"S:\Corporate Strategy\Infrastructure Strategies\Simulations\Software Libraries\TrainLibrary\TrainLibrary\bin\x64\Release\TrainLibrary.dll")

from IOLibrary import FileOperations
from TrainLibrary import Processing, TrainRecord, trainCommodity, trainOperator, GeoLocation, LoopLocation, direction


def setParameters(arguments):
    
    # Default parameters
    corridorlabel = "Gunnedah"
    today = datetime.now()
    if today.month > 1:
        lastmonth = today.replace(month=today.month-1)
    else:
        lastmonth = today.replace(year=today.year-1)
        lastmonth = lastmonth.replace(month=12)
    dateRange = [lastmonth, today]

    # One parameter supplied is the corridor Label
    if len(arguments) == 2:
        corridorlabel = arguments[1]

    # Two parameters supplied is the date range
    if len(arguments) == 3:
        dateRange = [datetime.strptime(arguments[1], '%d/%m/%Y'),
                     datetime.strptime(arguments[2], '%d/%m/%Y')]

    # Three parameters supplied is the corridorLabel and date range
    if len(arguments) == 4:
        corridorlabel = arguments[1]
        dateRange = [datetime.strptime(arguments[2], '%d/%m/%Y'),
                     datetime.strptime(arguments[3], '%d/%m/%Y')]

    return corridorlabel, dateRange


if __name__ == '__main__':
    """
    The Main program to be run to automate the train processing.

    The Train Processing algorithm will take each train movement and interpolate to define a higher granularity 
    of measurements. The effect of the TSR's and trains stopping at loops is removed to indicate a potential 
    actual movement without any conflicts.
    The resulting train journey information will be written back to the datawarehouse.

    Refer to the TRAin Performance (TRAP) analysis manual for details of how the algorithm works.

    Optional Inputs: 
    corridorlabel: The corridor label to perform the processing on. This is currently limited to the Hunter Valley region
        permitted labels are "Gunnedah", "Ulan" or "Hunter" to represent each zone of hunter operations.
        Default: "Gunnedah"

    start_date: The start date of the processing period. 
        Prefered format: "1/1/2018"
        Default: 1 month prior to current date.

    end_date: The end date of the processing period.
        Prefered format: "1/2/2018"
        Default: current date.

    Limitations:
    There are some limitations regarding the valid values for each journey. Where a train does not run the full 
    length of the distance assumed for each corridor, the resulting journey will contain average train speeds 
    while traversing a loop.

    Calling Procedure:
    1. Automated_Train_Processing 
    2. Automated_Train_Processing <corridor_label>
    3. Automated_Train_Processing <start_date> <end_date>
    4. Automated_Train_Processing <corridor_label> <start_date> <end_date>

    e.g.
    Automated_Train_Processing "Ulan" "1/1/2018" "1/2/2018"


    Author: Beau Bellamy
    Version: 0.0.1
    """

    
    if len(sys.argv) > 4:
        sys.exit('Too many arguments; Try one of the follwing signatures\n'+
                 'Use default parameters:               AutoTrainProcessing()\n'+
                 'Define corridor:                      AutoTrainProcessing(corridorLabel)\n'+
                 'Define analysis period:               AutoTrainProcessing(fromDate, toDate)\n'+
                 'Define corridor and analysis period:  AutoTrainProcessing(corridorLabel,fromDate, toDate)')

    
    corridorlabel, dateRange = setParameters(sys.argv)
    

    
    processing = Processing()


    processTrainDataPoint = processing.AutomatedProcessing(dateRange[0].year, dateRange[0].month, dateRange[0].day, dateRange[1].year, dateRange[1].month, dateRange[1].day, corridorlabel)
    
   


    print (len(processTrainDataPoint))
    # Write the processTrainDataPoint back to the datawarehouse

    print ('Corridor: ', corridorlabel)
    print ('Idx, Train Date,	Train ID,	Loco ID, PW_ratio, Operator,	Commodity,	Direction,	Kilometreage,	Speed,	Time,	Latitude,	Longitude,	Elevation,	'+
           'isLoop,	isTSR,	isGap,	Simulation Speed,	Simualtion Time,	Average Speed,	Average Time')
    for idx in range(len(100)):
        
        print (idx, processTrainDataPoint[idx].trainDate.ToString(), processTrainDataPoint[idx].TrainID, processTrainDataPoint[idx].locoID, processTrainDataPoint[idx].PW_ratio, 
               processTrainDataPoint[idx].trainOperator, processTrainDataPoint[idx].commodity, processTrainDataPoint[idx].trainDirection, 
               processTrainDataPoint[idx].kmMarker, processTrainDataPoint[idx].speed, processTrainDataPoint[idx].transitTime, 
               processTrainDataPoint[idx].location.latitude,  processTrainDataPoint[idx].location.longitude, processTrainDataPoint[idx].alignmentElevation,
               processTrainDataPoint[idx].isLoop, processTrainDataPoint[idx].isTSR, processTrainDataPoint[idx].isLargeGap, 
               processTrainDataPoint[idx].simulationSpeed, processTrainDataPoint[idx].simulationTime, 
               processTrainDataPoint[idx].averageSpeed, processTrainDataPoint[idx].averageTime)

