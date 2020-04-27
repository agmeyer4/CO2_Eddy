#library(reticulate)
#path_to_python <- "/uufs/chpc.utah.edu/common/home/u0890904/software/pkg/miniconda3/envs/CO2_Eddy/bin/python"
#use_python(path_to_python)
#sys = import("sys")
#test_package <- import("CO2_Dataset_Preparation")
#use_virtualenv("/uufs/chpc.utah.edu/common/home/u0890904/software/pkg/miniconda3/envs/CO2_Eddy")
#py_run_file("~/CO2_Eddy/openair_prep.py")
#os<-import("os")
#os$listdir(".")
##======================================================================================================
create_plot_calls <- function(tower,pn,excess_roll,poll_const,poll_stat,time_lag,wind_roll,low_ws,high_ws,percentile){
  if (poll_stat == 'none'){
    pollutant = poll_const
  }else{
    pollutant = paste0(poll_stat,'_r',excess_roll,'_',poll_const)
  }
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
  if (tower == 'WBB'){
    ws = paste0('ws.t.',time_lag,'.')
    wd = paste0('wd.t.',time_lag,'.')
  }
  
  info = paste0('tower_',tower,'_pn_',pn,'_timelag_',time_lag,'_windroll_',wind_roll,'_highws_',high_ws,'_lowws_',low_ws,'_percentile',percentile)
  namelist = list("pollutant"=pollutant,"ws"=ws,"wd"=wd,"info"=info)
  return(namelist)
}
###+===========================
extract_plot_data <- function(index,OA_data){
  x = OA_data[["data"]][["z"]]
  max_prob = max(x[!is.na(x)])
  maxid = which(x==max_prob)
  u = OA_data[["data"]][["u"]][[maxid]]
  v = OA_data[["data"]][["v"]][[maxid]]
  ws = sqrt(u^2+v^2)
  wd = atan2(v,u)/pi*180
  
  st = OA_data[["plot"]][["sub"]]
  cpf = as.numeric(substr(st,nchar(st)-4,nchar(st)-1))
  
  details = index
  
  d <- data.frame( cpf =cpf,
                  max_prob=max_prob,u=u,
                  v = v,ws = ws,
                  wd = wd,details= details)  
  return(d)
}




###=========================================================================================
library(openair)
setwd('~/CO2_Eddy/Openair/')
path = '../../CO2_Data_Processed/R_Dataframes/'
dfs = list()

pic_dfs <- list()
for (i in 1:2){
  filename = paste0('Picarro_',i,'.csv')
  pic_dfs[[i]]<-read.csv(paste0(path,filename))
}

dfs[["Picarro"]] = pic_dfs
rm(pic_dfs)

multi_dfs <- list()
for (i in 1:3){
  filename = paste0('Multi_',i,'.csv')
  multi_dfs[[i]]<-read.csv(paste0(path,filename))
}

wbb_dfs <- list()
for (i in 1:1){
  filename = paste0('WBB_',i,'.csv')
  wbb_dfs[[i]]<-read.csv(paste0(path,filename))
}

dfs[["WBB"]] = wbb_dfs
dfs[["Multi"]] = multi_dfs
rm(wbb_dfs)
rm(multi_dfs)


plot_data = list()


pn = 2
tower = 'Picarro'
poll_const = 'Pic_CH4'
poll_stat = 'excess'
low_ws = 2
high_ws = 10
wind_roll = 10
excess_roll = 10
time_lag = 10
percentile = 90
df_sub <- subset(dfs[[tower]][[pn]],ws>low_ws&ws<high_ws) 
plot_builder_index = create_plot_calls(tower,pn,excess_roll,poll_const,
                                       poll_stat,time_lag,wind_roll,
                                       low_ws,high_ws,percentile)
plot_data <- extract_plot_data(plot_builder_index,
             polarPlot(df_sub,pollutant=plot_builder_index$pollutant,
                        ws=plot_builder_index$ws,wd=plot_builder_index$wd,statistic = 'cpf',
                        percentile=percentile,key.header=plot_builder_index$info)
             )
plot_data[[pn]] <- data.frame(lag_time=numeric(0), 
                cpf =numeric(0),
                max_prob=numeric(0),
                u = numeric(0),
                v = numeric(0),
                ws = numeric(0),
                wd = numeric(0),
                details= character(0))
for (t in c(1,3,5,10,15,20,25,30,35,40,45,50,55,60,90,120)){
  plot_builder_index = create_plot_calls(tower,pn,excess_roll,poll_const,poll_stat,t,wind_roll,low_ws,high_ws,percentile)
  plot_data_t = extract_plot_data(plot_builder_index,
                                  polarPlot(df_sub,pollutant=plot_builder_index$pollutant,
                                  ws=plot_builder_index$ws,wd=plot_builder_index$wd,statistic = 'cpf',
                                  percentile=percentile,key.header=plot_builder_index$info)
  )
  #plot_data_t$time_lag = t
  #plot_data[[pn]] = rbind(plot_data[[pn]],plot_data_t)
}



ggplot()+
  geom_point(data = plot_data[[1]],aes(x=time_lag,y=ws),color="red")+
  geom_point(data = plot_data[[2]],aes(x=time_lag,y=ws),color="blue")

