from CO2_Dataset_Preparation import *
from ML_Model_Master import *
from datetime import datetime

position_number = 4
feature_columns = ['Pic_CO2','ANEM_X','ANEM_Y','ANEM_Z','wd','ws']
downsample_sec = 1
periods_to_lag = [120]
tower = 'Picarro'
train_percent = 0.7

activation = 'relu'
neurons = [128]
dropout_rate = [0.2]
learn_rate = [0.001,1e-4,1e-5]
decay = [1e-5,1e-6]
batch_size = [10,20,50,100]
epochs = [10,50,100]

file_name = 'ML_Models/PN{}_Lag{}_Neur{}_DR{}'.format(position_number,periods_to_lag[0],neurons[0],dropout_rate[0])
logfile=open('{}.txt'.format(file_name),'w')

now = datetime.now()
dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
print('*******************************START TIME = {}************************************'.format(dt_string),flush=True)
logfile.write('*******************************START TIME = {}************************************\n'.format(dt_string))

print("-------------------------BEGIN: GRIDSEARCH TESTING-------------------------")
logfile.write("-------------------------BEGIN: GRIDSEARCH TESTING-------------------------\n")
print("-------------------------PREPROCESSSING-------------------------")
logfile.write("-------------------------PREPROCESSSING-------------------------\n")
logfile.flush()

data = Dataset('../CO2_Data_Final',position_number)
data._preprocess()

print("-------------------------BUILD AND TRAIN MODELS-------------------------")
logfile.write("-------------------------BUILD AND TRAIN MODELS-------------------------\n")

tot_train = len(periods_to_lag)*len(neurons)*len(dropout_rate)*len(learn_rate)*len(decay)*len(batch_size)*len(epochs)-1

models = []
i = 0

for lag in periods_to_lag:
    ml_data = ML_Data(feature_columns,downsample_sec,lag,tower,train_percent)
    ml_data._ML_Process(data)
    for neur in neurons:
        for dr in dropout_rate:
            for lr in learn_rate:
                for dec in decay:
                    for bs in batch_size:
                        for ep in epochs:
                            print(f"---Training Model: {i} of {tot_train}---")
                            logfile.write(f"---Training Model: {i} of {tot_train}---\n")
                            logfile.flush()
                            ml_model = ML_Model_Builder(activation,neur,dr,lr,dec,bs,ep)
                            ml_model._train_model(ml_data)
                            models.append(ml_model)
                            i+=1
       
    
error_name  = 'rmse'   

error_vals = []
for m in models:
    error_vals.append(m.history.history[error_name][-1])
best_idx = error_vals.index(min(error_vals))

print("-------------------------RESULTS-------------------------")
logfile.write("-------------------------RESULTS-------------------------\n")

print(f"Best score for '{error_name}' was {min(error_vals)} in model {best_idx}")
logfile.write(f"Best score for '{error_name}' was {min(error_vals)} in model {best_idx}\n")

print(f"Downsampling Seconds: {models[best_idx].downsample_sec}\n\
Lag Periods: {models[best_idx].periods_to_lag}\n\
Activation: {models[best_idx].activation}\n\
Neurons: {models[best_idx].neurons}\n\
Learning Rate: {models[best_idx].learn_rate}\n\
Decay: {models[best_idx].decay}\n\
Epochs: {models[best_idx].epochs}")
logfile.write(f"Downsampling Seconds: {models[best_idx].downsample_sec}\n\
Lag Periods: {models[best_idx].periods_to_lag}\n\
Activation: {models[best_idx].activation}\n\
Neurons: {models[best_idx].neurons}\n\
Learning Rate: {models[best_idx].learn_rate}\n\
Decay: {models[best_idx].decay}\n\
Epochs: {models[best_idx].epochs}\n")
logfile.flush()

print("-------------------------SAVE FILE-------------------------")
logfile.write("-------------------------SAVE FILE-------------------------\n")
import pickle
with open('{}.pkl'.format(file_name), 'wb') as models_file:
     pickle.dump(models, models_file)

print(f"Saved list of models to {file_name}")
logfile.write(f"Saved list of models to {file_name}\n")
print(f"Models built with optimizer: {models[best_idx].opt_string}")
logfile.write(f"Models built with optimizer: {models[best_idx].opt_string}\n")

now = datetime.now()
dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
print('*******************************END TIME = {}************************************'.format(dt_string),flush=True)
logfile.write('*******************************END TIME = {}************************************\n'.format(dt_string))
logfile.flush()
