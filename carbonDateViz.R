setwd(getwd())
library(ggplot2)
library(readr)

datasetStatuses <- read_csv("~/ws-dl/CarbonDateViz/dataset-new2.csv", col_types = cols(status_code = col_integer()))

ggplot(datasetStatuses, aes(x = as.factor(datasetStatuses$status_code), fill = as.factor(datasetStatuses$status_code) )) + geom_bar() + scale_fill_brewer(palette = "Set1") + labs(x = "Status Codes", y = "Count") + geom_text(stat='count',aes(label=..count..),vjust=-0.25) + guides(fill=guide_legend(title="Dataset Status Codes"))

# ggplot(studentInfo, aes(x=as.factor(cyl) )) + geom_bar()

