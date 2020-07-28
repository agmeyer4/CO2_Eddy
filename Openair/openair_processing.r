library(openair)
library(lubridate)
library(ggplot2)
library(dplyr)
library(readr)
library(data.table)
library(gridExtra)

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

plot_prep1 <- function(df_list,pn,tower,wind_roll,low_ws,high_ws,m_dot_low,m_dot_high,omit){

  ws_label = paste0('ws_roll_',wind_roll)
  wd_label = paste0('wd_roll_',wind_roll)

  df_sub = add_wind_to_df(df_list[[tower]][[pn]],wind_roll,tower)
  if (omit==TRUE){
    df_sub = vent_on_only(df_sub)
  }
  df_sub = subset(df_sub,(df_sub$m_dot>=m_dot_low)&(df_sub$m_dot<=m_dot_high))
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

all_data = data.frame()




#for (i in (1:6)){
 
tower = "Picarro"
pn = 1
wind_roll = 0
ws_label = paste0('ws_roll_',wind_roll)
wd_label = paste0('wd_roll_',wind_roll)
df_sub1 = add_wind_to_df(dfs[[tower]][[pn]],wind_roll,tower)

time_lag = 1
df_sub = lag_wind_vars(df_sub1,time_lag)
ws_label = paste0('ws_roll_',wind_roll,'_lag_',time_lag)
wd_label = paste0('wd_roll_',wind_roll,'_lag_',time_lag)


m_dot_low =1
m_dot_high =18
df_sub = subset(df_sub,(df_sub$m_dot>m_dot_low)&(df_sub$m_dot<=m_dot_high))

high_ws = 15
low_ws = 2
df_sub = subset(df_sub,df_sub[[ws_label]]>low_ws & df_sub[[ws_label]]<high_ws)

excess_roll = 600
constituent = 'Pic_CO2'
stat = 'excess'
time_lag =0
percentile = 95

if (stat=='none'){
  pollutant = constituent
}else {
  pollutant = paste0(stat,'_r',excess_roll,'_',constituent)
}

names(df_sub)[names(df_sub)==wd_label] <-'wd'
names(df_sub)[names(df_sub)==ws_label] <-'ws'

perc = .3
rowint = as.integer(nrow(df_sub)*perc)
rand_df = df_sub[sample(nrow(df_sub),rowint),]

#plot_out = polarFreq(df_sub,pollutant = pollutant,statistic = 'max')
plot_out = polarPlot(rand_df,pollutant = pollutant,statistic = 'percentile',percentile = percentile)

x = plot_out[["data"]][["z"]]
max_prob = max(x[!is.na(x)])
maxid = which(x==max_prob)
u = plot_out[["data"]][["u"]][[maxid]]
v = plot_out[["data"]][["v"]][[maxid]]
ws = sqrt(u^2+v^2)
wd = add_360(atan2(v,u)/pi*180)
print(max_prob,ws,wd)





plot_out = cust_polarPlot(df_sub,pn,tower,constituent,stat,high_ws,low_ws,wind_roll,excess_roll,time_lag,percentile)


data = extract_plot_data(plot_out)

percentileRose(df_sub,pollutant = pollutant )

g1 = ggplot()+ geom_point(data = df_sub,aes(x=date,y=excess_r10_Pic_CH4),size=0.5)
g2 = ggplot()+ geom_point(data = df_sub,aes(x=date,y=m_dot),size=0.5)
grid.arrange(g1,g2,nrow=2)

















excess_to_total_comp <- function(poll_stat,plot_stat,pn){
  all_info = data.frame()
  
  tower = "Picarro"
  pn = pn
  wind_roll = 0
  ws_label = paste0('ws_roll_',wind_roll)
  wd_label = paste0('wd_roll_',wind_roll)
  df_sub1 = add_wind_to_df(dfs[[tower]][[pn]],wind_roll,tower)
  m_dot_low =-2
  m_dot_high =0
  
  
  while (m_dot_high<=12){
  

    df_sub = subset(df_sub1,(df_sub1$m_dot>m_dot_low)&(df_sub1$m_dot<=m_dot_high))
    
    high_ws = 20
    low_ws = 0
    df_sub = subset(df_sub,df_sub[[ws_label]]>low_ws & df_sub[[ws_label]]<high_ws)
    
    excess_roll = 600
    constituent = 'Pic_CO2'
    time_lag =0
    percentile = 95
    
    if (poll_stat=='none'){
      pollutant = constituent
    }else {
      pollutant = paste0(poll_stat,'_r',excess_roll,'_',constituent)
    }
    
    names(df_sub)[names(df_sub)==wd_label] <-'wd'
    names(df_sub)[names(df_sub)==ws_label] <-'ws'
    
    plot_out = polarPlot(df_sub,ws = 'ws',wd='wd',pollutant = pollutant,statistic = plot_stat,percentile = percentile)
    
    
    x = plot_out[["data"]][["z"]]
    max_perc = max(x[!is.na(x)])
    maxid = which(x==max_perc)
    u = plot_out[["data"]][["u"]][[maxid]]
    v = plot_out[["data"]][["v"]][[maxid]]
    ws = sqrt(u^2+v^2)
    wd = add_360(atan2(v,u)/pi*180)
    

    
    info = list()
    
    if (plot_stat == 'cpf'){
      st = plot_out[["plot"]][["sub"]]
      cpf = parse_number(substr(st,nchar(st)-5,nchar(st)))
      info$cpf=cpf
    }
    
    
    
    info$max_perc = max_perc
    info$ws = ws
    info$wd = wd
    info$min_mdot = m_dot_low
    info$max_mdot = m_dot_high
    
    all_info = rbind(all_info,info)
    m_dot_high = m_dot_high+2
    m_dot_low = m_dot_low+2
    
  }
  
  return(all_info)
  
}
