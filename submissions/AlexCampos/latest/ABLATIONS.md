# Ablation Study

## Modelo final

- Arquitectura: `SimpleCNN` — CNN convolucional con 4 etapas (stem, stage2, un bloque
  residual, stage4) + global average pooling + dropout + capa lineal. Usa `Conv2d`,
  `BatchNorm2d`, `ReLU`, `MaxPool2d`, `AdaptiveAvgPool2d`, `Dropout` y un bloque
  residual (dos convoluciones 3x3 con skip connection).
- Numero de parametros: 94,973
- Accuracy de validacion: 0.8010
- F1 macro de validacion: 0.8015
- Checkpoint usado: `output/20260723_112220/checkpoints/best.pt` (epoca 30)

## Experimentos

| Experimento | Cambio | Params | Val accuracy | Val F1 macro | Comentario |
|---|---|---:|---:|---:|---|
| Baseline | CNN residual, augmentations moderadas (flip horizontal, rotacion +-10, affine leve, color jitter), Adam lr=0.001, weight_decay=0.0, 5 epocas | 94,973 | 0.6170 | 0.6098 | El modelo no habia convergido; val accuracy seguia subiendo al terminar el entrenamiento |
| Experimento 1 | Misma arquitectura y augmentations, 30 epocas (6x mas entrenamiento), lr fijo 0.001 | 94,973 | 0.7790 | 0.7796 | +16.2 pts accuracy y +17.0 pts F1 macro vs baseline. Cierta inestabilidad entre epocas (caidas puntuales de val accuracy en epocas 4, 20, 21, 29), consistente con learning rate fijo sin scheduler |
| Experimento 2 | Igual que Experimento 1 pero con scheduler CosineAnnealingLR (lr baja de 0.001 a ~0.00001 a lo largo de las 30 epocas) | 94,973 | 0.7920 | 0.7927 | +1.3 pts accuracy y +1.3 pts F1 macro vs Experimento 1. Mejora mas importante: las ultimas 10 epocas son mucho mas estables (val accuracy entre 0.76-0.79 sin saltos bruscos), en vez del ruido que se veia con lr fijo |
| Experimento 3 | Igual que Experimento 2 pero con augmentations reforzadas: ColorJitter mas fuerte (brightness/contrast/saturation 0.25, + hue 0.05) y RandomErasing (p=0.25) para atacar la confusion cat/dog identificada en la matriz de confusion | 94,973 | 0.8010 | 0.8015 | +0.9 pts accuracy y +0.9 pts F1 macro vs Experimento 2. Mejora mas modesta que las anteriores pero consistente en todas las metricas (tambien mejoro AUROC y loss final) |

## Analisis de errores

La matriz de confusion del Experimento 1 muestra:

- `airplane` y `car` se clasifican casi perfectamente, con muy pocos errores.
- `bird` tiene buen desempeno pero se confunde ocasionalmente con `cat`.
- `cat` y `dog` son el par mas dificil: el modelo confunde sistematicamente estas
  dos clases entre si. `dog` es la clase con menor recall de las cinco.

Esto sugiere que el modelo aprende bien formas y contextos rigidos (aviones,
autos), pero le cuesta mas diferenciar texturas finas entre mamiferos de
apariencia similar a 96x96 px.

## Conclusion

La decision que mas mejoro el modelo fue entrenar mas epocas (de 5 a 30),
sin cambiar arquitectura ni augmentations: el F1 macro paso de 0.6098 a
0.7796 (+17 pts). Agregar un scheduler de learning rate (coseno) aporto
una mejora adicional (+1.3 pts de F1 macro) principalmente al estabilizar
el entrenamiento en sus ultimas epocas. Finalmente, reforzar las
augmentations (mas ColorJitter + RandomErasing) sumo otra mejora (+0.9 pts de F1 macro),
llevando el modelo a 0.8015 de F1 macro en validacion.

En conjunto, las tres mejoras fueron acumulativas y cada una aporto en un
frente distinto: capacidad de aprendizaje (mas epocas), estabilidad de
convergencia (scheduler) y generalizacion/regularizacion (augmentations).

Al comparar la matriz de confusion del Experimento 3 contra la del
Experimento 2, la confusion entre `cat` y `dog` no desaparecio, sigue
siendo el par mas dificil del dataset, aunque el F1 global mejoro un poco.
Esto sugiere que reforzar color/regularizacion ayuda de forma general, pero
no ataca directamente el problema: separar cat/dog probablemente requiere
mas capacidad en las capas que capturan texturas finas (pelaje, forma de
orejas/hocico), no solo mas regularizacion. Queda como linea de trabajo
futura: aumentar canales en las ultimas capas convolucionales manteniendo
el conteo de parametros bajo 100k, o probar weight_decay si en
entrenamientos mas largos aparece mayor separacion entre train y val
accuracy.
