## Homework Visualization
library(tidyverse)
library(ggplot2)
data(airquality)

# let's look at our dataset 
glimpse(airquality) 
head(airquality) 

# ความสัมพันธ์ระหว่างอุณหภูมิและปริมาณโอโซน
ggplot(airquality, aes(Temp, Ozone, color = Temp)) +
  geom_point(shape = 8, size = 3, na.rm = TRUE, show.legend = FALSE) +
  scale_color_gradient(low = "#03045e", high = "#ff8a5b") +
  geom_smooth(method = 'lm', se=TRUE, na.rm = TRUE, 
              fill='#0077b6',color='#023E8A') +
  theme_minimal() +
  labs(title = 'อุณหภูมิมีผลต่อปริมาณโอโซนในอากาศอย่างไร?',
       subtitle = 'ความสัมพันธ์ระหว่างอุณหภูมิและปริมาณโอโซน',
       caption = 'Built-in dataset: airquality ',
       x = 'Temp (°F) ',
       y = 'Ozone')

## correlation: Temp -> Ozone
airquality %>%
  filter(!is.na(Temp), !is.na(Ozone)) %>%
  summarise(corre_ = cor(Temp, Ozone))


# การกระจายตัวของความเร็วลม
ggplot(airquality,
       mapping = aes(Wind)) + 
  geom_histogram(bins = 8, fill = 'lightgreen', color='darkgreen') +
  theme_minimal() +
  labs(title = 'ความเร็วลมมีการกระจายตัวอย่างไรในช่วงเวลาที่ทำการเก็บข้อมูล?',
       subtitle = 'การกระจายตัวของความเร็วลม',
       caption = 'Built-in dataset: airquality ',
       x = 'Wind (Miles/Hour)',
       y = 'Count')


## freq table
airquality %>% 
  summarise(min_ = min(Wind),
            max_ = max(Wind))
# ความกว้าง = (20.7 - 1.7) / 8 = 2.375

# สร้างช่วงของข้อมูล
breaks <- seq(1.7, 20.7, by = 2.375)

# แบ่งช่วงข้อมูล
airquality <- airquality %>%
  mutate(Wind_cut = cut(Wind, breaks = breaks, include.lowest = TRUE))

# สร้างตารางแจกแจงความถี่
table(airquality$Wind_cut)



# ปริมาณโอโซนในแต่ละเดือน
airquality %>% 
  filter(!is.na(Ozone)) %>%
  group_by(Month) %>% 
  summarise(avg_ozone = mean(Ozone)) %>%
  ggplot(aes(Month, avg_ozone)) +
  geom_line(color = "navy", size = 1.2) +
  geom_point(color = "darkred", size = 4) +
  labs(title = "ปริมาณโอโซนมีการเปลี่ยนแปลงอย่างไรในแต่ละเดือน?",
       subtitle = "ปริมาณโอโซนในแต่ละเดือน", 
       x = "เดือนที่",
       y = "ค่าเฉลี่ยโอโซน (ppb)") +
  theme_minimal()
  
# table
airquality %>% 
  filter(!is.na(Ozone)) %>%
  group_by(Month) %>% 
  summarise(avg_ozone = mean(Ozone))


# ผลกระทบของรังสีแสงอาทิตย์ต่อปริมาณโอโซน
airquality %>%
  filter(!is.na(Ozone), !is.na(Solar.R)) %>%
  ggplot(aes(Solar.R, Ozone, color = Ozone)) + 
  geom_point(shape = 1, size = 3, show.legend = FALSE) +
  scale_color_gradient(low = "#04361d", high = "#76ba9d") +
  geom_smooth(method = 'lm', se=TRUE, na.rm = TRUE, 
              fill='#ef233c',color='#97051d') +
  theme_minimal() +
  labs(title = 'รังสีแสงอาทิตย์มีผลต่อปริมาณโอโซนอย่างไร?',
       subtitle = 'ผลกระทบของรังสีแสงอาทิตย์ต่อปริมาณโอโซน',
       caption = 'Built-in dataset: airquality ',
       x = 'ปริมาณรังสีแสงอาทิตย์',
       y = 'ความเข้มข้นของโอโซน')

## correlation: Temp -> Ozone
airquality %>%
  filter(!is.na(Solar.R), !is.na(Ozone)) %>%
  summarise(corre_ = cor(Solar.R, Ozone))


# การเปลี่ยนแปลงของอุณหภูมิในแต่ละวัน
airquality %>%
  filter(!is.na(Temp)) %>%
  ggplot(aes(Day, Temp)) +
  geom_line(color = "darkgreen", size = 1.2) +
  geom_point(color = "brown", size = 2)+
  facet_wrap(~Month, nrow=5) +
  theme_minimal()

# table
airquality %>%
  filter(!is.na(Temp)) %>%
  group_by(Month) %>%
  summarise(avg_temp = mean(Temp))
