#Aaron Meyer
#April, 2020
#  This script takes data from the folder '../CO2_Data_final' and processes then stores in '../CO2_Data_Processed'
#  The data stored in '../CO2_Data_Final' is deposited by running the 'SQL_download.py' script in this folder
#   Specifically, this script splits all data into Vent, Multi, Picarro, and WBB folders so we can get specific sets independently

# Import packages
import pickle
import CO2_Dataset_Preparation
import CO2_functions
import CO2_Processing
from CO2_Dataset_Preparation import *
from CO2_functions import * 
from CO2_Processing import *
import pandas as pd
import sys
import os

old_folder = '../CO2_Data_Final'
new_folder = '../CO2_Data_Processed'

print(os.listdir())

if not os.path.isdir(old_folder):
    sys.exit('Error: Data folder does not exist. Retry with valid folder containing daily data')

os.mkdir(new_folder)
os.mkdir(f'{new_folder}/Vent')
os.mkdir(f'{new_folder}/Multi')
os.mkdir(f'{new_folder}/Picarro')
os.mkdir(f'{new_folder}/WBB_Weather')
os.mkdir(f'{new_folder}/WBB_CO2')    

data = [] #Setup a list of the data for each picarro position
for i in range(1,7):
    d = Dataset(old_folder,i,logfile = None) #Use the Dataset class to retrieve data (from 'CO2_Dataset_Preparation.py')
    d._preprocess() #Preprocess (from 'CO2_Dataset_Preparation.py')
    data.append(d) # Append to list

#Store all vent data in its own folder
vent_data_all = data[0].data['Vent_Mass'].drop('DOW',axis=1) #Setup the dataframe for vent
for i in range(1,len(data)):
    vent_data_all = pd.concat([vent_data_all,data[i].data['Vent_Mass'].drop('DOW',axis=1)]) #Append all data 
vent_data_all = vent_data_all.loc[~vent_data_all.index.duplicated(keep='first')] #Delete any duplicate indicies
for date in daterange('2019-08-15','2019-11-27'): #Store each as it's own day 
    v = vent_data_all.loc[(vent_data_all.index>=f'{date} 00:00:00.00')&(vent_data_all.index<f'{date} 23:59:59.99')] #One day
    file_name =f'{new_folder}/Vent/{date}' #setup filename with date
    with open('{}.pkl'.format(file_name), 'wb') as file:  #store
        pickle.dump(v, file)

#Store multi data according to position number 
pn=1 #position number 
multi = data[0].data['Multi'] #setup the dataframe
multi['Multi_Loc'] = pn #set the pn to the correcte number
multi = multi.drop('DOW',axis=1) #Drop day of week
multi = multi[['CO2_1','CO2_2','CO2_3','Temp','Rotations','Wind_Velocity','Wind_Direction','Multi_Loc']] #reorder cols
multi = multi.loc[~multi.index.duplicated(keep='first')]#drop duplicate indicies
for date in daterange('2019-08-15','2019-08-21'): #Store data by day 
    m = multi.loc[(multi.index>=f'{date} 00:00:00.00')&(multi.index<f'{date} 23:59:59.99')]
    file_name =f'{new_folder}/Multi/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(m, file)

pn=0 #set pn0 for days where multi was turned off
for date in daterange('2019-08-22','2019-08-28'): #store empty dataframe for this
    m = multi.loc[(multi.index>=f'{date} 00:00:00.00')&(multi.index<f'{date} 23:59:59.99')]
    file_name =f'{new_folder}/Multi/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(m, file)

pn=2 #position number 2
multi1 = data[1].data['Multi']
multi1['Multi_Loc'] = pn
multi1 = multi1.drop('DOW',axis=1)
multi1 = multi1[['CO2_1','CO2_2','CO2_3','Temp','Rotations','Wind_Velocity','Wind_Direction','Multi_Loc']]
multi2 = data[2].data['Multi']
multi2['Multi_Loc'] = pn
multi2 = multi2.drop('DOW',axis=1)
multi2 = multi2[['CO2_1','CO2_2','CO2_3','Temp','Rotations','Wind_Velocity','Wind_Direction','Multi_Loc']]
multi = pd.concat([multi1,multi2])
multi = multi.loc[~multi.index.duplicated(keep='first')]
for date in daterange('2019-08-29','2019-09-19'):
    m = multi.loc[(multi.index>=f'{date} 00:00:00.00')&(multi.index<f'{date} 23:59:59.99')]
    file_name =f'{new_folder}/Multi/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(m, file)
        
pn=0
for date in daterange('2019-09-20','2019-09-29'):
    m = multi.loc[(multi.index>=f'{date} 00:00:00.00')&(multi.index<f'{date} 23:59:59.99')]
    file_name =f'{new_folder}/Multi/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(m, file)

pn=3
multi = data[3].data['Multi']
multi['Multi_Loc'] = pn
multi = multi.drop('DOW',axis=1)
multi = multi[['CO2_1','CO2_2','CO2_3','Temp','Rotations','Wind_Velocity','Wind_Direction','Multi_Loc']]
multi = multi.loc[~multi.index.duplicated(keep='first')]
for date in daterange('2019-09-30','2019-10-03'):
    m = multi.loc[(multi.index>=f'{date} 00:00:00.00')&(multi.index<f'{date} 23:59:59.99')]
    file_name =f'{new_folder}/Multi/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(m, file)
        
pn=0
for date in daterange('2019-10-04','2019-10-21'):
    m = multi.loc[(multi.index>=f'{date} 00:00:00.00')&(multi.index<f'{date} 23:59:59.99')]
    file_name =f'{new_folder}/Multi/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(m, file)
        
