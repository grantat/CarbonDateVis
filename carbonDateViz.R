setwd(getwd())
library(ggplot2)
library(readr)

datasetStatuses <- read_csv("./data/dataset-new2.csv", col_types = cols(status_code = col_integer()))

ggplot(datasetStatuses, aes(x = as.factor(datasetStatuses$status_code), fill = as.factor(datasetStatuses$status_code) )) + geom_bar() + scale_fill_brewer(palette = "Set1") + labs(x = "Status Codes", y = "Count") + geom_text(stat='count',aes(label=..count..),vjust=-0.25) + guides(fill=guide_legend(title="Dataset Status Codes"))

# ggplot(studentInfo, aes(x=as.factor(cyl) )) + geom_bar()

cd_stats <- read_csv("./data/cd-stats.csv")
# remove URI
cd_stats$URI <- NULL

getStats <- function(data){
  # create vectors
  tv = c()
  fv = c()
  dcols = colnames(data)
  # iterate through column names
  for(i in dcols){
    # find stats here
    isFalse = sum(data[[i]] == 'False')
    isTrue = sum(data[[i]] == 'True')
    print(i)
    print(isFalse)
    print(isTrue)
    tv <- c(tv, isTrue)
    fv <- c(fv, isFalse)
  }
  # rearrange true first then add false to single vector
  tv <- c(tv, fv)
  return(tv)
}

# create a dataset
specie=c(rep("True" , 9) , rep("False" , 9) )
condition1 = rep(colnames(cd_stats), 2)
vals = getStats(cd_stats)
print(vals)
data=data.frame(specie,condition1,vals)


# ggplot(cd_stats, aes(x= as.factor(cd_stats), fill= as.factor(cd_stats$`Estimated Creation Date`) )) + geom_bar()  + guides(fill=guide_legend(title="CarbonDate found a Date"))

# Faceting
ggplot(data, aes(y=vals, x=specie, color=specie, fill=specie) ) +
  geom_bar( stat="identity") +
  facet_wrap(~condition1) +
  labs(x = "Date Found (T/F)", y = "Count") +
  theme(legend.title=element_text("test"))

# ===============================
# CD dates

cdDates <- read_csv("./cd-dataset-merge-fixed.csv")
cdDates <- cdDates[!is.na(cdDates$`Estimated Creation Date`),]
cdDates <- cdDates[order(cdDates$`Actual Age`),]

overEstimated <- subset(cdDates, cdDates$`Estimated Age` > cdDates$`Actual Age`)

xaxis <- sum(complete.cases(cdDates$`Estimated Creation Date`))
services <- colnames(cdDates)[6:14]

for(j in services){
  print(j)
  print(sum(!is.na(cdDates[j])))
  # grep(i, colnames(cdDates))
  # print()
}

# count each
for(i in 1:xaxis){
  # estDate <-
  for(i in services){
    grep(i, colnames(cdDates))
    # print()
  }
}

temp <- c()
for(i in 1:xaxis){
  temp <- c(temp, i)
}

plot(temp, cdDates$`Actual Age`,
     xlab="Resource", ylab="Actual Age",
     xlim=c(0, 1000), ylim=c(0, 10000))
plot(temp, cdDates$`Estimated Age`,
     xlab="Resource", ylab="Estimated Age",
     xlim=c(0, 1000), ylim=c(0, 10000))

fit2 <- lm(temp ~ poly(cdDates$`Actual Age`, 2, raw=TRUE))
plot(xaxis, cdDates$`Actual Age`)
lines(xaxis, predict(fit2, data.frame(x=cdDates$`Actual Age`), col='red'))

# Plots of both estimated and actual ages on the same graph. Red is actual. Blue is estimated.
# Polynomial curve of degree 2 for both sets of data.
ggplot(data = cdDates, aes(y=cdDates$`Actual Age`, x=temp)) +
  xlab("Resources") +
  ylab("Age") +
  geom_point(alpha = 1, aes(colour='Real Creation Dates'), size=0.9, shape=19) +
  stat_smooth(method = "lm", formula = y ~ poly(x,2), aes(colour='Poly fitted Real Creation Dates')) +
  geom_point(aes(x=temp, y=cdDates$`Estimated Age`, colour='Estimated Creation Dates'), data=cdDates, size=0.5) +
  stat_smooth(method = "lm",aes(x=temp,y=cdDates$`Estimated Age`, colour='Poly fitted Best Estimated Dates'), formula = y ~ poly(x,2)) +
  theme(legend.title=element_blank(), legend.position = c(0.225, 0.825)) +
  scale_color_manual(name="", values=c("Real Creation Dates"="blue","Poly fitted Real Creation Dates"="blue","Estimated Creation Dates"="red","Poly fitted Best Estimated Dates"="red")) +
  guides(fill = guide_legend(override.aes = list(linetype = 0, shape=''))
         , colour = guide_legend(override.aes = list(linetype=c(0,1,1,0)
                                                     , shape=c(16,NA,NA,16))))

# print(sum(is.na(cdDates$`Estimated Creation Date`)))

library(zoo)

x <- 1:10
y <- 3*x+25
id <- order(x)

AUC <- sum(diff(xaxis)*rollmean(cdDates$`Estimated Age`,2))
