library(openair)
library(lubridate)
library(ggplot2)
library(dplyr)
library(readr)
library(data.table)
library(gridExtra)
library(grid)
library(latticeExtra)


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

retrieve_data <- function(){
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
  return(dfs)
}

plot_prep1 <- function(df_with_wind,basic_info){
  df_sub = lag_wind_vars(df_with_wind,basic_info$time_lag) #lag time
  basic_info$ws_label = paste0('ws_roll_',basic_info$wind_roll,'_lag_',basic_info$time_lag) 
  basic_info$wd_label = paste0('wd_roll_',basic_info$wind_roll,'_lag_',basic_info$time_lag)#Add wind
  
  #Random dropout *row precent
  rowint = as.integer(nrow(df_sub)*basic_info$row_perc)
  df_sub = df_sub[sample(nrow(df_sub),rowint),]

  #Reorder by date - rand dropout randomizes
  df_sub = df_sub[order(df_sub$Corrected_DT),]
  
  
  df_sub = subset(df_sub,(df_sub$m_dot>=basic_info$m_dot_low)&(df_sub$m_dot<=basic_info$m_dot_high)) #Addjust mass flow from vent bin
  df_sub = subset(df_sub,df_sub[[basic_info$ws_label]]>basic_info$low_ws & df_sub[[basic_info$ws_label]]<basic_info$high_ws)# Adjust wind speed
 #get pollutant name
   if (basic_info$stat=='none'){
    basic_info$pollutant = basic_info$constituent
  }else {
    basic_info$pollutant = paste0(basic_info$stat,'_r',basic_info$excess_roll,'_',basic_info$constituent)
  }
  names(df_sub)[names(df_sub)==basic_info$wd_label] <-'wd'
  names(df_sub)[names(df_sub)==basic_info$ws_label] <-'ws'
  

  res = list()
  res[[1]] = df_sub
  res[[2]] = basic_info
  
  return(res)
}


known_dir_line <- function(tower,pn){
  res = list()
  pic_theta = list(3.410933609,2.402871576,2.133658029,3.216301472,0.25971721,3.910745292)
  pic_x_text = list(-6.5,-7,-7,-6.7,11,-9)
  pic_y_text = list(-2.5,7,9.5,-1.2,3.7,-10)
  pic_text_angle = list(17,-42,-55,6,16,45)
  multi_theta = list(3.147460451,1.918607285,3.216301472)
  multi_x_text = list(-12,-6,-7.5)
  multi_y_text = list(-0.8,13,-1)
  multi_text_angle = list(2,-70,7)
  if (tower == 'Picarro'){
    theta = pic_theta[[pn]]
    res[['x_text']] = pic_x_text[[pn]]
    res[['y_text']] = pic_y_text[[pn]]
    res[['angle']]  = pic_text_angle[[pn]]
  }else if (tower == 'Multi'){
    theta = multi_theta[[pn]]
    res[['x_text']] = multi_x_text[[pn]]
    res[['y_text']] = multi_y_text[[pn]]
    res[['angle']]  = multi_text_angle[[pn]]
  }
  theta1 =  pi/2-theta
  res[['x_line']] = 30*sin(theta1)
  res[['y_line']] = 30*cos(theta1)
  return(res)
}



get_info <- function(plot_out,basic_info){
  info = list()
  x = plot_out[["data"]][["z"]]
  info$max_of_percentile = max(x[!is.na(x)])
  maxid = which(x==info$max_of_percentile)
  info$u_max_perc = plot_out[["data"]][["u"]][[maxid]]
  info$v_max_perc = plot_out[["data"]][["v"]][[maxid]]
  info$ws_max_perc = sqrt(info$u_max_perc^2+info$v_max_perc^2)
  info$wd_max_perc = add_360(atan2(info$v_max_perc,info$u_max_perc)/pi*180)
  info$basic_info = basic_info
  info$wd_diff = info$wd_max_perc - info$basic_info$known_wd
  
  return(info)
}


##==================================================================##
dfs = retrieve_data()
known_wd = list(195.4,137.7,122.2,184.3,14.9,224.1)



basic_info = list()
basic_info$tower = "Picarro"
basic_info$pn = 1
basic_info$wind_roll = 0
basic_info$ws_label = paste0('ws_roll_',basic_info$wind_roll)
basic_info$wd_label = paste0('wd_roll_',basic_info$wind_roll)
basic_info$known_wd = known_wd[[basic_info$pn]]

