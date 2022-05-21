
# MIA_DS_project: GRUPO 8
Proyecto 2022-1 MIA UC, Intro Data Science

<!-- PROJECT LOGO -->

<br />
<div align="center">
<a href="https://github.com/grojasc/image">
    <img src="image/png-clipart-blue-water-glass-without-matting-blue-transparent.png" alt="Logo" width="200" height="200">
</a>

<div align="left">




## Links importantes

+ Documento Entrega 1 :arrow_right: [link](https://docs.google.com/document/d/1iX4fWpx_Ve2AxUk_cVHWpNWbe2lXNLpwhVjJG1Vsx94/edit?pli=1)
+ Super Servicios Sanitarios:arrow_right: [link]( www.siss.gob.cl)
+ Drive Grupo 8:arrow_right: [link](https://drive.google.com/drive/u/0/folders/1rM6gkgPJj0QzSdJE5wqqjWYgZrwgCO_a)
+ Aguas Andinas reportes :arrow_right: [link](https://sustentabilidad.aguasandinas.cl/documents/33547/35846/Reporte+Integrado+Aguas+Andinas+2019.pdf/cd2cdfeb-5338-66ae-7bd0-8cb06a0f20ca?t=1590688082827)
+ Miro colaborativo ➡️ [link](https://miro.com/app/board/uXjVO0YbVvA=/)


## Árbol del repositorio.

```
.
├── Código
│   ├── Preprocesamiento
│   │   ├──caudales_rio_maipo.py
│   │   ├──precipitacion_rio_maipo.py
│   │   ├──datos_demanda.py
│   │   ├──NotebookDesarrolloenR_preprocesamientodeDatos.html
│   │   └── temperatura_rio_maipo.py
│   ├── Análisis exploratorio
│   │   ├──20220514 Trabajo Introduccion DS 2.ipynb
│   │   └── caudales_manzano.py
│   │
│   └── Modelamiento
│       ├── analisis_oferta_agua.py
│       ├── NotebookDesarrolloenR_modelamientocaudalesydemanda.html
│       └── regresion_demanda.py
├── Data Procesada
│   ├── Regiones.csv Fuente : (https://www.ine.cl/estadisticas/sociales/demografia-y-vitales/proyecciones-de-poblacion)
│   ├── caudales_2018-2021.csv
│   ├── Data regresión
│   └── Comunas.csv Fuente : (https://www.ine.cl/estadisticas/sociales/demografia-y-vitales/proyecciones-de-poblacion)
├── Data
│   ├── Datos de consumo (Articles-16585.xlsx) Fuente: (http://www.siss.gob.cl/appsiss/historico/w3-propertyvalue-6377.html)
│   ├── Poblacion_region.csv Fuente: (https://www.ine.cl/estadisticas/sociales/demografia-y-vitales/proyecciones-de-poblacion)
│   ├── cr2_qflxDaily_2018_stations Fuente: (https://www.cr2.cl/datos-de-caudales/)
│   ├── cr2_qflxDaily_2018_description Fuente: (https://www.cr2.cl/datos-de-caudales/)
│   ├── cr2_qflxDaily_2018.txt Fuente: (https://www.cr2.cl/datos-de-caudales/)
│   ├── Glaciares.shp  Fuente:  http://www.geoportal.cl/geoportal/catalog/search/resource/resumen.page?uuid={99BCC048-47F7-4FD0-8C6D-FB9DDB66A789}
│   ├── caudales_rio_maipo.csv Fuente: (https://www.ine.cl/estadisticas/sociales/demografia-y-vitales/proyecciones-de-poblacion)
│   ├── Crecimiento PIB % Mundial.xlsx Fuente : (https://datos.bancomundial.org/indicator/NY.GDP.MKTP.KD.ZG)
│   ├── Crecimiento_población_mundial.xlsx Fuente : (https://datos.bancomundial.org/indicator/SP.POP.GROW)
│   ├── Precios de petroleo.xlsx Fuente: (https://si3.bcentral.cl/)
│   └── Poblacion_comuna.csv  Fuente: (https://www.ine.cl/estadisticas/sociales/demografia-y-vitales/proyecciones-de-poblacion)
└──  Docs/Minutas

```
 <!-- ABOUT THE PROJECT -->
## Sobre el Proyecto

Tras 13 años de sequía, recientemente se dio a conocer un protocolo elaborado por la Superintendencia de Servicios Sanitarios (SiSS),
el gobierno y Aguas Andinas para el racionamiento del agua en la región metropolitana. Esta situación podría afectar la calidad de vida de más de 7 millones de personas.
El protocolo contempla un esquema de alertas progresivas que dependen de los sistemas de abastecimiento de los ríos Maipo y Mapocho, y el cual se divide en cuatro tipos de alerta:

<a href="https://github.com/grojasc/image">
    <img src="image/alerta.png" alt="Logo" width="800" height="600">
</a>

`Imagen 1. Protocolo de racionamiento en la Región Metropolitana. Superintendencia de servicios sanitarios.`


De ser necesaria la activación de la Alerta Roja habría más de 140 mil clientes afectados para quienes obtienen los suministros de agua gracias al Río Mapocho, y más de 1 millón y medio de clientes perjudicados en el caso de quienes se abastecen por el Río Maipo.
  
Se desea elaborar un análisis descriptivo y exploratorio que permita reconocer las zonas de mayor riesgo, luego a través de un modelo estadístico se buscará estimar la disponibilidad de agua potable en la zona. De esta manera, será posible comunicar a las autoridades y a las  comunidades con el fin de tomar medidas oportunas para evitar mayores impactos en el consumo y disponibilidad de este recurso natural.

## Objetivos
+ Estudiar los ciclos en la cantidad del flujo del agua en los caudales de Chile.
Las variaciones en el flujo de agua están determinadas por factores climáticos y de temporadas. Identificaremos insights a través de la exploración de los datos, segmentando por décadas, estaciones del año, regiones geográficas, entre otras variables.
+ Establecer correlaciones entre el suministro y la demanda de agua en distintas zonas geográficas del país, además de otros atributos asociados al consumo de agua.
La demanda del agua proviene de muchas fuentes (sector urbano, rural, industrial, agrícola, etc). Estableceremos en distintas regiones del país, cuáles son los + grupos que representan mayor impacto en el uso del agua y categorizarlos por su volumen de consumo.
+ Explorar un modelo que nos permita predecir cuándo será necesario establecer un racionamiento de agua en la población.
A partir del consumo de agua y su disponibilidad, establecer bajo ciertos criterios y parámetros, el momento adecuado para realizar restricciones en el consumo de agua en distintas zonas del país, a través de la aplicación de modelos estadísticos. 

## Herramientas

Algunas de las herramientas y lenguajes utilizados:

* [R](https://rstudio.com/)
* [colab](https://colab.research.google.com/)
* [Python](https://python.org/)
* [Github](https://github.com/)


<p align="right">(<a href="#top">back to top</a>)</p>


## Extración y Procesamiento de Datos
    
### Estaciones de Control de Caudales: 
    
+ Extracción de los archivos de estaciones de control de caudal de agua del país.
    
+ Creación de data frames y geodata frames para hacer análisis exploratorio.
    
### Ministerio de Obras Públicas: 
+ Data wrangling. 
### Instituto Nacional de Estadística:
    
+ Sistematización de información sociodemográfica como crecimiento demográfico, zonas de residencia y tasas de pobreza de la región metropolitana.
    
    
 ## Conclusiones y Recomendaciones
 
  Según nuestro pronóstico se espera que el año 2030 se utilice la mitad del agua disponible del río maipo para consumo humano. Para el 2058, se utilizará el 100%.
El análisis exploratorio nos muestra que las temperaturas se han elevado, las precipitaciones han disminuido lo que en resumen se refleja en bajas e los caudales que nos proveen de agua.

    
 La pregunta que nos hicimos al comienzo del trabajo fue: ¿Cuándo se tendrá que racionar el agua en Chile?, en el camino decidimos acotar la investigación a la Región Metropolitana debido a la diversidad de climas que hay a lo largo de nuestro país lo que podía complejizar mucho el análisis en términos climatológicos. Además, escogimos esta región porque es la que concentra la mayor cantidad de habitantes en nuestro país. 

Luego de analizar diversas bases de datos de muchas fuentes distintas, pudimos concluir 
según nuestro pronóstico si se mantiene los patrones de consumo de agua potable actuales, se espera que el año 2030 estemos consumiendo aproximadamente la mitad del agua disponible del Río Maipo, para consumo humano (no industrial). 
Por otra parte, llegamos a la conclusión de que para el 2058 año se utilizará el 100% del caudal del río.

    
 El análisis exploratorio nos muestra que las temperaturas se han elevado en la Región al igual que en el resto del país y que las precipitaciones han disminuido, esto estaría afectando de manera directa el caudal del agua. 

Si bien este análisis y el modelo desarrollado explican parte de la demanda por el agua, la mayor demanda proviene del sector agrícola y los rubros económicos asociados a la  minerías, sector agropecuario y sector industrial. Por lo tanto, si bien es importante hacer consciente a la ciudadanía de la crisis hidria en la que nos encontramos, es tanto o más importante desarrollar estrategias incentiven a que las empresas inviertan en tecnologías que lleven a disminuir el agua en sus procesos.


    











