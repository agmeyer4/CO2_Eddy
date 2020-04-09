library(openair)
path = '../../CO2_Data_Processed/R_Dataframes/'

filename = 'test2.Rdat'
pic2=read.csv(paste0(path,filename))
pic2$date<-as.POSIXct(pic2$X)

filename = 'test.Rdat'
pic6=read.csv(paste0(path,filename))
pic6$date<-as.POSIXct(pic6$X)

df = pic2

windroll = 60
time_lag = 45
poll_roll =10
poll_const = 'Pic_CH4'
poll_stat = 'excess'

pollutant = paste0(poll_stat,'_r',poll_roll,'_',poll_const)
ws = paste0('X',windroll,'_ws.t.',time_lag,'.')
wd = paste0('X',windroll,'_wd.t.',time_lag,'.')

df_sub = subset(df,ws>2&ws<10) 
polarPlot(df_sub,pollutant=pollutant,ws=ws,wd=wd,statistic='cpf',percentile=90)



df_ave <- timeAverage(df,avg.time = "min")
df_ave_sub <- subset(df_ave,ws>1&ws<10)

polarPlot(df_ave,pollutant='Pic_CH4',ws='ws.t.20.',wd='wd.t.20.',statistic='cpf',percentile=90)

dev.off()