df_with_wind = add_wind_to_df(dfs[[basic_info$tower]][[basic_info$pn]],basic_info$wind_roll,basic_info$tower)

#Plot before random dropout and filters
g1=ggplot()+ geom_point(data = df_with_wind,aes(x=date,y=Pic_CO2),size=0.5)
g2=ggplot()+ geom_point(data = df_with_wind,aes_string(x='date',y=basic_info$wd_label),size=0.5)
g3 =ggplot()+ geom_point(data = df_with_wind,aes(x=date,y=m_dot),size=0.5)
grid.arrange(g1,g2,g3,nrow=3)

basic_info$m_dot_low =0
basic_info$m_dot_high =20
basic_info$high_ws = 20
basic_info$low_ws = 0
basic_info$excess_roll = 600
basic_info$constituent = 'Pic_CO2'
basic_info$stat = 'excess'
basic_info$time_lag =0
basic_info$percentile = 95
basic_info$row_perc = .1

plot_def = plot_prep1(df_with_wind,basic_info)
basic_info = plot_def[[2]]
basic_info$rows = nrow(plot_def[[1]])


#Plot after random dropout and filters
g1=ggplot()+ geom_point(data = plot_def[[1]],aes_string(x='date',y=basic_info$pollutant),size=0.5)
g2=ggplot()+ geom_point(data = plot_def[[1]],aes(x=date,y=wd),size=0.5)
g3 =ggplot()+ geom_point(data = plot_def[[1]],aes(x=date,y=m_dot),size=0.5)
grid.arrange(g1,g2,g3,nrow=3)



title = paste0(basic_info$tower," Position ",basic_info$pn, " with ",basic_info$m_dot_low," < Vent_M > ",basic_info$m_dot_high, "g/s CO2")
footer = paste0("ppm ",basic_info$pollutant)
header = '95th Percentile \nConcentration'
plot_out = polarPlot(plot_def[[1]],pollutant = basic_info$pollutant,
                     statistic = 'percentile',percentile = basic_info$percentile,cols = 'viridis'
                     ,main =title,par.settings=list(fontsize=list(text=20)),
                     key = list(header=header,footer=footer),angle.scale = 45
                     )

source_dir = known_dir_line(basic_info$tower,basic_info$pn)
trellis.last.object() + layer(lsegments(0, 0, source_dir$x_line, source_dir$y_line, lty = 5,
                                        type = 'l',col='red',lwd = 2))

get_info(plot_out,basic_info)












plot_out = polarFreq(plot_def[[1]],pollutant = 'Pic_CO2',statistic = 'mean',
                     main =title,key.footer =footer,min.bin = 2,key = list(fit='all'))
percentileRose(plot_def[[1]],pollutant = 'Pic_CO2')




pic_size = list()
for (i in list(1,4,6)){
  pic_size[[i]] = size_relationship('Picarro',i,'Pic_CO2')
}



multi_size = list()
for (i in (1:3)){
  multi_size[[i]] = size_relationship('Multi',i,'CO2_3')
}


