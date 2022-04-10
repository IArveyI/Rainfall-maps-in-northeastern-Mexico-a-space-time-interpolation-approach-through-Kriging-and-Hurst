# Rainfall maps in northeastern Mexico a space time interpolation approach through Kriging and Hurst

Este repositorio está hecho con el propósito lograr la reproducibilidad de la metodología aplicada en el artículo : "Rainfall maps in northeastern Mexico a space time interpolation approach through Kriging and Hurst".  Para conocer más detalles técnicos visitar: '**Link del artículo**'

## Objetivo 

La región de estudio es la cuenca del Rio San Juan ubicada en el noreste de México, entre los estados de Coahuila, Nuevo León y Tamaulipas. Actualmente, existe una escazes de agua en esta zona, por lo que se realiza un análisis geoespacial con interpolación de Kriging, mostrando el comportamiento de la zona en base a la cantidad promedio anual de lluvia y su comportamiento histórico de  persistencia o anti-persistencia utilizando el exponente de Hurst.

## Marco teórico

Los datos observados son mediciones de la cantidad de lluvia en distintos puntos de una región específica. La correlación espacial del campo escalar $Z$ como función de la distancia se conoce como *variograma* o *semivariograma*. En aclaración, aunque variograma y semivariograma son comúnmente utilizaos indistintamente, realmente pueden aportar ciertas diferencias, por ello usar el término variograma insta a realizar un cálculo completo en vez de uno parcial que es representado en el semivariograma [1].

Considere dos puntos con vectores de posición **_x_** y **_x+h_**, respectivamente, ver la Fig. 1.

<p align="center">
  <img width="460" height="300" src="Images/Figure-1.jpg">
</p>




```mermaid
graph LR
A[Square Rect] -- Link text --> B((Circle))
A --> C(Round Rect)
B --> D{Rhombus}
C --> D
```
