install.packages('nycflights23')
library(nycflights23)
library(tidyverse)

# DF: flights
glimpse(flights) #Rows: 435,352 Columns: 19

# 5 queries
View(airlines)
View(airports)
View(planes)
View(flights)
View(weather)

# ในปี 2023 เที่ยวบินใดมีแนวโน้มที่จะล่าช้ามากที่สุด (โดยเฉลี่ย) เมื่อพิจารณาจากสายการบิน และช่วงเวลาของปี
carr_monthid <- flights %>%
  select(year, month, day, carrier, origin, dest, dep_delay, arr_delay) %>%
  mutate(dep_delay = replace_na(dep_delay, 0),
         arr_delay = replace_na(arr_delay, 0)) %>%
  mutate(sum_delay = dep_delay + arr_delay,
         cs_delay = ifelse(sum_delay > 0, "Late", ifelse(sum_delay < 0, "Early", "On time"))) %>%
  group_by(year, month, carrier, origin, dest) %>%
  summarise(n_rows = n(),
            sumt_delay = sum(sum_delay),
            avgt_delay = round(mean(sum_delay),2)) %>%
  arrange(desc(avgt_delay), carrier, origin, dest, year, month) %>%
  left_join(airlines, by='carrier') %>%
  select(carrier, carr_name = name, everything())

View(carr_monthid)


carr_top10 <- carr_monthid %>%
  head(10)

View(carr_top10)


carr_smdelay <- flights %>%
  select(year, month, day, carrier, dep_delay, arr_delay) %>%
  mutate(dep_delay = replace_na(dep_delay, 0),
         arr_delay = replace_na(arr_delay, 0)) %>%
  mutate(sum_delay = dep_delay + arr_delay,
         cs_delay = ifelse(sum_delay > 0, "Late", ifelse(sum_delay < 0, "Early", "On time"))) %>%
  group_by(carrier) %>%
  summarise(n_rows = n(),
            sumt_delay = sum(sum_delay),
            avgt_delay = round(mean(sum_delay),2)) %>%
  arrange(avgt_delay) %>%
  left_join(airlines, by='carrier') %>%
  select(carrier, carr_name = name, everything())

View(carr_smdelay)


## bar chart
library(ggplot2)
ggplot(carr_smdelay, aes(x = carrier, y = avgt_delay)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  geom_text(aes(label = avgt_delay), vjust = -0.5) +
  labs(title = "Airline Delay Statistics",
       x = "Carrier", y = "Mean time delay") +
  theme_minimal()

# เส้นทางการบินใดที่มีปริมาณผู้โดยสารมากที่สุด และเส้นทางใดที่มีการแข่งขันสูงที่สุด (พิจารณาจากจำนวนสายการบินที่ให้บริการ)
top_passenger <- flights %>%
  select(carrier, tailnum, origin, dest) %>%
  left_join(planes, by='tailnum') %>%
  select(carrier, tailnum, origin, dest, seats) %>%
  mutate(seats = ifelse(is.na(seats), 0, seats)) %>%
  group_by(origin, dest) %>%
  summarise(sum_seats = sum(seats),
            n_flight = n()) %>%
  arrange(desc(sum_seats)) %>%
  head(10)

View(top_passenger)

compet_route <- flights %>%
  select(carrier, origin, dest) %>%
  group_by(origin, dest) %>%
  summarise(uni_carr = n_distinct(carrier),
            n_flight = n()) %>%
  arrange(desc(uni_carr), desc(n_flight)) %>%
  head(10)

View(compet_route)

# เครื่องบินรุ่นใดมีประสิทธิภาพในการใช้เชื้อเพลิงมากที่สุด และเครื่องบินรุ่นใดที่มีปัญหาการซ่อมบำรุงมากที่สุด
eff_planes <- flights %>%
  select(tailnum, distance, air_time) %>%
  mutate(fuel_consump = distance/air_time) %>%
  filter(!is.na(fuel_consump), fuel_consump != Inf) %>%
  group_by(tailnum) %>%
  summarise(avg_fuel_consump = mean(fuel_consump)*60) %>%
  arrange(avg_fuel_consump) %>%
  # arrange(desc(avg_fuel_consump)) %>%
  head(10)

View(eff_planes)

carr_delay <- flights %>%
  select(tailnum, dep_delay, arr_delay) %>%
  mutate(sum_delay = dep_delay+arr_delay) %>%
  filter(sum_delay > 0) %>%
  group_by(tailnum) %>%
  summarise(avg_delay = mean(sum_delay),
            n_delay = n()) %>%
  arrange(desc(n_delay)) %>%
  head(10)

View(carr_delay)

library(stats)
# สภาพอากาศมีผลกระทบต่อความล่าช้าของเที่ยวบินอย่างไร
flights_with_weather <- flights %>%
  select(carrier, origin, dep_delay, year, month, day, hour) %>%
  left_join(weather, by = c("origin", "year", "month", "day", "hour")) %>%
  filter(!is.na(dep_delay), !is.na(precip), !is.na(wind_gust), !is.na(visib)) %>%
  group_by(origin) %>%
  summarise(corr_precip = cor(dep_delay, precip),
            corr_wind_gust = cor(dep_delay, wind_gust),
            corr_visib = cor(dep_delay, visib))

flights_with_weather

# ในแต่ละสนามบินช่วงเวลาใดของวัน (hour) ที่มีแนวโน้มที่จะเกิดความล่าช้าในการออกเดินทาง (dep_delay) มากที่สุด และช่วงเวลาใดที่มีความล่าช้าน้อยที่สุด
delay_by_time <- flights %>%
  select(origin, hour, dep_delay) %>%
  group_by(origin, hour) %>%
  summarise(avg_dep_delay = mean(dep_delay, na.rm = TRUE)) %>%
  arrange(origin, desc(avg_dep_delay))

max_delay <- delay_by_time %>%
  group_by(origin) %>%
  slice_max(avg_dep_delay) %>%
  mutate(type = 'max delay')

min_delay <- delay_by_time %>%
  group_by(origin) %>%
  slice_min(avg_dep_delay)%>%
  mutate(type = 'min delay')

bind_rows(max_delay, min_delay) %>%
  arrange(origin)
