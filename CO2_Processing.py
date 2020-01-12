# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 13:10:24 2020

@author: agmey
"""
def downsample_and_concatenate(dict_of_df):
    data = dict_of_df.copy() #hello
    return_data = {}
    return_data['Picarro'] = concat_pic(data)
    return_data['Multi'] = concat_multi(data)
    return_data['LI'] = data['LI_Vent'].drop(['EPOCH_TIME','Corrected_ET'],axis=1).set_index('Corrected_DT',drop=False).resample('1S').mean()
    return_data['Vent'] = data['Vent_Anem_Temp'].drop(['EPOCH_TIME','Corrected_ET'],axis=1).set_index('Corrected_DT').resample('10S').mean()
    return_data['WBB_CO2'] = data['WBB_CO2'].set_index('Corrected_DT').resample('10S').mean()
    return_data['WBB_Weather'] = data['WBB_Weather'].set_index('Corrected_DT').resample('T').mean()
    # for key in return_data:
    #     return_data[key].reset_index(drop=False,inplace=True)
    return return_data
#==============================================================================================================#
def concat_pic(data_dict):
    ######################################################################
    # Function to concatenate all of the picarro dataframes from         #
    # a dictionary of split dataframes. Resamples at 0.1 second intervals#
    # by mean. Returns the concatenated dataframe                        #
    ######################################################################
    import pandas as pd
    print("Concatenating Picarro Data")
    co2_resample = data_dict['Picarro_CO2'].drop(['EPOCH_TIME','Corrected_ET'],axis=1).set_index('Corrected_DT',drop=False).resample('0.1S').mean() #resample from corrected data
    anem_resample = data_dict['Picarro_ANEM'].drop(['EPOCH_TIME','Corrected_ET','Pic_Loc'],axis=1).set_index('Corrected_DT',drop=False).resample('0.1S').mean() #resample from corrected data
    return pd.concat([co2_resample,anem_resample],axis=1)   #concatenate and return
#==============================================================================================================#
def concat_multi(data_dict):
    ######################################################################
    # Function to concatenate all of the multiplexer dataframes from     #
    # a dictionary of split dataframes. Resamples at 1 second intervals  #
    # by mean. Returns the concatenated dataframe                        #
    ######################################################################
    import pandas as pd
    print("Concatenating Multi Data")
    Multi1_resample = data_dict['Multiplexer_CO2_1'].drop(['EPOCH_TIME','Corrected_ET','Location'],axis=1).set_index('Corrected_DT',drop=False).resample('1S').mean() #resample from corrected data
    Multi2_resample = data_dict['Multiplexer_CO2_2'].drop(['EPOCH_TIME','Corrected_ET','Location'],axis=1).set_index('Corrected_DT',drop=False).resample('1S').mean()#resample from corrected data
    Multi3_resample = data_dict['Multiplexer_CO2_3'].drop(['EPOCH_TIME','Corrected_ET','Location'],axis=1).set_index('Corrected_DT',drop=False).resample('1S').mean()#resample from corrected data
    MultiWeather_resample = data_dict['Multiplexer_Weather'].drop(['EPOCH_TIME','Corrected_ET'],axis=1).set_index('Corrected_DT',drop=False).resample('1S').mean()#resample from corrected data
    return pd.concat([Multi1_resample,Multi2_resample,Multi3_resample,MultiWeather_resample],axis=1)#concatenate and return
#==============================================================================================================#
def find_timesteps(df):
    from collections import Counter
    data = df.copy()
    if 'Corrected_DT' in data.columns:
        diff = data['Corrected_DT']-data['Corrected_DT'].shift(1)
    else:
        diff = data.reset_index()['Corrected_DT']-data.reset_index()['Corrected_DT'].shift(1)    
    c = Counter(diff)
    return c.most_common()[0][0].total_seconds()
#==============================================================================================================#
def moving_average(df,time_window):
    data = df.copy()
    t_step = find_timesteps(data)
    roll_num = int(time_window//t_step)
    return data.rolling(roll_num,center=True).mean()
#==============================================================================================================#
def dwn_sample(df,time_window):
    data = df.copy()
    return data.resample('{}S'.format(time_window)).mean() 
#==============================================================================================================#
def pre_ds_filter(filter_func,dict_of_dfs):
    data = dict_of_dfs.copy()
    for key in data:
        if (filter_func == moving_average) | (filter_func == dwn_sample):
            time_window = float(input("Input the time window in seconds over which to conduct the filter function for {}".format(key)))
            data[key] = filter_func(data[key],time_window)
    return data