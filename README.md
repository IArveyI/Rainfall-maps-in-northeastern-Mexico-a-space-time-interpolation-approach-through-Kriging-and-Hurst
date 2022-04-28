# Rainfall maps in northeastern Mexico a space time interpolation approach through Kriging and Hurst

This repository is made with the purpose of achieving reproducibility of the methodology applied in the article: "Rainfall maps in northeastern México, a space-time interpolation approach through Kriging and Hurst" (hyperlink to the article).

## Aim

The study region is the San Juan River basin, located in northeastern Mexico, between the states of Coahuila, Nuevo León and Tamaulipas. Currently, there is a water scarce in this area, so a geospatial analysis is performed with Kriging interpolation, showing the behavior of the area based on the average annual amount of rainfall and its historical behavior of persistence or anti-persistence using the Hurst exponent.

## Introduction

For more detailed information, see Additional File 2 (hyperlink to Additional File 2).

Observed data are measurements of the amount of rainfall at different points in a specific region. The spatial correlation of the scalar field _**Z**_ as a function of distance is known as a *variogram* or *semivariogram*. For clarification, although variogram and semivariogram are commonly used interchangeably, they can actually provide certain differences, so using the term variogram urges a complete calculation rather than the partial one that is represented in the semivariogram.

Consider two points with position vectors **_x_** and **_x+h_**, respectively, see Fig. 1.

<p align="center">
  <img width="460" height="300" src="Images/Figure-1.jpg">
</p>
<p align="center">
    <em>Fig. 1 - Scalar field Z(x) for this study are the rainfall values or Hurst exponent.</em>
</p>

The *variogram* **_γ_** by definition is the variance of the differences of a stationary random field, that is:

<p align="center">
    <img src="https://render.githubusercontent.com/render/math?math=\gamma({\bf h}) = \frac{1}{2}Var[Z({\bf x %2B \bf h}) - Z({\bf x})] =                                   \frac{1}{2}E\{[Z({\bf x %2B \bf h}) - Z({\bf x})]^{2}\}#gh-light-mode-only">
    <img src="https://render.githubusercontent.com/render/math?math={\color{white}\gamma({\bf h}) = \frac{1}{2}Var[Z({\bf x %2B \bf h}) - Z({\bf x})] =                         \frac{1}{2}E\{[Z({\bf x %2B \bf h}) - Z({\bf x})]^{2}\}}#gh-dark-mode-only">
</p>

where **_γ_** is independent to the location of **_x_** and dependent only on the vector **_h_**.

**EXPERIMENTAL VARIOGRAM**

The classical estimator or experimental (sample) variogram **_γ_*** is given by the following equation:

<p align="center">
   <img src="https://render.githubusercontent.com/render/math?math=\gamma^{\ast}({\bf H}) = \frac{1}{2n_{c}}\sum_{i = 1}^{n_{c}}[Z({\bf x}_{i}                            %2B {\bf h}) - Z({\bf x}_{i})]^{2}#gh-light-mode-only">
    <img src="https://render.githubusercontent.com/render/math?math={\color{white}\gamma^{\ast}({\bf H}) = \frac{1}{2n_{c}}\sum_{i = 1}^{n_{c}}[Z({\bf x}_{i}               %2B {\bf h}) - Z({\bf x}_{i})]^{2}}#gh-dark-mode-only">
</p>

where n<sub>c</sub> is the number of pairs of points connected by all vectors **_h_** belonging to a class **_H_** of vectors whose magnitude and direction fall within a specific region, see Fig.2.

<p align="center">
  <img width="460" height="300" src="Images/Figure-2.jpg">
</p>
<p align="center">
    <em>Fig. 2 - The vector h that goes from the center of the circle to any point in the shaded region is a vector whose magnitude is between |H| and |H +           a|, with direction between θ and θ + b. All the vectors within the shaded region (family H) are the ones that determine the average in the empirical         variogram equation.</em>
</p>


