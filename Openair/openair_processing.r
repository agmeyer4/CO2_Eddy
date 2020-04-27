library(openair)
library(lubridate)
library(ggplot2)
library(dplyr)
library(readr)
library(data.table)
setwd('~/CO2_Eddy/Openair/')
path = '../../CO2_Data_Processed/R_Dataframes/'

##=====================WIND FUNCTIONS=============================##
add_360 <- function(angle){
  if(is.na(angle)){
    result=NA
  }
  else if(angle<0){
    result = angle+360
  }
  else{
    result=angle
  }
  return(result)
}
twod_wind_dir <- function(x,y,pos_num){
  if(is.na(pos_num)){
    result = NA
  }
  else if (pos_num == 5){
    result = add_360(90-atan2(y,x)/pi*180)
  }
  else{
    result = add_360(-90-atan2(y,x)/pi*180)
  }
  return(result)
}
ws_calc <- function(x,y){
  return(sqrt(x^2+y^2))
}
add_wind_to_df <- function(df_orig,roll,tower){
  print(paste0("adding ws, wd with ",roll," rolling average"))
  if (tower=='Multi'){
    df_orig[['ws_roll_0']] = df_orig[['ws']]
    df_orig[['wd_roll_0']] = df_orig[['wd']]
    return(df_orig)
  }
  
  if (roll == 0){
    df_orig[['ws_roll_0']] = mapply(ws_calc,df_orig$ANEM_X,df_orig$ANEM_Y)
    df_orig[['wd_roll_0']] = mapply(twod_wind_dir,df_orig$ANEM_X,df_orig$ANEM_Y,df_orig$Pic_Loc)
  }
  else{
    rollx = rollingMean(df_orig,pollutant='ANEM_X',width = roll,new.name = 'roll')[['roll']]
    rolly = rollingMean(df_orig,pollutant='ANEM_Y',width = roll,new.name = 'roll')[['roll']]
    df_orig[[paste0('ws_roll_',roll)]]=mapply(ws_calc,rollx,rolly)
    df_orig[[paste0('wd_roll_',roll)]]=mapply(twod_wind_dir,rollx,rolly,df_orig$Pic_Loc)
    
  }
  return(df_orig)
}

lag_wind_vars <- function(df_orig,lag_periods){
  print(paste0("lagging wind variables ", lag_periods," periods"))
  cols = names(df_orig)[grepl('ws|wd',names(df_orig))]
  for (col in cols){
    df_orig[[paste0(col,'_lag_',lag_periods)]] = lag(df_orig[[col]],n=lag_periods)
  }
  return(df_orig)
}

vent_on_only <- function(df_orig){
  print("omitting data when vent is off")
  df = na.omit(df_orig,col='m_dot')
  df = df[df$m_dot>0,]
  return(df)
}

plot_prep1 <- function(df_list,pn,tower,wind_roll,low_ws,high_ws){
  ws_label = paste0('ws_roll_',wind_roll)
  wd_label = paste0('wd_roll_',wind_roll)

  df_sub = add_wind_to_df(df_list[[tower]][[pn]],wind_roll,tower)


  df_sub = subset(df_sub,df_sub[[ws_label]]>low_ws & df_sub[[ws_label]]<high_ws)
  return(df_sub)
}

extract_plot_data <- function(OA_data){
  x = OA_data[["data"]][["z"]]
  max_prob = max(x[!is.na(x)])
  maxid = which(x==max_prob)
  u = OA_data[["data"]][["u"]][[maxid]]
  v = OA_data[["data"]][["v"]][[maxid]]
  ws = sqrt(u^2+v^2)
  wd = add_360(atan2(v,u)/pi*180)
  
  st = OA_data[["plot"]][["sub"]]
  cpf = parse_number(substr(st,nchar(st)-5,nchar(st)))
  
  d <- data.frame( cpf =cpf,
                   max_prob=max_prob,u=u,
                   v = v,ws = ws,
                   wd = wd)  
  return(d)
}


cust_polarPlot <- function(df,pn,tower,constituent,stat,high_ws,low_ws,wind_roll,excess_roll,time_lag,percentile){
  df = lag_wind_vars(df,time_lag)
  #if (tower == 'Picarro'){
    if (stat=='none'){
      pollutant = constituent
    }
    else {
      pollutant = paste0(stat,'_r',excess_roll,'_',constituent)
    }
  #}
  #else if (tower == 'Multi'){
  #  pollutant = constituent
  #  print('here')
  #}
  ws_label = paste0('ws_roll_',wind_roll,'_lag_',time_lag)
  wd_label = paste0('wd_roll_',wind_roll,'_lag_',time_lag)
  
  plot_out = polarPlot(df,pollutant = pollutant,x=ws_label,wd=wd_label,statistic='cpf',percentile=percentile
                       ,units = "")
                       # ,key = list(header="Conditional Probability",footer = "Excess CO2 Concentration",height = 1,
                       #            space = "left",labels = list(cex = 1.5)))
  
  return(plot_out)
}
##==================================================================##
dfs = list()
pic_dfs <- list()
for (i in 1:6){
  filename = paste0('Picarro_',i,'_excess.csv')
  pic_dfs[[i]]<-read.csv(paste0(path,filename))
  pic_dfs[[i]]$date = as.POSIXct(pic_dfs[[i]]$Corrected_DT)
}
dfs[["Picarro"]] = pic_dfs
rm(pic_dfs)


multi_dfs <- list()
for (i in 1:3){
  filename = paste0('Multi_',i,'_excess.csv')
  multi_dfs[[i]]<-read.csv(paste0(path,filename))
  multi_dfs[[i]]$date = as.POSIXct(multi_dfs[[i]]$Corrected_DT)
}
dfs[["Multi"]] = multi_dfs
rm(multi_dfs)





tower = "Multi"
pn = 2
high_ws = 15
low_ws = 2
wind_roll = 0
plot_df = plot_prep1(dfs,pn,tower,wind_roll,low_ws,high_ws)


excess_roll = 10
constituent = 'CO2_1'
stat = 'excess'
time_lag =0
percentile = 90
plot_out = cust_polarPlot(plot_df,pn,tower,constituent,stat,high_ws,low_ws,wind_roll,excess_roll,time_lag,percentile)









ggplot()+
  geom_line(data = df,aes(x=date,y=ws_roll_10),color="red")+
  geom_line(data = df,aes(x=date,y=ws_roll_1000),color="blue")
