import pickle
import CO2_Dataset_Preparation
import CO2_functions
import CO2_Processing
from CO2_Dataset_Preparation import *
from CO2_functions import * 
from CO2_Processing import *
import pandas as pd
data = []
for i in range(1,7):
    d = Dataset('../CO2_Data_Final',i,logfile = None)
    d._preprocess()
    data.append(d)
vent_data_all = data[0].data['Vent_Mass'].drop('DOW',axis=1)
for i in range(1,len(data)):
    vent_data_all = pd.concat([vent_data_all,data[i].data['Vent_Mass'].drop('DOW',axis=1)])
vent_data_all = vent_data_all.loc[~vent_data_all.index.duplicated(keep='first')]
for date in daterange('2019-08-15','2019-11-27'):
    v = vent_data_all.loc[(vent_data_all.index>=f'{date} 00:00:00.00')&(vent_data_all.index<f'{date} 23:59:59.99')]
    file_name =f'../CO2_Data_Processed/Vent/{date}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(v, file)
        
pn=1
multi = data[0].data['Multi']
multi['Multi_Loc'] = pn
multi = multi.drop('DOW',axis=1)
multi = multi[['CO2_1','CO2_2','CO2_3','Temp','Rotations','Wind_Velocity','Wind_Direction','Multi_Loc']]
multi = multi.loc[~multi.index.duplicated(keep='first')]
for date in daterange('2019-08-15','2019-08-21'):
    m = multi.loc[(multi.index>=f'{date} 00:00:00.00')&(multi.index<f'{date} 23:59:59.99')]
    file_name =f'../CO2_Data_Processed/Multi/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(m, file)

pn=0
for date in daterange('2019-08-22','2019-08-28'):
    m = multi.loc[(multi.index>=f'{date} 00:00:00.00')&(multi.index<f'{date} 23:59:59.99')]
    file_name =f'../CO2_Data_Processed/Multi/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(m, file)

pn=2
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
    file_name =f'../CO2_Data_Processed/Multi/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(m, file)
        
pn=0
for date in daterange('2019-09-20','2019-09-29'):
    m = multi.loc[(multi.index>=f'{date} 00:00:00.00')&(multi.index<f'{date} 23:59:59.99')]
    file_name =f'../CO2_Data_Processed/Multi/{date}_PN{pn}'
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
    file_name =f'../CO2_Data_Processed/Multi/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(m, file)
        
pn=0
for date in daterange('2019-10-04','2019-10-21'):
    m = multi.loc[(multi.index>=f'{date} 00:00:00.00')&(multi.index<f'{date} 23:59:59.99')]
    file_name =f'../CO2_Data_Processed/Multi/{date}_PN{pn}'
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
    file_name =f'../CO2_Data_Processed/Multi/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(m, file)
        
pn=0
for date in daterange('2019-10-31','2019-11-05'):
    m = multi.loc[(multi.index>=f'{date} 00:00:00.00')&(multi.index<f'{date} 23:59:59.99')]
    file_name =f'../CO2_Data_Processed/Multi/{date}_PN{pn}'
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
    file_name =f'../CO2_Data_Processed/Multi/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(m, file)
        
pn = 1
pic  = data[0].data['Picarro']
pic['Pic_Loc'] = pn
pic = pic.drop('DOW',axis=1)
for date in daterange('2019-08-15','2019-08-21'):
    p = pic.loc[(pic.index>=f'{date} 00:00:00.00')&(pic.index<f'{date} 23:59:59.99')]
    file_name =f'../CO2_Data_Processed/Picarro/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(p, file)

pn=0
for date in daterange('2019-08-22','2019-08-27'):
    p = pic.loc[(pic.index>=f'{date} 00:00:00.00')&(pic.index<f'{date} 23:59:59.99')]
    file_name =f'../CO2_Data_Processed/Picarro/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(p, file)
        
pn = 2
pic =data[1].data['Picarro']
pic = pic.loc[pic.index<'2019-09-12 13:00:00']
pic['Pic_Loc'] = pn
pic = pic.drop('DOW',axis=1)
for date in daterange('2019-08-28','2019-09-12'):
    p = pic.loc[(pic.index>=f'{date} 00:00:00.00')&(pic.index<f'{date} 23:59:59.99')]
    file_name =f'../CO2_Data_Processed/Picarro/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(p, file)
        
pn = 3
pic =data[2].data['Picarro']
pic = pic.loc[(pic.index>'2019-09-12 17:00:00')&(pic.index<'2019-09-23 12:00:00')]
pic['Pic_Loc'] = pn
pic = pic.drop('DOW',axis=1)
for date in daterange('2019-09-12','2019-09-23'):
    p = pic.loc[(pic.index>=f'{date} 00:00:00.00')&(pic.index<f'{date} 23:59:59.99')]
    file_name =f'../CO2_Data_Processed/Picarro/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(p, file)
        
pn = 4
pic =data[3].data['Picarro']
pic['Pic_Loc'] = pn
pic = pic.drop('DOW',axis=1)
for date in daterange('2019-09-24','2019-10-03'):
    p = pic.loc[(pic.index>=f'{date} 00:00:00.00')&(pic.index<f'{date} 23:59:59.99')]
    file_name =f'../CO2_Data_Processed/Picarro/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(p, file)
        
pn=0
for date in daterange('2019-10-04','2019-10-15'):
    p = pic.loc[(pic.index>=f'{date} 00:00:00.00')&(pic.index<f'{date} 23:59:59.99')]
    file_name =f'../CO2_Data_Processed/Picarro/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(p, file)
        
pn = 5
pic =data[4].data['Picarro']
pic['Pic_Loc'] = pn
pic = pic.drop('DOW',axis=1)
for date in daterange('2019-10-16','2019-11-04'):
    p = pic.loc[(pic.index>=f'{date} 00:00:00.00')&(pic.index<f'{date} 23:59:59.99')]
    file_name =f'../CO2_Data_Processed/Picarro/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(p, file)
        
pn = 6
pic =data[5].data['Picarro']
pic['Pic_Loc'] = pn
pic = pic.drop('DOW',axis=1)
for date in daterange('2019-11-05','2019-11-27'):
    p = pic.loc[(pic.index>=f'{date} 00:00:00.00')&(pic.index<f'{date} 23:59:59.99')]
    file_name =f'../CO2_Data_Processed/Picarro/{date}_PN{pn}'
    with open('{}.pkl'.format(file_name), 'wb') as file:
        pickle.dump(p, file)