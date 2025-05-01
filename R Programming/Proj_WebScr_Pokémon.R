# Load library
library(rvest)
library(tidyverse)
library(googlesheets4)

# List of Pokémon
url <- "https://pokemon.fandom.com/wiki/List_of_Pok%C3%A9mon"

# Extracting text from table tag
pokemon_data <- url %>%
  read_html() %>%
  html_elements("table.wikitable") %>%   # Select <table> tag & .class wikitable
  .[[1]] %>%                             # only 1st table
  html_table()                           # Convert table to df

pokemon_data <- pokemon_data %>% mutate(generation = 'IX') # add col generation
pokemon_data

# Extracting image URLs from table tag
image_urls <- url %>%
  read_html() %>%
  html_elements("table.wikitable") %>%  # Select <table> tag & .class wikitable
  .[[1]] %>%                            # only 1st table
  html_elements("a.image") %>%          # Select <a> tag & .class image
  html_attr("href")                     # Extract the "href" attribute (image URL)

image_urls

# Combine the image URLs with the Pokemon data
pokemon_data$Image_URL <- image_urls[1:nrow(pokemon_data)]

pokemon_data


# Optional: Download images
for (i in 1:nrow(pokemon_data)) {
   download.file(pokemon_data$Image_URL[i], paste0("pokemon_images/", pokemon_data$Name[i], ".png"), mode = "wb")
}

# Google Sheet URL
sheet_url <- "https://docs.google.com/spreadsheets/d/1mGXpI44CT6tXsFdz9vYA3dDHzqgjVaWdn0Dw1F_fhfA" # Replace with your sheet's URL

# Authenticate
gs4_auth()

write_sheet(pokemon_data, ss = sheet_url, sheet = "PokeList_IX")