pn=1
multi = data[4].data['Multi']
multi['Multi_Loc'] = pn
multi = multi.drop('DOW',axis=1)
multi = multi[['CO2_1','CO2_2','CO2_3','Temp','Rotations','Wind_Velocity','Wind_Direction','Multi_Loc']]
multi = multi.loc[~multi.index.duplicated(keep='first')]
for date in daterange('2019-10-22','2019-10-30'):
    m = multi.loc[(multi.index>=f'{date} 00:00:00.00')&(multi.index<f'{date} 23:59:59.99')]
    file_name =f'{new_folder}/Multi/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(m, file)
        
pn=0
for date in daterange('2019-10-31','2019-11-05'):
    m = multi.loc[(multi.index>=f'{date} 00:00:00.00')&(multi.index<f'{date} 23:59:59.99')]
    file_name =f'{new_folder}/Multi/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(m, file)
        
pn=1
multi = data[5].data['Multi']
multi['Multi_Loc'] = pn
multi = multi.drop('DOW',axis=1)
multi = multi[['CO2_1','CO2_2','CO2_3','Temp','Rotations','Wind_Velocity','Wind_Direction','Multi_Loc']]
multi = multi.loc[~multi.index.duplicated(keep='first')]
for date in daterange('2019-11-06','2019-11-27'):
    m = multi.loc[(multi.index>=f'{date} 00:00:00.00')&(multi.index<f'{date} 23:59:59.99')]
    file_name =f'{new_folder}/Multi/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(m, file)
        
pn = 1
pic  = data[0].data['Picarro']
pic['Pic_Loc'] = pn
pic = pic.drop('DOW',axis=1)
for date in daterange('2019-08-15','2019-08-21'):
    p = pic.loc[(pic.index>=f'{date} 00:00:00.00')&(pic.index<f'{date} 23:59:59.99')]
    file_name =f'{new_folder}/Picarro/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(p, file)

pn=0
for date in daterange('2019-08-22','2019-08-27'):
    p = pic.loc[(pic.index>=f'{date} 00:00:00.00')&(pic.index<f'{date} 23:59:59.99')]
    file_name =f'{new_folder}/Picarro/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(p, file)
        
pn = 2
pic =data[1].data['Picarro']
pic = pic.loc[pic.index<'2019-09-12 13:00:00']
pic['Pic_Loc'] = pn
pic = pic.drop('DOW',axis=1)
for date in daterange('2019-08-28','2019-09-12'):
    p = pic.loc[(pic.index>=f'{date} 00:00:00.00')&(pic.index<f'{date} 23:59:59.99')]
    file_name =f'{new_folder}/Picarro/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(p, file)
        
pn = 3
pic =data[2].data['Picarro']
pic = pic.loc[(pic.index>'2019-09-12 17:00:00')&(pic.index<'2019-09-23 12:00:00')]
pic['Pic_Loc'] = pn
pic = pic.drop('DOW',axis=1)
for date in daterange('2019-09-12','2019-09-23'):
    p = pic.loc[(pic.index>=f'{date} 00:00:00.00')&(pic.index<f'{date} 23:59:59.99')]
    file_name =f'{new_folder}/Picarro/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(p, file)
        
pn = 4
pic =data[3].data['Picarro']
pic['Pic_Loc'] = pn
pic = pic.drop('DOW',axis=1)
for date in daterange('2019-09-24','2019-10-03'):
    p = pic.loc[(pic.index>=f'{date} 00:00:00.00')&(pic.index<f'{date} 23:59:59.99')]
    file_name =f'{new_folder}/Picarro/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(p, file)
        
pn=0
for date in daterange('2019-10-04','2019-10-15'):
    p = pic.loc[(pic.index>=f'{date} 00:00:00.00')&(pic.index<f'{date} 23:59:59.99')]
    file_name =f'{new_folder}/Picarro/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(p, file)
        
pn = 5
pic =data[4].data['Picarro']
pic['Pic_Loc'] = pn
pic = pic.drop('DOW',axis=1)
for date in daterange('2019-10-16','2019-11-04'):
    p = pic.loc[(pic.index>=f'{date} 00:00:00.00')&(pic.index<f'{date} 23:59:59.99')]
    file_name =f'{new_folder}/Picarro/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(p, file)

pn = 6
pic =data[5].data['Picarro']
pic['Pic_Loc'] = pn
pic = pic.drop('DOW',axis=1)
for date in daterange('2019-11-05','2019-11-27'):
    p = pic.loc[(pic.index>=f'{date} 00:00:00.00')&(pic.index<f'{date} 23:59:59.99')]
    file_name =f'{new_folder}/Picarro/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(p, file)
        
d = Dataset(old_folder,'all',logfile = None)
d._preprocess()
d.data['WBB_Weather'].set_index('Corrected_DT',inplace=True)
for date in daterange('2019-08-15','2019-11-27'):
    w = d.data['WBB_Weather'].loc[(d.data['WBB_Weather'].index>=f'{date} 00:00:00.00')&(d.data['WBB_Weather'].index<f'{date} 23:59:59.99')]
    file_name=f'{new_folder}/WBB_Weather/{date}'
    with open('{}.pkl'.format(file_name),'wb') as file:
        pickle.dump(w,file)
        
d.data['WBB_CO2'].set_index('Corrected_DT',inplace=True)
for date in daterange('2019-08-15','2019-11-27'):
    w = d.data['WBB_CO2'].loc[(d.data['WBB_CO2'].index>=f'{date} 00:00:00.00')&(d.data['WBB_CO2'].index<f'{date} 23:59:59.99')]
    file_name=f'{new_folder}/WBB_CO2/{date}'
    with open('{}.pkl'.format(file_name),'wb') as file:
        pickle.dump(w,file)