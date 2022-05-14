library(tidyverse)
library(lubridate)
library(readr)

# Transformación de datos - Población  ------------------------------------------

poblacion <- read_csv2("Datos/Censo2017_Manzanas.csv")
View(poblacion)
names(poblacion)
poblacion %>% filter(REGION == 15) %>% 
  group_by(COMUNA) %>% summarise(POBLACION = sum(PERSONAS))

pob <- poblacion %>% group_by(REGION) %>% summarise(POBLACION = sum(PERSONAS))

### Proyeccion 2030

library(readxl)
poblacion <- read_xlsx("Datos/proyecciones-2002-2035-comuna-y-área-urbana-y-rural.xlsx")

poblacion_comuna <- poblacion %>% 
  janitor::clean_names() %>%  group_by(region, nombre_region, comuna, nombre_comuna) %>% 
  summarise(p_2002 = sum(poblacion_2002),
            p_2003 = sum(poblacion_2003),
            p_2004 = sum(poblacion_2004),
            p_2005 = sum(poblacion_2005),
            p_2006 = sum(poblacion_2006),
            p_2007 = sum(poblacion_2007),
            p_2008 = sum(poblacion_2008),
            p_2009 = sum(poblacion_2009),
            p_2010 = sum(poblacion_2010),
            p_2011 = sum(poblacion_2011),
            p_2012 = sum(poblacion_2012),
            p_2013 = sum(poblacion_2013),
            p_2014 = sum(poblacion_2014),
            p_2015 = sum(poblacion_2015),
            p_2016 = sum(poblacion_2016),
            p_2017 = sum(poblacion_2017),
            p_2018 = sum(poblacion_2018),
            p_2019 = sum(poblacion_2019),
            p_2020 = sum(poblacion_2020),
            p_2021 = sum(poblacion_2021),
            p_2022 = sum(poblacion_2022),
            p_2023 = sum(poblacion_2023),
            p_2024 = sum(poblacion_2024),
            p_2025 = sum(poblacion_2025),
            p_2026 = sum(poblacion_2026),
            p_2027 = sum(poblacion_2027),
            p_2028 = sum(poblacion_2028),
            p_2029 = sum(poblacion_2029),
            p_2030 = sum(poblacion_2030))

poblacion_region <- poblacion %>% 
  janitor::clean_names() %>%  group_by(region, nombre_region) %>% 
  summarise(
    p_2002 = sum(poblacion_2002),
    p_2003 = sum(poblacion_2003),
    p_2004 = sum(poblacion_2004),
    p_2005 = sum(poblacion_2005),
    p_2006 = sum(poblacion_2006),
    p_2007 = sum(poblacion_2007),
    p_2008 = sum(poblacion_2008),
    p_2009 = sum(poblacion_2009),
    p_2010 = sum(poblacion_2010),
    p_2011 = sum(poblacion_2011),
    p_2012 = sum(poblacion_2012),
            p_2013 = sum(poblacion_2013),
            p_2014 = sum(poblacion_2014),
            p_2015 = sum(poblacion_2015),
            p_2016 = sum(poblacion_2016),
            p_2017 = sum(poblacion_2017),
            p_2018 = sum(poblacion_2018),
            p_2019 = sum(poblacion_2019),
            p_2020 = sum(poblacion_2020),
            p_2021 = sum(poblacion_2021),
            p_2022 = sum(poblacion_2022),
            p_2023 = sum(poblacion_2023),
            p_2024 = sum(poblacion_2024),
            p_2025 = sum(poblacion_2025),
            p_2026 = sum(poblacion_2026),
            p_2027 = sum(poblacion_2027),
            p_2028 = sum(poblacion_2028),
            p_2029 = sum(poblacion_2029),
            p_2030 = sum(poblacion_2030),
  )

poblacion_region <- poblacion_region %>% select(-nombre_region) %>% 
  pivot_longer(!region, names_to = "periodo", values_to = "poblacion") %>% 
  mutate(periodo = as.numeric(str_remove_all(periodo , "p_")))



poblacion_comuna <- poblacion_region %>% select(-nombre_region) %>% 
  pivot_longer(!region, names_to = "periodo", values_to = "poblacion") %>% 
  mutate(periodo = as.numeric(str_remove_all(periodo , "p_")))

write.csv(poblacion_region, "poblacion_region.csv")
write.csv(poblacion_comuna, "poblacion_comuna.csv")

## Construcccion data estaciones

estaciones <- read_csv("Datos/cr2_prDaily_2020/cr2_prDaily_2020_stations.txt")
View(estaciones)

## Construcccion data precipitaciones

prep <- read_csv("Datos/cr2_prDaily_2020v2/cr2_prDaily_2020.txt",
                 col_names = FALSE, na = c("", "NA",-9999))

caud <- read_csv2("Datos/caudales_rio_maipo.csv",
                 na = c("", "NA",-9999))



caud %>% group_by(estacion) %>% count()
  

x2 <- prep4 %>% group_by(codigo_estacion, nombre_estacion) %>% count()


# Transformación de datos - Caudales ----------------------------------------------------------------

library(readxl)
ruta1 <- "Datos/Caudales/Caudales Medios Diarios 14_05_2022 17_08.xls"
ruta2 <- "Datos/Caudales/Caudales Medios Diarios 14_05_2022 17_12.xls"
ruta3 <- "Datos/Caudales/Caudales Medios Diarios 14_05_2022 17_13 (1).xls"
ruta4 <- "Datos/Caudales/Caudales Medios Diarios 14_05_2022 17_13.xls"
ruta5 <- "Datos/Caudales/Caudales Medios Diarios 14_05_2022 17_14.xls"
ruta6 <- "Datos/Caudales/Caudales Medios Diarios 14_05_2022 17_15.xls"

readxl::excel_sheets(ruta1)
readxl::excel_sheets(ruta2)
readxl::excel_sheets(ruta3)
readxl::excel_sheets(ruta4)
readxl::excel_sheets(ruta5)
readxl::excel_sheets(ruta6)

caudales <- function(ruta){
h1 <- ruta %>%
  excel_sheets() %>%
  set_names() %>%
  map_dfr(read_excel, path = ruta, skip = 9, .id = "nombre") %>%
  janitor::clean_names() %>%   mutate(year = x1 ) %>% 
  select(year, everything()) %>% mutate(year = case_when(year == "AÑO: 2018" ~ 2018,
                                         year == "AÑO: 2019" ~ 2019,
                                         year == "AÑO: 2020" ~ 2020,
                                         year == "AÑO: 2021" ~ 2021
                                         )) %>% fill(year) %>% 
  select(nombre, year, x1, x2, x4, x6, x8,x10,x12,x14,x16,x18,x20,x22,x25)

names(h1) <- c("nombre", "year", "day", month.name)

h1 <- h1 %>% filter(day %in% as.character(1:31))
h1
}

c1 <- caudales(ruta1)
c2 <- caudales(ruta2)
c3 <- caudales(ruta3)
c4 <- caudales(ruta4)
c5 <- caudales(ruta5)
c6 <- caudales(ruta6)

final <- c1 %>% bind_rows(c2) %>% bind_rows(c3) %>% 
  bind_rows(c4) %>% bind_rows(c5) %>% bind_rows(c6)

caudales <-final %>% pivot_longer(cols = January:December, names_to = "mes", values_to = "Caudal")
glimpse(caudales)

write.csv(caudales,"caudales_2018-2021.csv")
