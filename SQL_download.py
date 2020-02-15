# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 12:56:31 2020

@author: agmey
"""
#=========================================================================================================#
def get_date_range():
    #Ask the user for a date range and return the results
    print("helloworld")
    date1=input("Enter Start Date YYYY-mm-DD: ")
    date2=input("Enter End Date YYYY-mm-DD: ") 
    return date1,date2

#=========================================================================================================#
    
def sql_connect():
    ######################################################################
    # Function to get exclusively "Spike Necessary" LI_8100 Data         # 
    # from SQL. Input the SQL Tablename, and date range between which    #
    # data will be fetched. For one day's worth of data, enter the same  #
    # Date.                                                              #
    ######################################################################
    import pymysql.cursors
    
    #Connect to SQL database with username and pw
    mydb = pymysql.connect(
        host='155.98.6.253',
        user='EddyFlux',
        passwd = 'UvTrhM_yFo71X2',
        database = 'CO2_Eddy'
        )
    
    #Set up cursor (allows navigation through SQL syntax)
    mycursor = mydb.cursor()
    
    return mycursor

#=========================================================================================================#

def get_LI_data(tablename,date1,date2):
    ######################################################################
    # Function to get necessary LI_8100 Data                             # 
    # from SQL. Input the SQL Tablename, and date range between which    #
    # data will be fetched. For one day's worth of data, enter the same  #
    # Date.                                                              #
    # Inputs:   tablename = name of SQL table to query, input as string  #
    #           date1 = start data for query, as string                  #
    #           date2 = end date for query, as string                    #
    ######################################################################
    import pandas as pd

    mycursor = sql_connect()
    mycursor.execute("SELECT Local_DT, EPOCH_TIME, Cdry\
                        FROM {}\
                        WHERE Local_DT >= '{} 00:00:00' AND Local_DT <= '{} 23:59:59.99'\
                        order by EPOCH_TIME asc;".format(tablename,date1,date2)) #SQL statement
    data = mycursor.fetchall() #fetch the data
    LI_vent = pd.DataFrame(list(data)) #convert imported data to dataframe
    LI_vent.columns = ['Local_DT','EPOCH_TIME','LI_CO2'] #name columns
    cols = LI_vent.columns.drop('Local_DT') #get all column names beside date column
    LI_vent[cols]=LI_vent[cols].apply(pd.to_numeric,errors='coerce') #change all but date to floats
    
    return LI_vent
#=========================================================================================================#
    
def get_multiplexer_data(tablename,date1,date2,split_or_concat,i):
    ######################################################################
    # Function to get exclusively "Spike Necessary" Multiplexer Data     # 
    # from SQL. Input the SQL Tablename, and date range between which    #
    # data will be fetched. For one day's worth of data, enter the same  #
    # Date.                                                              #
    ######################################################################
    
    import pandas as pd
    
    #Connect to SQL
    mycursor = sql_connect()   
    
    if split_or_concat == 'split':
        if i < 3:
            mycursor.execute("SELECT Local_DT,EPOCH_TIME,CO2_{},Location_Multi\
                        FROM {}\
                        WHERE Local_DT >= '{} 00:00:00' AND Local_DT <= '{} 23:59:59.99'\
                        order by EPOCH_TIME asc;".format(i,tablename,date1,date2)) #SQL query
            data = mycursor.fetchall() #fetch the data
            Multiplexer = pd.DataFrame(list(data)) #convert imported data into a dataframe
            Multiplexer.columns = ['Local_DT','EPOCH_TIME','CO2_{}'.format(i),'Multi_Loc'] #name columns
        elif i == 3:
            mycursor.execute("SELECT Local_DT,EPOCH_TIME,CO2_{},Rotations, Wind_Velocity,Wind_Direction,Temp,Location_Multi\
                        FROM {}\
                        WHERE Local_DT >= '{} 00:00:00' AND Local_DT <= '{} 23:59:59.99'\
                        order by EPOCH_TIME asc;".format(i,tablename,date1,date2)) #SQL query
            data = mycursor.fetchall() #fetch the data
            Multiplexer = pd.DataFrame(list(data)) #convert imported data into a dataframe
            Multiplexer.columns = ['Local_DT','EPOCH_TIME','CO2_{}'.format(i),'Rotations','Wind_Velocity','Wind_Direction','Temp','Multi_Loc'] #name columns
    elif split_or_concat == 'concat':
        mycursor.execute("SELECT *\
                    FROM {}\
                    WHERE Local_DT >= '{} 00:00:00' AND Local_DT <= '{} 23:59:59.99'\
                    order by EPOCH_TIME asc;".format(tablename,date1,date2)) #SQL query
        data = mycursor.fetchall() #fetch the data
        Multiplexer = pd.DataFrame(list(data)) #convert imported data into a dataframe
        Multiplexer.columns = ['Local_DT','EPOCH_TIME','CO2_1','CO2_2','CO2_3','Rotations','Wind_Velocity','Wind_Direction','Temp','Multi_loc'] #name columns
    else:
        raise ValueError('Input "split" or "concat" as the last argument')
        
    
    
    cols = Multiplexer.columns.drop('Local_DT') #get all column names but date column
    Multiplexer[cols]=Multiplexer[cols].apply(pd.to_numeric,errors='coerce') #change all but date to floats
    
    return Multiplexer
#=========================================================================================================#
    
def get_vent_anem_temp_data(tablename,date1,date2):
    ######################################################################
    # Function to get exclusively "Spike Necessary" Vent_Anem_Temp Data  # 
    # from SQL. Input the SQL Tablename, and date range between which    #
    # data will be fetched. For one day's worth of data, enter the same  #
    # Date.                                                              #
    ######################################################################
    import pandas as pd
   
    #Connect to SQL
    mycursor = sql_connect()
    mycursor.execute("SELECT *\
                    FROM {}\
                    WHERE Local_DT >= '{} 00:00:00' AND Local_DT <= '{} 23:59:59.99'\
                    order by EPOCH_TIME asc;".format(tablename,date1,date2)) #SQL query
    data = mycursor.fetchall() #fetch the data
    Vent_Anem_Temp = pd.DataFrame(list(data)) #convert imported data to a dataframe
    Vent_Anem_Temp.columns = ['Local_DT','EPOCH_TIME','Rotations','Velocity','Temp_1','Temp_2'] #name columns
    cols = Vent_Anem_Temp.columns.drop('Local_DT') #get all column names but date
    Vent_Anem_Temp[cols]=Vent_Anem_Temp[cols].apply(pd.to_numeric,errors='coerce') #change all but date to floats
    
    return Vent_Anem_Temp
#=========================================================================================================#
    
def get_wbb_weather(date1,date2):
    ######################################################################
    # Function to get WBB weather data                                   #
    ######################################################################
    import pandas as pd
   
    #Connect to SQL
    mycursor = sql_connect()
    mycursor.execute("SELECT Date_Time,air_temp_set_1,wind_speed_set_1,wind_direction_set_1,wind_cardinal_direction_set_1d\
                        FROM Aug2019_WBB_Weather\
                        WHERE Date_Time >= '{} 00:00:00' AND Date_Time <= '{} 23:59:59.99'\
                        ORDER BY Date_Time asc;".format(date1,date2))
    x = mycursor.fetchall()
    WBB_weather = pd.DataFrame(x)
    WBB_weather.columns = ['Corrected_DT','Temp','ws','wd','wcd']
    cols = WBB_weather.columns.drop(['Corrected_DT','wcd'])
    WBB_weather[cols]=WBB_weather[cols].apply(pd.to_numeric,errors='coerce')
    
    return WBB_weather
#=========================================================================================================#
    
def get_wbb_co2(date1,date2):
    ######################################################################
    # Function to get WBB weather data                                   #
    ######################################################################
    import pandas as pd
    mycursor = sql_connect()
    mycursor.execute("SELECT EPOCH_TIME, Local_DT, CO2d_ppm_cal, CH4d_ppm_cal\
                        FROM Aug2019_WBB_CO2\
                        WHERE Local_DT >= '{} 00:00:00' AND Local_DT <= '{} 23:59:59.99'\
                        ORDER BY EPOCH_TIME ASC;".format(date1,date2))
    x = mycursor.fetchall()
    WBB_CO2 = pd.DataFrame(x)
    WBB_CO2.columns = ['EPOCH_TIME','Corrected_DT','WBB_CO2','WBB_CH4']
    cols = WBB_CO2.columns.drop(['Corrected_DT'])
    WBB_CO2[cols]=WBB_CO2[cols].apply(pd.to_numeric,errors='coerce')
    
    return WBB_CO2
#=========================================================================================================#

def get_picarro_data(tablename,date1,date2,spikes_or_all,split_or_concat,i):
    import pandas as pd
    ###################################################################
    # Function to get exclusively "Spike Necessary" Picarro Data from #
    # SQL. Input the SQL Tablename, and date range between which data #
    # will be fetched. For one day's worth of data, enter the same    #
    # Date.                                                           #
    ###################################################################
    
    #Connect to SQL
    mycursor = sql_connect()
    if (spikes_or_all == 'spikes') & (split_or_concat == 'split'):
        raise KeyError("Cannot have spikes and split, as the spikes df only gets some wind information")
        
        
    if spikes_or_all == 'spikes':
        mycursor.execute("SELECT Local_DT, EPOCH_TIME, CO2_dry, ANEMOMETER_UY\
                        FROM {}\
                        WHERE Local_DT >= '{} 00:00:00' AND Local_DT <= '{} 23:59:59.99'\
                        order by EPOCH_TIME asc;".format(tablename,date1,date2)) #SQL statement
        data = mycursor.fetchall() #fetch the data
        Picarro = pd.DataFrame(list(data)) #convert data to a dataframe
        Picarro.columns = ['Local_DT','EPOCH_TIME','Pic_CO2','ANEM_Y'] #name columns
    elif spikes_or_all == 'all':
        if split_or_concat =='concat':
            mycursor.execute("SELECT Local_DT, EPOCH_TIME, CO2_dry, CH4_dry, ANEMOMETER_UY, ANEMOMETER_UX, ANEMOMETER_UZ, Location_Picarro\
                            FROM {}\
                            WHERE Local_DT >= '{} 00:00:00' AND Local_DT <= '{} 23:59:59.99'\
                            order by EPOCH_TIME asc;".format(tablename,date1,date2)) #SQL statement
            data = mycursor.fetchall() #fetch the data
            Picarro = pd.DataFrame(list(data)) #convert data to a dataframe
            Picarro.columns = ['Local_DT','EPOCH_TIME','Pic_CO2','Pic_CH4','ANEM_Y','ANEM_X','ANEM_Z','Pic_Loc'] #name columns
        elif split_or_concat == 'split':
            if i == 0:
                mycursor.execute("SELECT Local_DT, EPOCH_TIME, CO2_dry, CH4_dry, Location_Picarro\
                                FROM {}\
                                WHERE Local_DT >= '{} 00:00:00' AND Local_DT <= '{} 23:59:59.99'\
                                order by EPOCH_TIME asc;".format(tablename,date1,date2)) #SQL statement
                data = mycursor.fetchall() #fetch the data
                Picarro = pd.DataFrame(list(data)) #convert data to a dataframe
                Picarro.columns = ['Local_DT','EPOCH_TIME','Pic_CO2','Pic_CH4','Pic_Loc'] #name columns  
            else:
                mycursor.execute("SELECT Local_DT, EPOCH_TIME, ANEMOMETER_UY, ANEMOMETER_UX, ANEMOMETER_UZ, Location_Picarro\
                                FROM {}\
                                WHERE Local_DT >= '{} 00:00:00' AND Local_DT <= '{} 23:59:59.99'\
                                order by EPOCH_TIME asc;".format(tablename,date1,date2)) #SQL statement
                data = mycursor.fetchall() #fetch the data
                Picarro = pd.DataFrame(list(data)) #convert data to a dataframe
                Picarro.columns = ['Local_DT','EPOCH_TIME','ANEM_Y','ANEM_X','ANEM_Z','Pic_Loc'] #name columns
        else:
            raise KeyError('Input "split" or "concat"')
    else:
        raise ValueError('Input spikes or all as the last argument')
    cols = Picarro.columns.drop('Local_DT') #get all column names but date
    Picarro[cols]=Picarro[cols].apply(pd.to_numeric,errors='coerce') #change all but date to floats
    
    return Picarro

#=========================================================================================================#
    
def get_sql_data(LI_vent_sql_tablename,Multiplexer_sql_tablename,\
                 Vent_Anem_Temp_sql_tablename,Picarro_sql_tablename,date1,date2,spikes_or_all,split_or_concat):
    
    ######################################################################
    #Script pulls in all of the necessary data in the date range input into the function
    #Inputs: The names of each SQL table
    #        date1 - start date for range of data to pull
    #        date2 - end date for range of data to pull                    #
    ######################################################################

    import pandas as pd

    dict_of_dfs = {}
    #Import source (LI_8100_Vent) data
    #If there is a value error (no data in table for date range), set up an empty dataframe and pass the error
    print('Retrieving LI_vent data')
    try:
        dict_of_dfs['LI_Vent']=get_LI_data(LI_vent_sql_tablename,date1,date2)
    except ValueError:
        dict_of_dfs['LI_Vent'] = pd.DataFrame() #set empty dataframe
        pass
    
    
    #Import Multiplexer data
    #If there is a value error (no data in table for date range), set up an empty dataframe and pass the error
    print('Retrieving Multiplexer data')
    try:
        if split_or_concat == 'concat':
            dict_of_dfs['Multiplexer'] = get_multiplexer_data(Multiplexer_sql_tablename,date1,date2,split_or_concat,0)
        elif split_or_concat == 'split':
            for i in range(1,4):
                #if i < 4:
                dict_of_dfs['Multiplexer_CO2_{}'.format(i)] = get_multiplexer_data(Multiplexer_sql_tablename,date1,date2,split_or_concat,i)
                #else:
                 #   dict_of_dfs['Multiplexer_Weather'] = get_multiplexer_data(Multiplexer_sql_tablename,date1,date2,split_or_concat,i)
                
        else: 
            raise KeyError('Input "split" or "concat" as the last argument')
    except ValueError:
        dict_of_dfs['Multiplexer'] = pd.DataFrame() #make empty dataframe
        pass
    
    #Import Vent_Anem_Temp data
    #If there is a value error (no data in table for date range), set up an empty dataframe and pass the error
    print('Retrieving Vent_Anem_Temp data')
    try:
        dict_of_dfs['Vent_Anem_Temp'] = get_vent_anem_temp_data(Vent_Anem_Temp_sql_tablename,date1,date2)
    except ValueError:
        dict_of_dfs['Vent_Anem_Temp'] = pd.DataFrame() #make empty dataframe
        pass

    
    #Import Picarro data
    #If there is a value error (no data in table for date range), set up an empty dataframe and pass the error
    print('Retrieving Picarro data')
    try:
        if split_or_concat == 'concat':
            dict_of_dfs['Picarro'] = get_picarro_data(Picarro_sql_tablename,date1,date2,spikes_or_all,split_or_concat,0)
        if split_or_concat == 'split':
            for i in range(0,2):
                if i == 0 :
                    dict_of_dfs['Picarro_CO2'] = get_picarro_data(Picarro_sql_tablename,date1,date2,spikes_or_all,split_or_concat,i)
                else:
                    dict_of_dfs['Picarro_ANEM'] = get_picarro_data(Picarro_sql_tablename,date1,date2,spikes_or_all,split_or_concat,i)
    except ValueError:
        dict_of_dfs['Picarro'] = pd.DataFrame() #make empty dataframe
        pass
    
    #Import WBB_weather data
    #If there is a value error (no data in table for date range), set up an empty dataframe and pass the error
    print('Retrieving WBB Weather data')
    try:
        dict_of_dfs['WBB_Weather'] = get_wbb_weather(date1,date2)
    except ValueError:
        dict_of_dfs['WBB_Weather'] = pd.DataFrame() #make empty dataframe
        pass
    
    #Import WBB_CO2 data
    #If there is a value error (no data in table for date range), set up an empty dataframe and pass the error
    print('Retrieving WBB CO2 data')
    try:
        dict_of_dfs['WBB_CO2'] = get_wbb_co2(date1,date2)
    except ValueError:
        dict_of_dfs['WBB_CO2'] = pd.DataFrame() #make empty dataframe
        pass
    
    return dict_of_dfs#return all of the fetched dataframes
#=========================================================================================================#
    
def get_lag_groups(actual_spike_df,column):
    import pandas as pd
    import numpy as np
    
    spike_df = actual_spike_df[['Actual_DT','Actual_ET',column]].dropna()
    spike_df['lags'] = spike_df.apply(lambda row: row['Actual_ET']-row[column],axis=1)
    spike_df['diff'] = spike_df['Actual_ET'] - spike_df['Actual_ET'].shift(1)
    spike_df.reset_index(drop=True,inplace=True)
    
    grp = int(0)
    df_list = {}
    st_ix = 0 
    end_ix = 0
    for i in range(1,len(spike_df)):
        if spike_df.loc[i,'diff'] < 1000:
            end_ix += 1
        else:
            df_list[grp] = pd.DataFrame(spike_df.loc[st_ix:end_ix])
            grp+=1
            end_ix += 1
            st_ix = end_ix
    df_list[grp] = pd.DataFrame(spike_df.loc[st_ix:end_ix])
    

    ETs = []
    ave_lags = []
    for i in range(0,len(df_list)):
        ETs.append((df_list[i][column].iloc[0]+df_list[i][column].iloc[-1])/2)
        ave_lags.append(np.mean(df_list[i]['lags']))

    final_lags = pd.DataFrame({'mid_ET':ETs,'ave_lag':ave_lags})

    for i in range(0,len(final_lags)-1):
        final_lags.loc[i,'slope']= (final_lags.loc[i,'ave_lag']-final_lags.loc[i+1,'ave_lag'])/(final_lags.loc[i,'mid_ET']-final_lags.loc[i+1,'mid_ET'])
        
    return final_lags

#==============================================================================================================#
    
def df_correction_lag_slope(final_lags,df):
    ######################################################################
    # Correct the time drift of a dataframe using the grouped lag df     #
    ######################################################################
    
    import pandas as pd
    from datetime import datetime

    def row_correction(row,final_lags_df,grp):
        return row+final_lags_df['ave_lag'][grp]+(row-final_lags_df['mid_ET'][grp])*final_lags_df['slope'][grp]

    df_to_correct = df.copy()
    df_corr_list = {}
    df_corr_list[0] = df_to_correct.where((df_to_correct['EPOCH_TIME'] < final_lags.loc[1,'mid_ET'])).dropna()
    df_corr_list[0]['Corrected_ET'] = df_corr_list[0]['EPOCH_TIME'].apply(row_correction,args=(final_lags,0))
    df_corr_list[0]['Corrected_DT'] = df_corr_list[0]['Corrected_ET'].apply(lambda x: datetime.fromtimestamp(x))

    for i in range(1,len(final_lags)-1):
        df_corr_list[i] = df_to_correct.where((df_to_correct['EPOCH_TIME'] >= final_lags.loc[i,'mid_ET']) & (df_to_correct['EPOCH_TIME'] <= final_lags.loc[i+1,'mid_ET'])).dropna(how='all')
        df_corr_list[i]['Corrected_ET'] = df_corr_list[i]['EPOCH_TIME'].apply(row_correction,args=(final_lags,i))
        df_corr_list[i]['Corrected_DT'] = df_corr_list[i]['Corrected_ET'].apply(lambda x: datetime.fromtimestamp(x))

    corrected_df = pd.concat(df_corr_list)
    corrected_df.drop_duplicates(['EPOCH_TIME'],inplace=True)

    return corrected_df

#==============================================================================================================#
def drift_correct(dict_of_dfs):
    import pandas as pd
    from datetime import datetime
    
    print("Initializing Drift Correct")
    
    data = dict_of_dfs.copy()
    spikes = pd.read_pickle('Spike_ETs.pkl')
    for key in data:
        if data[key].empty:
            print("{} is empty - no correction needed".format(key))
            continue
        print('Correcting data for {}'.format(key))

        if (key == 'WBB_CO2')|(key=='WBB_Weather'):
            continue
        lags = get_lag_groups(spikes,key)
        data[key] = df_correction_lag_slope(lags,data[key])
    
    if 'Multiplexer_CO2_3' in data.keys():
        data['Multiplexer_Weather'] = data['Multiplexer_CO2_3'][['EPOCH_TIME','Local_DT','Rotations','Wind_Velocity','Wind_Direction','Corrected_ET']]
        data['Multiplexer_Weather']['Corrected_ET'] = data['Multiplexer_Weather'].apply(lambda row: row['Corrected_ET']-2,axis=1)
        data['Multiplexer_Weather']['Corrected_DT'] = data['Multiplexer_Weather']['Corrected_ET'].apply(lambda row: datetime.fromtimestamp(row))
        
        data['Multiplexer_CO2_3'].drop(['Rotations','Wind_Velocity','Wind_Direction'],axis=1,inplace=True)
    
    return data


#=========================================================================================================#
def download_and_save_daily(start_date,end_date):
    ######################################################################
    # Function to download and save as pickle all necessary data for a user input #
    # date range.                                                        #
    # Returns a dataframe with all variables concatenated, cleaned, and  #
    # drift corrected.                                                   #
    ######################################################################
    from datetime import timedelta, datetime
    import pickle
    
    def daterange(start_date, end_date):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        for n in range(int ((end_date - start_date).days)+1):
            yield start_date + timedelta(n)


    for single_date in daterange(start_date, end_date):
        data = get_sql_data("Aug2019_LI_8100_Vent",\
                  "Aug2019_Multiplexer","Aug2019_Vent_Anem_Temp",\
                  "Aug2019_Picarro",single_date,single_date,'all','split') #fetch data from four instruments between dates
        
        data = drift_correct(data) #correct drifts
        for key in data:
            data[key].reset_index(drop=True,inplace=True) #reset indecies (get added for some reason)
            
        print("Dumping data from {} to Data/{}.pickle".format(single_date,single_date))
        with open('Data/{}.pickle'.format(single_date), 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
            
    return

#=========================================================================================================#


download_and_save_daily('2019-10-15','2019-10-16')