# Ablation Study

-----------------------------------------------------------------------------------

## Modelo numero: 1

- Arquitectura: BonillaCNN base con tres bloques Conv2d-BatchNorm-ReLU, dos MaxPool, AdaptiveAvgPool 1x1 y clasificador lineal.
- Epocas entrenadas: 5
- Numero de parametros: 24,133
- Accuracy de validacion: 0.6140
- F1 macro de validacion: 0.5818
- Checkpoint usado: `output/20260822_205610/checkpoints/best.pt`

## Datos del modelo 1

| Params | Val accuracy | Train accuracy | Val F1 macro | Best.pt |
|---:|---:|---:|---:|---|
| 24,133 | 0.6140 | 0.5728 | 0.5818 | `output/20260822_205610/checkpoints/best.pt` |

## Conclusion del modelo 1

El modelo base completo las 5 epocas en CPU sin errores. Obtuvo 61.40% de accuracy exacta y 58.18% de F1 macro en validacion. La accuracy de entrenamiento reportada en la ultima epoca fue 57.28%; el hecho de que sea menor que validacion es coherente con el aumento aleatorio aplicado solo durante entrenamiento.

-----------------------------------------------------------------------------------

## Modelo numero: 2

- Arquitectura: BonillaCNN con tres bloques convolucionales, AdaptiveAvgPool 3x3 y clasificador 576-128-5 con ReLU y Dropout 0.25.
- Epocas entrenadas: 5
- Numero de parametros: 98,309
- Accuracy de validacion: 0.6570
- F1 macro de validacion: 0.6555
- Checkpoint usado: `output/20260822_210202/checkpoints/best.pt`

## Datos del modelo 2

| Params | Val accuracy | Train accuracy | Val F1 macro | Best.pt |
|---:|---:|---:|---:|---|
| 98,309 | 0.6570 | 0.6084 | 0.6555 | `output/20260822_210202/checkpoints/best.pt` |

## Conclusion del modelo 2

Se reemplazo el promedio adaptativo 1x1 por una salida 3x3 y se agrego un clasificador oculto con Dropout. Con respecto al Modelo 1, el accuracy subio 4.30 puntos porcentuales y el F1 macro subio 7.37 puntos. Conservar informacion espacial antes de clasificar produjo una mejora clara.

-----------------------------------------------------------------------------------

## Modelo numero: 3

- Arquitectura: BonillaCNN con cuatro bloques convolucionales (16-32-64-96 canales), AdaptiveAvgPool 2x2 y clasificador 384-128-5 con Dropout 0.25.
- Epocas entrenadas: 5
- Numero de parametros: 129,317
- Accuracy de validacion: 0.6540
- F1 macro de validacion: 0.6379
- Checkpoint usado: `output/20260822_210659/checkpoints/best.pt`

## Datos del modelo 3

| Params | Val accuracy | Train accuracy | Val F1 macro | Best.pt |
|---:|---:|---:|---:|---|
| 129,317 | 0.6540 | 0.6128 | 0.6379 | `output/20260822_210659/checkpoints/best.pt` |

## Conclusion del modelo 3

Se agrego un cuarto bloque convolucional de 96 canales. Frente al Modelo 2, el accuracy bajo 0.30 puntos porcentuales y el F1 macro bajo 1.76 puntos, aunque el AUROC subio de 0.8991 a 0.9019. La profundidad adicional no produjo una mejora global con solo 5 epocas, por lo que no se conserva en la siguiente version.

-----------------------------------------------------------------------------------

## Modelo numero: 4

- Arquitectura: se recupera la arquitectura efectiva del Modelo 2; se moderan los aumentos geometricos, de color, degradacion y recorte, y se agrega weight decay de 0.0001.
- Epocas entrenadas: 5
- Numero de parametros: 98,309
- Accuracy de validacion: 0.6930
- F1 macro de validacion: 0.6876
- Checkpoint usado: `output/20260822_211225/checkpoints/best.pt`

## Datos del modelo 4

| Params | Val accuracy | Train accuracy | Val F1 macro | Best.pt |
|---:|---:|---:|---:|---|
| 98,309 | 0.6930 | 0.6525 | 0.6876 | `output/20260822_211225/checkpoints/best.pt` |

## Conclusion del modelo 4

Se retiro la cuarta convolucion que no habia aportado mejora, se redujo la intensidad de los aumentos y se agrego una regularizacion L2 pequena. Frente al Modelo 3, el accuracy subio 3.90 puntos porcentuales y el F1 macro subio 4.97 puntos. Tambien supero al Modelo 2 por 3.60 y 3.21 puntos, respectivamente.

-----------------------------------------------------------------------------------

## Modelo numero: 5

