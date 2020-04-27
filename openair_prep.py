from CO2_Dataset_Preparation import *
from CO2_functions import * 
from CO2_Processing import *


for pn in range(1,7):
    excess_rolls = excess_rolls_sec = [1,10,60,600,3600] #these specify the rolling window (in seconds) on which a minimum is applied for excess 
    tower = 'Picarro'
    position_number = pn
    downsample_sec =1
    wind_rolls = [1,5,10,30,60,600,3600]
    lag_shifts = [1,3,5,10,15,20,25,30,35,40,45,50,55,60,90,120]

    print(f"Processing data for {tower}\nPosition Number = {position_number}")

    if (tower == 'WBB') & (downsample_sec<60):
        raise ValueError('downsampling for WBB tower must be at least 60 seconds to conform with wind sampling')

    def process_for_openair(excess_rolls,tower,position_number,downsample_sec,wind_rolls,lag_shifts):
        data = Processed_Set(tower,position_number,excess_rolls_sec,vent_bool = True,wbb_bool=False)
        data._retrieve_data('../CO2_Data_Processed/')
        data._apply_excess(delete_min_cols = True)
        data._combine_vent_tower(downsample_sec)
        if tower == 'Picarro':
            data._add_rolling_wind(wind_rolls,delete_anem_bool = False)
        data._column_shifter(lag_shifts,delete=False)
        data._vent_on_only()
        d = data.df.dropna(how='all').to_csv(f'../CO2_Data_Processed/R_Dataframes/{tower}_{position_number}.csv')

    process_for_openair(excess_rolls,tower,position_number,downsample_sec,wind_rolls,lag_shifts)
