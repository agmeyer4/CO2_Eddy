#library(reticulate)
#path_to_python <- "/uufs/chpc.utah.edu/common/home/u0890904/software/pkg/miniconda3/envs/CO2_Eddy/bin/python"
#use_python(path_to_python)
#sys = import("sys")
#test_package <- import("CO2_Dataset_Preparation")
#use_virtualenv("/uufs/chpc.utah.edu/common/home/u0890904/software/pkg/miniconda3/envs/CO2_Eddy")
#py_run_file("~/CO2_Eddy/openair_prep.py")
#os<-import("os")
#os$listdir(".")

library(openair)
setwd('~/CO2_Eddy/Openair/')

pn=3

path = '../../CO2_Data_Processed/R_Dataframes/'
filename = paste0('pic_',pn,'.csv')
df=read.csv(paste0(path,filename))

tower = 'Picarro'
excess_rolls <- c(1,10,60,600,3600)
poll_const = 'Pic_CH4'
poll_stat = 'excess'
time_lags <- c(0,5,10,15,20,30,45,60,80,120)
wind_rolls = c(1,5,10,30,60,600,3600)
low_ws = 2
high_ws = 10

for (excess_roll in excess_rolls){
  for (time_lag in time_lags){
    for (wind_roll in wind_rolls){
      

      
      pollutant = paste0(poll_stat,'_r',excess_roll,'_',poll_const)
      if (tower == 'Multi'){
        ws = paste0('ws.t.',time_lag,'.')
        wd = paste0('wd.t.',time_lag,'.')
      }
      if (tower == 'Picarro'){
        if (wind_roll ==0){
          ws=paste0('ws.t.',time_lag,'.')
          wd=paste0('wd.t.',time_lag,'.')
        }
        else {
          if (time_lag == 0){
            ws = paste0('roll_',wind_roll,'_ws')
            wd = paste0('roll_',wind_roll,'_wd')
          }
          else{
            ws = paste0('roll_',wind_roll,'_ws.t.',time_lag,'.')
            wd = paste0('roll_',wind_roll,'_wd.t.',time_lag,'.')
          }
        }
      }
      df_sub = subset(pic_3,ws>low_ws&ws<high_ws) 
      info = paste0('tower_',tower,'_pn_',pn,'_timelag_',time_lag,'_windroll_',wind_roll,'_highws_',high_ws,'_lowws_',low_ws)
      polarPlot(df_sub,pollutant=pollutant,ws=ws,wd=wd,statistic='cpf',percentile=90,key.header=info)

    }
  }
}