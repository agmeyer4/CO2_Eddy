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
    
    data['Vent_Anem_Temp']['DOW'] = data['Vent_Anem_Temp']['Corrected_DT'].dt.dayofweek
    data['Vent_Anem_Temp'] = set_vent_zeros(data['Vent_Anem_Temp'])
    return_data['Vent'] = data['Vent_Anem_Temp'].drop(['EPOCH_TIME','Corrected_ET'],axis=1).set_index('Corrected_DT').resample('10S').mean()
    return_data['Vent'].interpolate(limit=1,inplace=True)
    
    
    return_data['WBB_CO2'] = data['WBB_CO2'].set_index('Corrected_DT').resample('10S').mean()
    return_data['WBB_Weather'] = data['WBB_Weather'].set_index('Corrected_DT').resample('T').mean()
    for key in return_data:
        return_data[key]['DOW'] = return_data[key].index.dayofweek

    return return_data

#==============================================================================================================#
def set_vent_zeros(vent_df):
    print('setting night vent data to zero')
    vent = vent_df.copy()
    vent.loc[(vent['Rotations']<80)&((vent.Corrected_DT.dt.hour<10)|(vent.Corrected_DT.dt.hour>17)|(vent.DOW == 5)|(vent.DOW == 6)), ['Rotations','Velocity']]=0.0
    return vent
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
    Multi1_resample = data_dict['Multiplexer_CO2_1'].drop(['EPOCH_TIME','Corrected_ET'],axis=1).set_index('Corrected_DT',drop=False).resample('1S').mean() #resample from corrected data
    Multi2_resample = data_dict['Multiplexer_CO2_2'].drop(['EPOCH_TIME','Corrected_ET','Multi_Loc'],axis=1).set_index('Corrected_DT',drop=False).resample('1S').mean()#resample from corrected data
    Multi3_resample = data_dict['Multiplexer_CO2_3'].drop(['EPOCH_TIME','Corrected_ET','Multi_Loc'],axis=1).set_index('Corrected_DT',drop=False).resample('1S').mean()#resample from corrected data
    MultiWeather_resample = data_dict['Multiplexer_Weather'].drop(['EPOCH_TIME','Corrected_ET'],axis=1).set_index('Corrected_DT',drop=False).resample('1S').mean()#resample from corrected data
    concat = pd.concat([Multi1_resample,Multi2_resample,Multi3_resample,MultiWeather_resample],axis=1)#concatenate and return
    #concat['DOW'] = concat.Datetimeindex.dayofweek
    
    return concat
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
    if 'Corrected_DT' in data.columns:
        data.set_index('Corrected_DT',inplace=True)
    return data.rolling(roll_num,center=True).mean()
#==============================================================================================================#
def dwn_sample(df,time_window):
    data = df.copy()
    if 'Corrected_DT' in data.columns:
        result = data.set_index('Corrected_DT').resample('{}S'.format(time_window)).mean() 
    else :
        result =  data.resample('{}S'.format(time_window)).mean() 
    return result
#==============================================================================================================#
def pre_ds_filter(filter_func,dict_of_dfs):
    data = dict_of_dfs.copy()
    for key in data:
        if (filter_func == moving_average) | (filter_func == dwn_sample):
            time_window = float(input("Input the time window in seconds over which to conduct the filter function for {}".format(key)))
            data[key] = filter_func(data[key],time_window)
    return data
#==============================================================================================================#
def combine_vent_data(dict_of_dfs):
    import pandas as pd
    data = dict_of_dfs.copy()
    data['Vent_Mass'] = pd.concat([dwn_sample(data['LI'],10),data['Vent'].drop('DOW',axis=1),data['WBB_CO2'].drop(['EPOCH_TIME'],axis=1)],axis=1)
    data['Vent_Mass']['Q'] = float('NaN')
    data['Vent_Mass'].loc[data['Vent_Mass']['Velocity']>0.0,['Q']]=5.77
    data['Vent_Mass'].loc[data['Vent_Mass']['Velocity']==0.0,['Q']]=0.0
    del data['Vent']
    del data['LI']
    return data
#==============================================================================================================#

def moving_mass_flow(concat_df):
    import pandas as pd
    df = concat_df.copy()
    R = 8.3145
    P = 85194.46
    T = df['Temp_1']+273
    df['Excess'] = df['LI_CO2'] - df['WBB_CO2'].interpolate()
    Excess = df['Excess']
    C_v = Excess*10**(-6)
    M_m = 44.01
    df['C_m'] = P*C_v*M_m/(R*T)
    Q = df['Q']
    df['m_dot'] = df.apply(lambda row: 0.0 if row['Q'] == 0.0 else row['Q']*row['C_m'],axis=1)
    df.drop(['C_m'],axis=1,inplace=True)
    return df