size_relationship <- function(tower, pn, constituent){

  basic_info = list()
  all_info = list()

  basic_info$tower = tower
  basic_info$pn =pn
  basic_info$wind_roll = 0
  basic_info$ws_label = paste0('ws_roll_',basic_info$wind_roll)
  basic_info$wd_label = paste0('wd_roll_',basic_info$wind_roll)
  df_with_wind = add_wind_to_df(dfs[[basic_info$tower]][[basic_info$pn]],basic_info$wind_roll,basic_info$tower)
  
  basic_info$high_ws = 20
  basic_info$low_ws = 2
  basic_info$excess_roll = 600
  basic_info$constituent = constituent
  basic_info$stat = 'excess'
  basic_info$time_lag =0
  basic_info$percentile = 95
  basic_info$row_perc = 1
  
  basic_info$m_dot_low =-2
  basic_info$m_dot_high =0
  i = 1
  while (basic_info$m_dot_high<14){
    if (basic_info$m_dot_high>9){
      basic_info$m_dot_high = 20
    }
    plot_def = plot_prep1(df_with_wind,basic_info)
    basic_info = plot_def[[2]]
    basic_info$rows = nrow(plot_def[[1]])
    title = paste0(tower," Position ",basic_info$pn, " with ",basic_info$m_dot_low," < Vent_M > ",basic_info$m_dot_high, "g/s CO2")
    footer = paste0("ppm ",basic_info$pollutant)
    
    plot_out = polarPlot(plot_def[[1]],pollutant = basic_info$pollutant,
                         statistic = 'percentile',percentile = basic_info$percentile,cols = 'viridis'
                         ,main =title,key.footer =footer)
    info = get_info(plot_out,basic_info)
    all_info[[i]]=info
    basic_info$m_dot_high = basic_info$m_dot_high+2
    basic_info$m_dot_low = basic_info$m_dot_low +2
    i = i+1
  }

  res = list()
  res[['allinfo']] = all_info
  res[['mass_table']] = data.frame()
  for (i in 1:length(all_info)){
    mass_table = list()
    mass_table$m_dot_low = all_info[[i]]$basic_info$m_dot_low
    mass_table$m_dot_high = all_info[[i]]$basic_info$m_dot_high
    mass_table$max_of_perc = all_info[[i]]$max_of_perc
    mass_table$ws_max_perc = all_info[[i]]$ws_max_perc
    mass_table$wd_max_perc = all_info[[i]]$wd_max_perc
    mass_table$rows = all_info[[i]]$basic_info$rows
    res[['mass_table']] = rbind(res[['mass_table']],mass_table)
  }
  
   
  return(res)

}



detectability <- function(){
  
  basic_info = list()
  all_info = list()
  res = data.frame(stringsAsFactors = FALSE)
  
  for (tower in list('Picarro')){
    basic_info$tower = tower
    if (tower =='Picarro'){
      pn_list = list(1,2,3,4,5,6)
    }else if (tower == 'Multi'){
      pn_list = list(1,2,3)
    }
    for (pn in pn_list){
      basic_info$pn =pn
      basic_info$wind_roll = 0
      basic_info$ws_label = paste0('ws_roll_',basic_info$wind_roll)
      basic_info$wd_label = paste0('wd_roll_',basic_info$wind_roll)
      df_with_wind = add_wind_to_df(dfs[[basic_info$tower]][[basic_info$pn]],basic_info$wind_roll,basic_info$tower)
      
      
      basic_info$time_lag = 0
      basic_info$high_ws = 20
      basic_info$low_ws = 2
      basic_info$excess_roll = 600
      
      if (tower == 'Picarro'){
        constituent_list = list('Pic_CH4')
      }else if (tower == 'Multi'){
        constituent_list = list('CO2_1','CO2_2','CO2_3')
      }
      
      for (constituent in constituent_list){
        print(constituent)
        basic_info$constituent = constituent
        basic_info$stat = 'excess'
        basic_info$time_lag =0
        basic_info$percentile = 95
        basic_info$row_perc = 1
        
        basic_info$m_dot_low =1
        basic_info$m_dot_high =20
        i = 1
        
        plot_def = plot_prep1(df_with_wind,basic_info)
        basic_info = plot_def[[2]]
        basic_info$rows = nrow(plot_def[[1]])
        title = paste0(tower," Position ",basic_info$pn, " with ",basic_info$m_dot_low," < Vent_M > ",basic_info$m_dot_high, "g/s CO2")
        footer = paste0("ppm ",basic_info$pollutant)
        
        plot_out = polarPlot(plot_def[[1]],pollutant = basic_info$pollutant,
                             statistic = 'percentile',percentile = basic_info$percentile,cols = 'viridis'
                             ,main =title,key.footer =footer)
        info = get_info(plot_out,basic_info)
        print(info$basic_info$constituent)

        detection = list()
        detection$tower = info$basic_info$tower
        detection$pn = info$basic_info$pn
        detection$constituent = info$basic_info$constituent
        print(info$basic_info$tower)
        detection$max_of_perc = info$max_of_perc
        detection$ws_max_perc = info$ws_max_perc
        detection$wd_max_perc = info$wd_max_perc
        detection$rows = info$basic_info$rows
        res = rbind(res,detection,stringsAsFactors = FALSE)
      
      }
    }
  }
  
  return(res)
  
}








    

