library(ggplot2)
library(grid)
library(openair)
library(latticeExtra)

basic_info = list()
basic_info$tower = "Picarro"
basic_info$pn = 2
basic_info$wind_roll = 0
basic_info$ws_label = paste0('ws_roll_',basic_info$wind_roll)
basic_info$wd_label = paste0('wd_roll_',basic_info$wind_roll)
df_with_wind = add_wind_to_df(dfs[[basic_info$tower]][[basic_info$pn]],basic_info$wind_roll,basic_info$tower)
basic_info$m_dot_low =1
basic_info$m_dot_high =20
basic_info$high_ws = 20
basic_info$low_ws = 2
basic_info$excess_roll = 600
basic_info$constituent = 'Pic_CO2'
basic_info$stat = 'excess'
basic_info$time_lag =0
basic_info$percentile = 95
basic_info$row_perc = 1
basic_info$dropout_type = 'sequential'


plot_def = plot_prep1(df_with_wind,basic_info)
df = plot_def[[1]]
basic_info = plot_def[[2]]
basic_info$rows = nrow(plot_def[[1]])

if (basic_info$stat=='none'){
  lab1 = 'Raw'
  lab2 = ''}else{
  lab1='Excess'
  lab2= 'Excess'}
if (basic_info$constituent == 'Pic_CH4'){
  lab3 = ' CH4'}else{
  lab3 = ' CO2'
}

if (basic_info$tower=='Picarro'){
  title = paste0('      EC Station ',basic_info$pn)
}else if (basic_info$tower=='Multi'){
  title = paste0('      Multi Station ',basic_info$pn)
}

footer = paste0('ppm ',lab2,lab3)
header = '95th Percentile'
plot_out = polarPlot(plot_def[[1]],pollutant = basic_info$pollutant,
                     statistic = 'percentile',percentile = basic_info$percentile,cols = 'viridis'
                     ,main = title,par.settings=list(fontsize=list(text=22),font ='Times New Roman'),
                     key = list(header=' ',footer=' ',draw = TRUE),angle.scale = 45,
)

trellis.focus("legend", side="right", clipp.off=TRUE, highlight=FALSE)
grid.text(header, 0.2, 1, hjust=0.1, vjust=1,gp = gpar(fontsize = 18))
grid.text(footer, 0.2, 0, hjust=0.1, vjust=-.5,gp = gpar(fontsize = 18))
trellis.unfocus()

source_dir = known_dir_line(basic_info$tower,basic_info$pn)
trellis.last.object() + layer(lsegments(0, 0, source_dir$x_line, source_dir$y_line, lty = 5,
                                        type = 'l',col='red',lwd = 2))
trellis.last.object() + layer(ltext(source_dir$x_text,source_dir$y_text,gp = gpar(fontface = 'bold'), "Source",col = 'red',
                                    cex = 0.8,srt = source_dir$angle))



get_info(plot_out,basic_info)




title = paste0('      CBPF EC Station ',basic_info$pn)
footer = paste0('ppm ',lab2,lab3)
header = 'CPF Probability'
plot_out = polarPlot(plot_def[[1]],pollutant = basic_info$pollutant,
                     statistic = 'cpf',percentile = c(85,95),cols = 'viridis'
                     ,main = title,par.settings=list(fontsize=list(text=22),font ='Times New Roman'),
                     key = list(header=' ',footer=' ',draw = TRUE),angle.scale = -135
)

trellis.focus("legend", side="right", clipp.off=TRUE, highlight=FALSE)
grid.text(header, 0.2, 1, hjust=0.1, vjust=1,gp = gpar(fontsize = 18))
grid.text(footer, 0.2, 0, hjust=0.1, vjust=-.5,gp = gpar(fontsize = 18))
trellis.unfocus()



windRose(plot_def[[1]],main = paste0('EC Tower ',basic_info$pn,' Wind Rose'),key.position = 'right',par.settings=list(fontsize=list(text=20)))
polarFreq(plot_def[[1]],pollutant = basic_info$pollutant,main = 'EC Tower 6 Wind Rose',key.position = 'right',par.settings=list(fontsize=list(text=20)))



#Histogram
ggplot(df,aes(x=Pic_CO2))+geom_histogram(bins = 40)+
  labs(x = 'CO2 Concentration (ppm)')+labs(y = 'Count')+
  scale_y_continuous(labels = function (x) format(x,scientific=TRUE))+
  xlim(400,600)+
  theme(axis.title.x = element_text(size = rel(1.5)))+
  theme(axis.title.y = element_text(size = rel(1.5)))+
  theme(axis.text.x = element_text(size = rel(1.5)))+
  theme(axis.text.y = element_text(size = rel(1.5)))