**VARIOGRAM PARAMETERS**
The theoretical model associated with the empirical variogram depends in general on three independent parameters known as the *nugget* effect _C<sub>0</sub>_, the partial *plateau* _C_ and the *range* _R_, see Fig.3.

<p align="center">
  <img width="460" height="300" src="Images/Figure-3.jpg">
</p>
<p align="center">
    <em>Fig. 3 - A general theoretical model of the empirical variogram with its principal components: Range, Sill, Partial Sill and Nugget. The origin of           the horizontal scale corresponding to h<sub>min</sub> ≡ 0.</em>
</p>

- *The nugget effect : According to the definition of the variogram, when _h = 0_ the variogram is also zero, _**γ**(0) = 0_. However, in practice the theoretical value _h = 0_ corresponds to a minimum separation value _h<sub>min</sub>_ between rainfall stations. This empirical "residual" value of the variogram is known as the *nugget effect* and is represented by _**γ***(0)= C<sub>0</sub>_.

- *Partial sill* : Again, according to the definition, in a process without long-range correlations, when _h→∞_ ρ→0 is expected, ρ being the correlation coefficient, therefore, the variogram converges to the constant value _f<sub>0</sub>_. In practice, however, it is observed that from a certain maximum distance _h<sub>max</sub>_ the empirical variogram "stabilizes", that is, the variogram practically does not grow when _h_ increases.This "asymptotic" value, measured from the *nugget*, where the variogram levels with the horizontal is known as the *partial plateau* and is symbolized by _C_. The sum _C<sub>0</sub> + C_ is conceived as the *plateau* or threshold of the variogram.

- *Range* : The value _h<sub>max</sub>_ for which the empirical variogram model begins to "flatten" is called *range* and is denoted by the symbol _R ≡ h<sub>max</sub>_. Observations of the scalar field at points separated by a distance greater than the range _R_ are considered to be uncorrelated, i.e., if _|x<sub>i</sub> - x<sub>j</sub>| > R_ then _Cov[Z(x<sub>i</sub>), Z(x<sub>j</sub>)] = 0_, _i ≠ j_. 

**MODELO TEÓRICO**

Cuatro de los modelos teóricos más utilizados para ajustar los valores del variograma experimental o empírico son los siguientes \cite{mert4,montero5}, ver la Fig. 4.

<p align="center">
  <img width="460" height="300" src="Images/Figure-4.jpg">
</p>
<p align="center">
    <em>Fig. 4 - La figura muestra 4 de los modelos teóricos de variogramas más utilizados, un modelo esférico (curva azul), un modelo lineal (curva verde),         un modelo Gaussiano (curva morada) y un modelo exponencial (curva naranja). Para fines de comparación en todos los casos se han utilizado los mismos         parámetros: C<sub>0</sub> = 1, C = 3, y a = 1.5. La figura muestra también el valor del rango para cada modelo: R = a, √3a, 3a para los modelos               exponencial y lineal, Gaussiano, y exponencial, respectivamente.</em>
</p>

**Variograma esférico**

<p align="center">
  <img width="460" src="Images/Equation-1.JPG">
</p>

El variograma esférico alcanza el valor umbral _C<sub>0</sub> + C_ exactamente cuando el rango es _|h|= R = a_.

**Variograma exponencial**

<p align="center">
  <img width="460" src="Images/Equation-2.JPG">
</p>

Aunque teóricamente el valor del variograma para el modelo exponencial alcanza el umbral _C<sub>0</sub> + C_ cuando _|h|→∞_, en la práctica se dice que se ha alcanzado dicho umbral para el valor  _|h| = a*_ tal que _γ(a*) - C<sub>0</sub> = 0.95C_, esto es, para un rango efectivo igual a _R ≡ a* ≈ 3a_.

**Variograma Gaussiano**

<p align="center">
  <img width="460" src="Images/Equation-3.JPG">
</p>

