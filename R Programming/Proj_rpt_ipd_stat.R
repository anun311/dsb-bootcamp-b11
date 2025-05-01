# 1. Import Excel Files ####
library(readxl)
ipd <- read_excel('RefFiles/ipd-202410-202411.xlsx', sheet = 1)
dtype <- read_excel('RefFiles/ipd-202410-202411.xlsx', sheet = 2)
beds <- read_excel('RefFiles/ipd-202410-202411.xlsx', sheet = 3)

ipd
dtype
beds

# 2. Exploratory data analysis ####
# a. Data structure
str(ipd)
head(ipd)
tail(ipd)
summary(ipd)

# b. Missing value
sum(is.na(ipd))
table(is.na(ipd))

## missing ของแต่ละ cols
apply(ipd, 2, function(x) any(is.na(x)))
## missing ของแต่ละ col มีจำนวนเท่าไหร่
colSums(is.na(ipd))


# 3. Data preparetion ####

# c. Transform data type
ipd$ward <- as.character(ipd$ward)
ipd$dchtype <- as.character(ipd$dchtype)
dtype$dchtype <- as.character(dtype$dchtype)
beds$ward <- as.character(beds$ward)


# a. manage missing data
## dchtype ที่หายไปต้องการแทนที่ด้วย 5
ipd$dchtype[is.na(ipd$dchtype)] <- 5

## missing ของแต่ละ col มีจำนวนเท่าไหร่
colSums(is.na(ipd))

# b. transform data
## Calc LoS: Length of Stay
a = ipd$admit_date[0:1]
b = ipd$dis_date[0:1]

difftime(b, a, units = 'days')


# transform data
## Calc LoS: Length of Stay
ipd$los <- as.integer(difftime(ipd$dis_date, ipd$admit_date, units = "days"))
ipd$los[ipd$los == 0] <- 1 # replace 0 -> 1
ipd

# Make MonthID
ipd$month_id <- as.character(format.Date(ipd$dis_date, format = '%Y-%m'))
ipd


# join data ipd + dtype
library(dplyr)
ipd <- left_join(ipd, dtype, by='dchtype')

# rename colName
names(ipd)[names(ipd) == "name"] <- "dchtype_nm"
ipd


df_count <- ipd %>%
  select(dchtype_nm, id) %>% 
  group_by(dchtype_nm) %>%  
  summarise(cnt_ = n_distinct(id))
df_count

library(ggplot2)

ggplot(df_count, aes(x = dchtype_nm, y = cnt_)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  labs(title = "จำนวนผู้ป่วยตามประเภทการจำหน่าย",
       x = "ประเภทการจำหน่าย", y = "จำนวนผู้ป่วย") +
  theme_minimal()

# "จำนวนผู้ป่วยทั้งหมดที่รับไว้ในหอผู้ป่วยในเดือนนี้เป็นเท่าใด? เพิ่มขึ้นหรือลดลงเมื่อเทียบกับเดือนที่แล้ว?"
# c. Select Data & Make data set

## histogram
hist(ipd$los)
hist(ipd$cost)

## boxplot
boxplot(ipd$los)
boxplot(ipd$cost)

ward_stat <- ipd %>%
  select(id, ward, month_id, dchtype_nm, los, cost) %>%
  group_by(ward, month_id) %>%
  summarise(
    cnt_pt = n_distinct(id),
    sum_los = sum(los),
    sum_cost = sum(cost),
    mean_los = mean(los),
    mean_cost = mean(cost),
    mead_los = median(los),
    mead_cost = median(cost))
ward_stat

# join data ward_stat + beds
ward_stat <- left_join(ward_stat, beds, by='ward')

# df บอกว่าแต่ละเดือนมีกี่วัน
mday <- data.frame(
  month_id = c('2024-10', '2024-11'), 
  days = c(31, 30)
)

# join data ward_stat + mday
ward_stat <- left_join(ward_stat, mday, by='month_id')
ward_stat


# calc อัตราการครองเตียง
# (ผลรวมจำนวนวันนอนของผู้ป่วยใน x 100 ) / (จำนวนเตียงของโรงพยาบาล x(จำนวนวันในเดือนนั้น)))
ward_stat <- ward_stat %>%
  mutate(bed_rate = round((sum_los*100)/(beds * days), digit=2)) 
ward_stat

# Data Analysis ####
ward_stat



## assume ว่าต้องการแสดง ward = 2301
ward2301 <- 
  ward_stat %>%
  filter(ward == 2301)

## bar chart จำนวนผู้ป่วยใน
library(ggplot2)
ggplot(ward2301, aes(x = month_id, y = cnt_pt)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  geom_text(aes(label = cnt_pt), vjust = -0.5) +
  labs(title = "จำนวนผู้ป่วยที่รับไว้ในหอผู้ป่วยในแต่ละเดือน",
       x = "เดือน", y = "จำนวนผู้ป่วย") +
  theme_minimal()

## bar chart อัตราการครองเตียง
ggplot(ward2301, aes(x = month_id, y = bed_rate)) +
  geom_bar(stat = "identity", fill = "lightgreen") +
  geom_text(aes(label = bed_rate), vjust = -0.5) +
  labs(title = "อัตราการครองเตียงของหอผู้ป่วยในแต่ละเดือน",
       x = "เดือน", y = "อัตราการครองเตียง") +
  theme_minimal()


## line chart
ggplot(ward2301, aes(x = month_id, y = cnt_pt, group = 1)) +
  geom_line(color = "skyblue", size = 1) +
  geom_point(color = "skyblue", size = 3) +
  geom_text(aes(label = cnt_pt), vjust = -0.5) +
  labs(title = "จำนวนผู้ป่วยที่รับไว้ในหอผู้ป่วยในแต่ละเดือน",
       x = "เดือน", y = "จำนวนผู้ป่วย") +
  scale_y_continuous(limits = c(50, NA)) +
  theme_minimal()

## อยากรู้การกระจายตัวของ จำนวนวันนอน + ค่าใช้จ่ายที่เกิดขึ้น
# make scatter plot 
ggplot(ward_stat, aes(mead_los, mead_cost)) +     
  geom_point() + 
  geom_smooth()

## เอ๊ะใครกันนะ
los_hg <- ward_stat %>% filter(mead_los > 15)

# df ward
ward_nm <- data.frame(
  ward = c('2418', '2455', '2458', '303041001'), 
  ward_nm = c('วิกฤตศัลยกรรมประสาท', 'วิกฤตศัลยกรรมหัวใจ', 'วิกฤตศัลยกรรมหัวใจ', 'โรคหลอดเลือดสมอง')
)

los_hg <- left_join(los_hg, ward_nm, by='ward')
los_hg
## มีค่าใช้จ่ายสูง + นอนนาน อาจเกิดจากการนอนรอคิวผ่าตัดและหลังผ่าตัดอาจจะมีการ observe ดูอาการด้วย