from CO2_Dataset_Preparation import *
from CO2_functions import * 
from CO2_Processing import *

print("helloworld")

excess_rolls = [10,60,3600,6000,36000] #these specify the rolling window on which a minimum is applied for excess 
tower = 'Picarro'
position_number = 6
downsample_sec = 1
wind_rolls = [5,10,30,60,600]
lag_shifts = [5,10,20,30,45,60,90,120]

def process_for_openair(excess_rolls,tower,position_number,downsample_sec,wind_rolls,lag_shifts):
    data = Processed_Set(tower,position_number,excess_rolls,vent_bool = True,wbb_bool=False)
    data._retrieve_data('../CO2_Data_Processed/')
    data._apply_excess()
    data._combine_vent_tower(downsample_sec)
    if tower == 'Picarro':
        data._add_rolling_wind(wind_rolls,False)
    data._column_shifter(lag_shifts,delete=False)
    data._vent_on_only()
    d = data.df.dropna(how='all').to_csv('../CO2_Data_Processed/R_Dataframes/test.csv')

process_for_openair(excess_rolls,tower,position_number,downsample_sec,wind_rolls,lag_shifts)