Justo como en el modelo exponencial, en la práctica se dice que el variograma Gaussiano alcanza el umbral _C<sub>0</sub> + C_ cuando el rango efectivo _R ≡ a*_ es tal que _γ(a*) - C<sub>0</sub> = 0.95C_, esto es, cuando _R ≡ a* ≈ √3a_.

**Variograma lineal**

<p align="center">
  <img width="460" src="Images/Equation-4.JPG">
</p>

**INTERPOLACIÓN DE KRIGING ORDINARIO**

El método de Kriging Ordinario supone que los datos observados representan una realización de un proceso estocástico espacial estacionario de segundo orden, esto es, que la media del proceso estocástico es una constante y que su función de autocovarianza depende únicamente de la distancia de separación entre los puntos observados. 

En el Kriging Ordinario la estimación _Ẑ(x<sub>0</sub>)_ del valor del campo escalar en el punto _x<sub>0</sub>_ es una combinación lineal de los valores observados _Ẑ(x<sub>i</sub>)_ del campo escalar en cada uno de los puntos de observación _x<sub>i</sub>_, es decir:

<p align="center">
   <img src="https://render.githubusercontent.com/render/math?math={\hat Z}({\bf x}_{0}) = \sum_{i = 1}^{n}\lambda_{i}Z({\bf x}_{i})#gh-light-mode-only">
   <img src="https://render.githubusercontent.com/render/math?math={\color{white}{\hat Z}({\bf x}_{0})=\sum_{i=1}^{n}\lambda_{i}Z({\bf x}_{i})}#gh-dark-mode-             only">
</p>

donde _Ẑ(x<sub>0</sub>)_ es el valor estimado del campo aleatorio _Z_ en  _x<sub>0</sub>_, _Ẑ(x<sub>i</sub>)_ es el valor del campo aleatorio en el punto x<sub>i</sub>, y los λ<sub>i</sub> son los coeficientes (pesos) a ser determinados, para _i = 1, 2, ... , n_.

## Metodología

En general, la metodología sigue los pasos de la Fig.5:
<p align="center">
  <img width="586" height = "306" src="Images/Figure-5.png">
</p>

**STEP 1 - CLIMATOL DATA PREPARATION**

Para empezar, se recomienda crear una carpeta y establecerla como directorio de trabajo para realizar el proyecto. Para este paso es necesario tener descargada la carpeta *Stations* en este directorio. En este paso, se lee la información de datos mensuales de lluvia de cada estación y se analizan en que años existe la mayor cantidad de datos, con esto, se elige el periodo de _1998-2018_. Después, se filtran las estaciones con una cantidad mayor o igual a _80%_ de datos en ese periodo. Con los valores de las estaciones que pasan este filtro, se preparan los archivos para utilizarlos en la libreria *Climatol*. El programa crea la carpeta *Climatol* dentro del directorio de trabajo con dos archivos, *Rmon_1998-2018.est* con las coordenadas e información de cada estación y *Rmon_1998-2018.dat* con los valores mensuales de lluvia de las estaciones. Estos  archivos serán necesarios para el siguiente paso.

**STEP 2 - HOMOGENIZATION BY CLIMATOL**

