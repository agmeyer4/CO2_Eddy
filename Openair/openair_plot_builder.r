library(openair)

library(reticulate)

path_to_python <- "/uufs/chpc.utah.edu/common/home/u0890904/software/pkg/miniconda3/envs/CO2_Eddy/bin/python"
use_python(path_to_python)

sys = import("sys")

c <- import("CO2_Dataset_Preparation")

use_virtualenv("/uufs/chpc.utah.edu/common/home/u0890904/software/pkg/miniconda3/envs/CO2_Eddy")

py_run_file("~/CO2_Eddy/openair_prep.py")

os<-import("os")
os$listdir(".")




path = '../../CO2_Data_Processed/R_Dataframes/'
filename = 'test.csv'
df=read.csv(paste0(path,filename))


tower = 'Picarro'
time_lag = 60
poll_roll =60
poll_const = 'Pic_CH4'
poll_stat = 'excess'
wind_roll = 10
low_ws = 2
high_ws = 15
pollutant = paste0(poll_stat,'_r',poll_roll,'_',poll_const)
if (tower == 'Multi'){
  ws = paste0('ws.t.',time_lag,'.')
  wd = paste0('wd.t.',time_lag,'.')
}
if (tower == 'Picarro'){
  ws = paste0('roll_',wind_roll,'_ws.t.',time_lag,'.')
  wd = paste0('roll_',wind_roll,'_wd.t.',time_lag,'.')
}

df_sub = subset(df,ws>low_ws&ws<high_ws) 

polarPlot(df_sub,pollutant=pollutant,ws=ws,wd=wd,statistic='cpf',percentile=90,cols = "plasma")

dev.off()
