
# page that uses ggmap and a heatmap
# https://www.rdocumentation.org/packages/ggmap/versions/3.0.0
# https://rdrr.io/cran/ggmap/man/qmplot.html

# less usefull:
# https://www.r-bloggers.com/data-on-tour-plotting-3d-maps-and-location-tracks/

library(ggplot2)
library(ggmap)

# map_theme <- list(theme(legend.position = "top",
#                         panel.grid.minor = element_blank(),
#                         panel.grid.major = element_blank(),
#                         panel.background = element_blank(),
#                         plot.background = element_rect(fill = "white"),
#                         panel.border = element_blank(),
#                         axis.line = element_blank(),
#                         axis.text.x = element_blank(),
#                         axis.text.y = element_blank(),
#                         axis.ticks = element_blank(),
#                         axis.title.x = element_blank(),
#                         axis.title.y = element_blank(),
#                         plot.title = element_text(size = 18)))


# vancouver scraped location min/max
# max lat, lon 57.674786	-96.416838
# min lat, lon 19.862189	-101.445007
lat <- (57.674786+-96.416838)/2
lat
lon <- (-101.445007 + -96.416838)/2
lon

lat <-49.22961461140338
lon <- -122.89116821041198

df <- data.frame(lon=c(lon), lat=c(lat))
df

df <- read.csv("/home/james/projects/clscraper/realty_prices_by_geo.csv")

df$lon <- df$longitude
df$lat <- df$latitude
df$price <- factor(df$price)
# df$price <- factor(df$price)

# vancouver all the way to chiliwack
# bbox=c(-122.9985,49.0338,-122.3256,49.3218)

# vancouver to surrey
bbox=c(-123.3112,49.0509,-122.6287,49.4047)

mp <- mean(df$price, na.rm=TRUE)
summary(df)

map <- get_stamenmap(c(lon, lat),
        data=df,
        zoom = 10,
        maptype = "toner-lite",
        # darken=0.7,
        source="stamen",
        bbox=bbox)

mp

df$price

qmplot(lon, lat,
       data=df,
       zoom = 10,
       geom="blank",
       maptype = "toner-background",
       # darken=0.7,
       source="stamen") +
  stat_density_2d(aes(fill=..level..), geom="polygon", alpha=0.1, color=NA) +
  scale_fill_gradient2("price", low="green", high="red", midpoint=mp)

# ggmap(map)


?stat_density_2d
?diamonds
?ggmap::crimes
warnings()

?ggmap

?
?ggplot2

# ggmap(map) + 
#   geom_point(data = data_combined, aes(x = lon, y = lat, color = track), alpha = 0.3) +
#   scale_color_brewer(palette = "Set1") +
#   map_theme
