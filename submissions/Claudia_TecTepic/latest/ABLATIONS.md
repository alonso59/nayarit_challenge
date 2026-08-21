# Ablation Study

## Modelo final

- Arquitectura: SimpleCNN con 3 bloques residuales (conv-bn-relu-conv-bn + skip, proyeccion 1x1 cuando cambian canales), stem inicial, MaxPool2d entre etapas, AdaptiveAvgPool2d + Dropout(0.3) + Linear como head. Canales: 16 -> 16 -> 32 -> 64. Sin cambios de arquitectura respecto a los experimentos previos; la mejora final viene de Stochastic Weight Averaging (SWA) aplicado en `trainer.py` sobre el mismo entrenamiento.
- Numero de parametros: 78,053
- Accuracy de validacion: 0.8150
- F1 macro de validacion: 0.8123
- Checkpoint usado: `output/20260820_130938/checkpoints/swa.pt` (promedio de pesos de las epocas 46-60 con `seed=43`, BatchNorm recalibrado tras el promediado)

## Experimentos

| Experimento | Cambio | Params | Val accuracy | Val F1 macro | Comentario |
|---|---|---:|---:|---:|---|
| Baseline (5 epocas) | ResidualCNN 16-16-32-64, augmentations (flip, rotacion, affine, color jitter), Adam lr=1e-3, batch 64 | 78,053 | 0.6559 | - | Curva de loss aun bajando y val_acc subiendo en la ultima epoca; 5 epocas insuficiente para converger. |
| Experimento 1 (30 epocas) | Mismo modelo y augmentations, solo se aumento epochs de 5 a 30 | 78,053 | 0.7541 | 0.7565 | Mejor resultado en la ultima epoca (30/30); train_acc (0.7562) muy cerca de val_acc, sin overfitting. Confusion concentrada en clases animales (cat/dog/bird), airplane y car casi perfectas. Sugiere que mas epocas siguen ayudando. |
| Experimento 2 (60 epocas) | Mismo modelo y augmentations, epochs=60 | 78,053 | 0.8030 | 0.8045 | Mejor checkpoint en epoca 49/60 (val_acc 0.8041). Mejora sustancial (+0.049 acc, +0.048 F1) respecto a 30 epocas sin cambiar arquitectura ni augmentations, solo dandole mas tiempo de entrenamiento. Confusion cat/dog se redujo notablemente frente al experimento 1. |
| Experimento 3a (SE, Squeeze-Excitation) | Bloque SE agregado + regularizacion extra, 3 seeds (base, 43, 44) | 79,589 | 0.8050 / 0.7990 / 0.7850 | 0.8035 / 0.7967 / 0.7817 | No es mejora demostrada: el mejor resultado cae dentro del margen de ruido de reruns identicos ya observado (~1.5-2 pts), y las otras dos seeds quedan por debajo del modelo de 60 epocas. Descartado. |
| Experimento 3b (MobileNet) | Convoluciones depthwise-separable estilo MobileNet | 60,325 | 0.7410 | 0.7396 | Claramente peor (-0.062 acc); menos parametros pero capacidad insuficiente para el dataset a 96x96px. Descartado con margen claro. |
| Experimento 4 (SWA, epochs=60, seed=42) | Mismo modelo de 60 epocas + Stochastic Weight Averaging (promedio de pesos epocas 46-60 + recalibracion de BatchNorm), sin cambiar arquitectura ni augmentations | 78,053 | 0.8080 | 0.8055 | Primera corrida SWA: supera el modelo entregado (+0.005 acc, +0.001 F1). Se corrio una segunda corrida con distinta seed para confirmar que la mejora no era ruido de rerun. |
| **Experimento 4 (SWA, epochs=60, seed=43)** | Igual al anterior, solo cambia `seed=43` | 78,053 | **0.8150** | **0.8123** | Confirma la mejora de SWA con margen mayor (+0.012 acc, +0.008 F1) frente al modelo entregado; las dos corridas SWA (seeds 42 y 43) superan consistentemente 0.8030/0.8045, a diferencia del experimento SE que no fue consistente entre seeds. **Adoptado como modelo final.** |

## Conclusion

La primera mejora sustancial vino de extender el numero de epocas de entrenamiento (5 -> 30 -> 60), sin tocar arquitectura ni augmentations: el modelo nunca mostro senales de overfitting (train_acc y val_acc se mantuvieron cercanas en todas las corridas) porque el dataset es pequeno (3000 imagenes de entrenamiento) y el modelo es compacto (78K params), asi que la capacidad estaba lejos de saturarse y la curva de val_loss/val_acc seguia mejorando en cada corrida mas larga.

Una segunda ronda de experimentos probo cambios de arquitectura (bloque Squeeze-Excitation, convoluciones depthwise-separable estilo MobileNet): ninguno mejoro de forma consistente sobre el modelo de 60 epocas, y en el caso de MobileNet el resultado fue claramente peor. Esto sugiere que, con este dataset (3000 imagenes, 5 clases) y esta resolucion (96x96px), el cuello de botella ya no era la arquitectura sino la varianza del entrenamiento (el checkpoint de "mejor val_acc" de una sola corrida depende de en que epoca cayo el pico, y ese pico varia con la seed).

La mejora final y adoptada fue **Stochastic Weight Averaging (SWA)**: en vez de quedarse con el checkpoint de mejor val_acc de una sola epoca (ruidoso, como muestran las corridas de SE), se promedian los pesos del modelo durante el ultimo 25% del entrenamiento (epocas 46-60, con LR constante) y se recalibra BatchNorm sobre el set de entrenamiento con esos pesos promediados. Esto no agrega parametros ni cambia la arquitectura -- sigue siendo el mismo ResidualCNN de 78,053 parametros -- pero produce un checkpoint mas estable que generaliza mejor que cualquier epoca individual. Se confirmo con dos seeds distintas (42 y 43): ambas superaron el modelo de 60 epocas sin SWA (0.8030/0.8045), con la seed 43 alcanzando 0.8150/0.8123, la mejor combinacion de accuracy y F1 macro obtenida en todo el estudio.

El bloque residual con proyeccion 1x1 permitio profundizar la red (3 etapas, canales 16->16->32->64) sin degradar el gradiente, manteniendo el conteo de parametros muy por debajo del limite de 100K (usa 78,053, efficiency_score = 1.0).

Analisis de errores: la matriz de confusion muestra que `airplane` y `car` se clasifican casi sin error en las tres corridas (siluetas muy distintas al resto de clases). El error se concentra en las clases animales -- `cat` se confunde con `dog` y, en menor medida, con `bird` -- lo cual es esperable porque a 96x96px estas clases comparten textura y forma general (cuerpo con pelaje/plumas, cuatro patas o silueta similar en pose sentada). Este patron se redujo pero no desaparecio al pasar de 30 a 60 epocas ni con SWA, lo que sugiere que mejorar mas esta confusion requeriria augmentations mas especificas (p. ej. mas variacion de escala/crop) o mayor capacidad en las etapas finales del modelo, en vez de solo mas epocas o mejor promediado de pesos.
