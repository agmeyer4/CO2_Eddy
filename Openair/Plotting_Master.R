library(ggplot2)
library(grid)
library(openair)
library(latticeExtra)

basic_info = list()
basic_info$tower = "Picarro"
basic_info$pn = 6
basic_info$wind_roll = 0
basic_info$ws_label = paste0('ws_roll_',basic_info$wind_roll)
basic_info$wd_label = paste0('wd_roll_',basic_info$wind_roll)
df_with_wind = add_wind_to_df(dfs[[basic_info$tower]][[basic_info$pn]],basic_info$wind_roll,basic_info$tower)
basic_info$m_dot_low =1
basic_info$m_dot_high =20
basic_info$high_ws = 20
basic_info$low_ws = 2
basic_info$excess_roll = 600
basic_info$constituent = 'Pic_CH4'
basic_info$stat = 'excess'
basic_info$time_lag =0
basic_info$percentile = 95
basic_info$row_perc = 1
plot_def = plot_prep1(df_with_wind,basic_info)
df = plot_def[[1]]
basic_info = plot_def[[2]]
basic_info$rows = nrow(plot_def[[1]])
if (basic_info$stat=='none'){
  lab1 = 'Raw'
  lab2 = ''}else{
  lab1='Excess'
  lab2= 'Excess'}
title = paste0('      EC Station ',basic_info$pn)
footer = paste0('ppm ',lab2,' CH4')
header = '95th Percentile'
plot_out = polarPlot(plot_def[[1]],pollutant = basic_info$pollutant,
                     statistic = 'percentile',percentile = basic_info$percentile,cols = 'viridis'
                     ,main = title,par.settings=list(fontsize=list(text=22),font ='Times New Roman'),
                     key = list(header=' ',footer=' ',draw = TRUE),angle.scale = 45
)
source_dir = known_dir_line(basic_info$tower,basic_info$pn)
trellis.last.object() + layer(lsegments(0, 0, source_dir$x_line, source_dir$y_line, lty = 5,
                                        type = 'l',col='red',lwd = 2))
trellis.last.object() + layer(ltext(source_dir$x_text,source_dir$y_text,gp = gpar(fontface = 'bold'), "Source",col = 'red', 
                                    cex = 0.8,srt = source_dir$angle))
trellis.focus("legend", side="right", clipp.off=TRUE, highlight=FALSE)
grid.text(header, 0.2, 1, hjust=0.1, vjust=1,gp = gpar(fontsize = 18))
grid.text(footer, 0.2, 0, hjust=0.1, vjust=-.5,gp = gpar(fontsize = 18))
trellis.unfocus()







trellis.last.object() + layer(ltext(-7.5, -1,gp = gpar(fontface = 'bold'), "Source",col = 'red', 
                                    cex = 0.8,srt = 7))



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






















##Histogram 
ggplot(df,aes(x=Pic_CO2))+geom_histogram(bins = 40)+
  labs(x = 'CO2 Concentration (ppm)')+labs(y = 'Count')+
  scale_y_continuous(labels = function (x) format(x,scientific=TRUE))+
  xlim(400,600)+
  theme(axis.title.x = element_text(size = rel(1.5)))+
  theme(axis.title.y = element_text(size = rel(1.5)))+
  theme(axis.text.x = element_text(size = rel(1.5)))+
  theme(axis.text.y = element_text(size = rel(1.5)))
  