Para este paso, es necesario establecer como directorio de trabajo la carpeta *Climatol* creada anteriormente. Este programa genera distintos archivos, el archivo *Rmon_1998-2018.txt* es un diagnóstico general de las estaciones, de este archivo se obtiene la información del porcentaje de datos originales (POD) en el archivo *Stations POD.csv*, y el archivo *Rmon_1998-2018.pdf* es un informe con un análisis exploratorio de datos y el procedimiento de imputación de los datos. El archivo *Rmon_1998-2018_series.csv* contiene las series mensuales de las estaciones con datos ya imputados. Para conocer más de cómo funciona la librería [*Climatol*](https://www.climatol.eu/) visitar su sitio oficial.
 
**STEP 3 - Hurst exponent and mean rainfall**

Es necesario tener descargados en el directorio de trabajo, los archivos *Stations POD.csv* y *Stations Info.csv*, y generar el archivo *Rmon_1998-2018_series.csv* del paso 2 en la carpeta Climatol. Se filtran las estaciones con un _POD >= 80_ ya eliminados los datos outliers y ya homogeneizados. Este programa genera el archivo *Aditional File 1.csv* con la información de localización de las estaciones, la media anual de lluvia y exponente de Hurst de cada una.

**STEP 4 - Exploratory Data Analysis**

Es necesario tener descargado en el directorio de trabajo el archivo *Boundary.csv* y el archivo *Aditional File 1.csv* generado en el paso anterior. Se genera el archivo *Area.csv* que se utilizará en el siguiente paso. Se generan los mapas de localización de las estaciones dentro de la zona de estudio, con un graiente de color que identifica la intensidad de los valores de lluvia y exponente de hurst. Se grafica las variables de lluvia y exponente de Hurst para ver su estacionaridad de acuerdo a su longitud, latitud y elevación, además, se mide la media y desviación estándar de todas las estaciones. Se obtienen las distribuciones de lluvia y exponente de Hurst para los datos originales, y además, se aplico una transformación a estos datos por logaritmo *(Log)*. A cada una de estas distribuciones se obtuvo su coeficiente de asimetría. Se observa que las distribuciones de datos originales de ambas variables son más simétricas para datos originales, por lo que se decide utilizar los datos originales para el modelo, ya que, para aplicar la interpolación Kriging es necesaria que la distribución de los datos sea simétrica. Además, se calculan los coeficientes de autocorrelación _I_ de Morán y _c_ de Geary. Para esto, la región de estudio se dividió en regiones de acuerdo a un diagrama de Voronoi, tomando cada estación como nodo, una vez hecho esto, se calcularon los coeficientes de autocorrelación.

**STEP 5 - VARIOGRAM MAP**

Es necesario tener descargado el archivo *Aditional File 1.csv* en el directorio de trabajo. Este programa realiza el mapa variográfico de la región de estudio, esto sirve para identificar anisotropía en la región y la dirección de los ejes.

**STEP 6 - VARIOGRAM PARAMETERS**

Se necesita el archivo *Aditional File 1.csv* en el directorio de trabajo. Aquí, se calculan los parámetros de los modelos teóricos que mejor se ajustan a los variogramas experimentales de cada variable. Se utilizan los modelos experimental, Gaussiano y esférico. Se generan los archivos con los parámetros de cada modelo en *Rainfall Parameters.csv* para datos de lluvia y *Hurst Parameters.csv* para valores del exponente de Hurst.

**STEP 7 - KRIGING MAPS**

Se necesitan los archivos *Aditional File.csv*, *Area.csv*, *Rainfall Parameters.csv*, *Hurst Parameters.csv*. Se realiza los mapas de interpolación por medio del Kriging Ordinario para ambas variables. Los mapas presentan un gradiente de color para identificar las intensidad de cada variable. Además, se realiza una validación cruzada, donde se obtienen métricas como la media del error, el Mean Squared Prediction Error (MSPE), el Normalized Mean Square Error (NMSE), el coeficiente de determinación entre los datos observados y los predichos, y los predichos y los errores.

## Resultados

La localización de la región de estudio y de cada estación y la intensidad de las variables, lluvia media anual y el exponente de Hurst, se observan en la Fig.6. La información necesaria se encuentra en el archivo *Aditional File 1.csv*.

<p align="center">
  <img width="628" height="280" src="Images/Figure-6.png">
</p>
<p align="center">
    <em>Fig. 6 - Se identifica la intensidad de cada variable con un gradiente de color de tonalidades azules, donde los tonos claros indican mayor                   intensidad. </em>
</p>

La distribución de los datos originales de cada variable se observa en la Fig.7, junto a cada una de ellas, se encuentra la distribución de los datos transformados por medio de Logaritmo *Log*. A cada distribución, se calculó el coeficiente de asimetría (skewness), se pretende utilizar los datos con coeficiente más cercano a 0, es decir, más simétrica. 

<p align="center">
  <img width="618" height="678" src="Images/Figure-7.png">
</p>
<p align="center">
    <em>Fig. 7 - Para datos de lluvia originales (en la parte superior) se obtuvo un skewness de 0.33, y para los datos transformados de -0.92. Para los             datos originales del exponente de Hurst (en la parte inferior) se tiene un coeficiente de  -0.07, y de -1.03 para datos transformados. </em>
</p>

Por los valores de los coeficientes, se decide utilizar los valores originales de cada variable.

Ahora se pasa a hacer uso del mapa variográfico, en la Fig.8, dónde se establece el ángulo de los ejes de anisotropía, donde para ambas variables, se establece un ángulo de 130°. 

<p align="center">
  <img width="668" height="306" src="Images/Figure-8.png">
</p>
<p align="center">
    <em>Fig. 8 - Mapa variográfico de ambas variables, el la izquierda valores de lluvia y en la derecha del exponente de Hurst, donde se observa la                 anisotrpía de la región y el ángulo del eje donde la variación es mínima.  </em>
</p>

Una vez que se conoce la dirección, se pasa a realizar el variograma experimental de cada variable, y se ajusta a los modelos teóricos exponencial, Gausiano y esférico. Se utilizan los parámetros de dirección de _130°_ con una tolerancia de _40°_ , un rango maximo de _150000 metros_ y un total de _20_ lags para datos de lluvia, para el exponente de Hurst se utilizaron los parámetros con dirección de _130°_ con una tolerancia de _40°_ , un rango maximo de _100000 metros_ y un total de _25_ lags. En la Fig.9 se observan los variogramas. 

<p align="center">
  <img width="640" height="822" src="Images/Figure-9.png">
</p>
<p align="center">
    <em>Fig. 9 - Variogramas experimentales de valores de lluvia (izquierda) y exponente de Hurst (derecha) ajustados a modelos esféricos, Gaussianos y               esféricos.  </em>
</p>

Con estos variogramas, se decide aplicar el Kriging Ordinario para variogramás teóricos de modelo exponencial y gausiano. En la Fig.10 se observan los mapas interpolados de cada variable.

<p align="center">
  <img width="574" height="715" src="Images/Figure-10.png">
</p>
<p align="center">
    <em>Fig. 10 - En la parte superior se observan los mapas de lluvia para modelos exponencial y esférico, y en la parte inferior para el exponente de               Hurst.  </em>
</p>

## Discusión y conclusión

Los hallazgos muestran que las zonas que registran anti-persistencia y gran cantidad de lluvia, de acuerdo con la orografía, se localizan principalmente al pie de las montañas de la Eastern Sierra Madre (SMO). Otra característica de esta zona es la anisotropía de la antipersistencia (direccionalidad espacial a _130°_), indicada como una franja amarilla en la parte central de la región y que coincide con la abundante vegetación de la SMO. Esto implica que en esta franja llueve pocos días al año pero abundantemente, haciendo a estas áreas ideales para la recolección de agua, lo que justifica la localización de las presas; La Boca y Cerro Prieto. En contraste hay zonas con clima predominantemente árido, localizadas en dirección suroeste de la región a una altitud de _1600 masl_. Otra contribución de esta metodología es la identificación geográfica de zonas húmedas, con excelentes condiciones para la agricultura y ganadería.

De otra manera, las zonas con una menor cantidad de lluvia histórica, tiende a presentarse un exponente de Hurst persistente, haciendo las temporadas de lluvias extensas, pero de poca lluvia. Estos resultados pueden evitar la construcción de ciudades sin el debido control de inundaciones en estas zonas, la creación de lagos artificiales nacientes de zonas con lluvia anti-persistente a las otras zonas del área, o la construcción de presas para recaudar y aprovechar de una manera mas eficiente las condiciones de lluvia de estos lugares.
