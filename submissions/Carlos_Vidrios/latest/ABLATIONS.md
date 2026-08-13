# Ablation Study

## Alumno: Carlos Alberto Vidrios Serrano

## Modelo final

- Arquitectura:
----
----
| Layer (type:depth-idx) | Input Shape | Output Shape | Param |
|---|---|---:|---:|---:|---|
| SimpleCNN | [1, 3, 96, 96] |  [1, 5] | -- |
| ├─Conv2d: 1-1 | [1, 3, 96, 96] | [1, 32, 96, 96] | 896 |
| ├─BatchNorm2d: 1-2 | [1, 32, 96, 96] | [1, 32, 96, 96] | 64 |
| ├─ReLU: 1-3 | [1, 32, 96, 96] | [1, 32, 96, 96] | -- |
| ├─MaxPool2d: 1-4 | [1, 32, 96, 96] | [1, 32, 48, 48] | -- |
| ├─Conv2d: 1-5 | [1, 32, 48, 48] | [1, 64, 48, 48] | 18,496 |
| ├─BatchNorm2d: 1-6 | [1, 64, 48, 48] | [1, 64, 48, 48] | 128 |
| ├─ReLU: 1-7 | [1, 64, 48, 48] | [1, 64, 48, 48] | -- |
| ├─MaxPool2d: 1-8 | [1, 64, 48, 48] | [1, 64, 24, 24] | -- |
| ├─Conv2d: 1-9 | [1, 64, 24, 24] | [1, 128, 24, 24] | 73,856 |
| ├─BatchNorm2d: 1-10 | [1, 128, 24, 24] | [1, 128, 24, 24] | 256 |
| ├─ReLU: 1-11 | [1, 128, 24, 24] | [1, 128, 24, 24] | -- |
| ├─MaxPool2d: 1-12 | [1, 128, 24, 24] | [1, 128, 12, 12] | -- |
| ├─Conv2d: 1-13 | [1, 128, 12, 12] | [1, 256, 12, 12] | 295,168 |
| ├─BatchNorm2d: 1-14 | [1, 256, 12, 12] | [1, 256, 12, 12] | 512 |
| ├─ReLU: 1-15 | [1, 256, 12, 12] | [1, 256, 12, 12] | -- |
| ├─MaxPool2d: 1-16 | [1, 256, 12, 12] | [1, 256, 6, 6] | -- | 
| ├─AdaptiveAvgPool2d: 1-17 | [1, 256, 6, 6] | [1, 256, 1, 1] | -- |
| ├─Flatten: 1-18 | [1, 256, 1, 1] | [1, 256] | -- |
| ├─Linear: 1-19 | [1, 256] | [1, 512] | 131,584 |
| ├─ReLU: 1-20 | [1, 512] | [1, 512] | -- |
| ├─Dropout: 1-21 | [1, 512] | [1, 512] | -- |
| ├─Linear: 1-22 | [1, 512] | [1, 5] | 2,565 |



- Numero de parametros: 523,525
- Accuracy de validacion: 0.7970
- F1 macro de validacion: 0.7955
- Checkpoint usado: best.pt

## Experimentos

| Experimento | Cambio | Params | Val accuracy | Val F1 macro | Comentario |
|---|---|---:|---:|---:|---|
| Baseline | | 523,525 | 0.6600 | 0.6347 | 5 epocas de entrenamiento sin augmentation |
| Experimento 1 | Aumento a 50 epocas de entrenamiento | 523,525 | 0.8293 | 0.8219 | Entrenamiento sin augmentation, loss 1.2566|
| Experimento 2 | 50 epocas de entrenamiento, con augmentation | 523,525 | 0.7650 | 0.7593 | loss 0.8912|
| Experimento 3 | 100 epocas de entrenamiento con augmentation | 523,525 | 0.8070 | 0.8051 | loss 0.5854 
|Experimento 4 | 92 epocas de entrenamiento con augmentation | 523,525 | 0.8090 | 0.8109 | loss 0.5147

## Conclusiones

Para la implementación del modelo de clasificación basado en redes neuronales convolucionales (CNN), se tomó como punto de partida una arquitectura previamente reportada en la literatura especializada. La adopción de este modelo permitió establecer una estructura inicial para la red, la cual posteriormente fue adaptada y evaluada de acuerdo con las características particulares del conjunto de datos empleado en el presente proyecto. A partir de esta arquitectura base, se realizó un proceso experimental orientado a determinar las condiciones de entrenamiento que permitieran obtener el mejor desempeño de clasificación.

Como parte del proceso de optimización, se realizaron diferentes pruebas modificando principalmente el número de épocas de entrenamiento y las técnicas de _data augmentation_ aplicadas al conjunto de imágenes. Estas pruebas permitieron analizar el comportamiento del modelo tanto durante el aprendizaje como en la etapa de validación, buscando alcanzar un equilibrio entre la capacidad de aprendizaje de la red y su capacidad de generalización ante datos no utilizados directamente durante el entrenamiento.

Los resultados obtenidos mostraron que el desempeño del modelo presentó una mejora durante las primeras etapas del entrenamiento. Posteriormente, el mejor desempeño se obtuvo alrededor de la época 92, donde se alcanzó una precisión de validación de 80.90%, acompañada de un _loss_ de 0.5147. Aunque se realizaron pruebas con hasta 100 épocas de entrenamiento, después de aproximadamente la época 92 se observó un deterioro en el comportamiento del modelo, caracterizado por un incremento de la función de pérdida y una menor capacidad de generalización sobre los datos de validación.

Este comportamiento es consistente con la presencia de un proceso de **sobreajuste (_overfitting_)**, en el cual el modelo continúa ajustándose a las características específicas de los datos de entrenamiento sin obtener mejoras equivalentes en su desempeño sobre datos no observados. En este sentido, la selección de la época 92 como punto de referencia para el modelo final se justifica no únicamente por presentar la mayor precisión de validación observada, sino también por mostrar un valor de _loss_ considerablemente menor que el obtenido en etapas anteriores. El menor _loss_ indica una mejor correspondencia entre las probabilidades asignadas por el modelo y las clases reales, evitando en mayor medida predicciones excesivamente confiadas en casos incorrectos.

En conjunto, los experimentos realizados permitieron establecer una configuración de la CNN con un desempeño de aproximadamente 80.90 % de precisión sobre el conjunto de validación. Los resultados demuestran que la selección de la arquitectura, las técnicas de aumento de datos y, particularmente, el número de épocas de entrenamiento tienen una influencia significativa en la capacidad de generalización del modelo. Por lo tanto, el proceso experimental realizado permitió identificar una configuración adecuada para el problema de clasificación planteado y establecer evidencia de que un mayor número de épocas de entrenamiento no necesariamente implica un mejor desempeño del modelo.