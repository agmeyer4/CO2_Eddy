# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 13:10:24 2020

@author: agmey
"""
def downsample_and_concatenate(dict_of_df):
    data = dict_of_df.copy(deep=True)
    return_data = {}
    return_data['Picarro'] = concat_pic(data)
    return_data['Multi'] = concat_multi(data)
    return_data['LI'] = data['LI_Vent'].set_index('Corrected_DT',drop=False).resample('1S').mean()
    return_data['Vent'] = data['Vent_Anem_Temp'].drop(['EPOCH_TIME','Corrected_ET'],axis=1).set_index('Corrected_DT').resample('10S').mean()
    return_data['WBB_CO2'] = data['WBB_CO2'].drop('index',axis=1)#.set_index('Corrected_DT').resample('10S').mean()
    return_data['WBB_Weather'] = data['WBB_Weather'].drop('index',axis=1).set_index('Corrected_DT').resample('T').mean()
    #for key in return_data:
        #return_data[key].reset_index(drop=False,inplace=True)
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