- Arquitectura: arquitectura del Modelo 4 con Dropout 0.20 y scheduler cosenoidal de learning rate entre 0.001 y 0.0001 durante 5 epocas.
- Epocas entrenadas: 5
- Numero de parametros: 98,309
- Accuracy de validacion: 0.6960
- F1 macro de validacion: 0.6931
- Checkpoint usado: `output/20260822_211746/checkpoints/best.pt`

## Datos del modelo 5

| Params | Val accuracy | Train accuracy | Val F1 macro | Best.pt |
|---:|---:|---:|---:|---|
| 98,309 | 0.6960 | 0.6572 | 0.6931 | `output/20260822_211746/checkpoints/best.pt` |

## Conclusion del modelo 5

Se redujo el Dropout de 0.25 a 0.20 y se agrego una reduccion cosenoidal del learning rate para afinar los pesos al final. Frente al Modelo 4, el accuracy subio 0.30 puntos porcentuales, el F1 macro subio 0.55 puntos y el AUROC paso de 0.9123 a 0.9191. Esta version obtiene el mejor balance global y se selecciona como modelo final para generar `predictions.csv`.

-----------------------------------------------------------------------------------

## Modelo numero: 6

- Arquitectura: Modelo 5 con una segunda convolucion Conv2d-BatchNorm-ReLU de 64 canales en el bloque de alto nivel.
- Epocas entrenadas: 5
- Numero de parametros: 135,365
- Accuracy de validacion: 0.6800
- F1 macro de validacion: 0.6689
- Checkpoint usado: `output/20260822_222356/checkpoints/best.pt`

## Datos del modelo 6

| Params | Val accuracy | Train accuracy | Val F1 macro | Best.pt |
|---:|---:|---:|---:|---|
| 135,365 | 0.6800 | 0.6646 | 0.6689 | `output/20260822_222356/checkpoints/best.pt` |

## Conclusion del modelo 6

Se agrego una segunda convolucion de 64 canales para mejorar los rasgos semanticos de las clases animales. Frente al Modelo 5, el accuracy bajo 1.60 puntos porcentuales y el F1 macro bajo 2.42 puntos. La perdida mejoro de 0.7322 a 0.7156 y el AUROC de 0.9191 a 0.9196, pero el balance de clasificacion fue inferior; la capa adicional no se conserva.

-----------------------------------------------------------------------------------

## Modelo numero: 7

- Arquitectura: se recupera la arquitectura del Modelo 5 y se moderan nuevamente rotacion, afin, color, degradacion y recorte.
- Epocas entrenadas: 5
- Numero de parametros: 98,309
- Accuracy de validacion: 0.6900
- F1 macro de validacion: 0.6886
- Checkpoint usado: `output/20260822_222916/checkpoints/best.pt`

## Datos del modelo 7

| Params | Val accuracy | Train accuracy | Val F1 macro | Best.pt |
|---:|---:|---:|---:|---|
| 98,309 | 0.6900 | 0.6709 | 0.6886 | `output/20260822_222916/checkpoints/best.pt` |

## Conclusion del modelo 7

Se retiro la convolucion adicional y se redujo la intensidad de los aumentos para aprovechar mejor las 5 epocas. Frente al Modelo 6, el accuracy subio 1.00 punto porcentual y el F1 macro subio 1.97 puntos. Quedo 0.60 y 0.45 puntos por debajo del Modelo 5, aunque mejoro la perdida a 0.7142 y el AUROC a 0.9203.

-----------------------------------------------------------------------------------

## Modelo numero: 8

- Arquitectura: Modelo 7 con perdida CrossEntropy ponderada por clase; pesos `[1.0, 1.0, 1.0, 1.1, 1.25]` para airplane, bird, car, cat y dog.
- Epocas entrenadas: 5
- Numero de parametros: 98,309
- Accuracy de validacion: 0.6910
- F1 macro de validacion: 0.6908
- Checkpoint usado: `output/20260822_223420/checkpoints/best.pt`

## Datos del modelo 8

| Params | Val accuracy | Train accuracy | Val F1 macro | Best.pt |
|---:|---:|---:|---:|---|
| 98,309 | 0.6910 | 0.6783 | 0.6908 | `output/20260822_223420/checkpoints/best.pt` |

## Conclusion del modelo 8

Se ponderaron moderadamente `cat` y `dog`, las clases con menor recall en el Modelo 7. Frente al Modelo 7, el accuracy subio 0.10 puntos porcentuales, el F1 macro subio 0.22 puntos, la perdida bajo de 0.7142 a 0.7099 y el AUROC subio de 0.9203 a 0.9208. Aunque el Modelo 5 conserva el mayor accuracy y F1 global, el Modelo 8 obtiene la mejor perdida y el mejor AUROC de las ocho iteraciones.

-----------------------------------------------------------------------------------
