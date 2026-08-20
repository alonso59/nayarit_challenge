# Ablation Study

## Modelo final

- Arquitectura: SimpleCNN con 3 bloques residuales (conv-bn-relu-conv-bn + skip, proyeccion 1x1 cuando cambian canales), stem inicial, MaxPool2d entre etapas, AdaptiveAvgPool2d + Dropout(0.3) + Linear como head. Canales: 16 -> 16 -> 32 -> 64.
- Numero de parametros: 78,053
- Accuracy de validacion: 0.8030
- F1 macro de validacion: 0.8045
- Checkpoint usado: output/20260818_103429/checkpoints/best.pt (mejor val_acc, epoca 49 de 60)

## Experimentos

| Experimento | Cambio | Params | Val accuracy | Val F1 macro | Comentario |
|---|---|---:|---:|---:|---|
| Baseline (5 epocas) | ResidualCNN 16-16-32-64, augmentations (flip, rotacion, affine, color jitter), Adam lr=1e-3, batch 64 | 78,053 | 0.6559 | - | Curva de loss aun bajando y val_acc subiendo en la ultima epoca; 5 epocas insuficiente para converger. |
| Experimento 1 (30 epocas) | Mismo modelo y augmentations, solo se aumento epochs de 5 a 30 | 78,053 | 0.7541 | 0.7565 | Mejor resultado en la ultima epoca (30/30); train_acc (0.7562) muy cerca de val_acc, sin overfitting. Confusion concentrada en clases animales (cat/dog/bird), airplane y car casi perfectas. Sugiere que mas epocas siguen ayudando. |
| Experimento 2 (60 epocas) | Mismo modelo y augmentations, epochs=60 | 78,053 | 0.8030 | 0.8045 | Mejor checkpoint en epoca 49/60 (val_acc 0.8041). Mejora sustancial (+0.049 acc, +0.048 F1) respecto a 30 epocas sin cambiar arquitectura ni augmentations, solo dandole mas tiempo de entrenamiento. Confusion cat/dog se redujo notablemente frente al experimento 1. |

## Conclusion

La decision que mas mejoro el modelo fue simplemente extender el numero de epocas de entrenamiento (5 -> 30 -> 60), sin tocar arquitectura ni augmentations: el modelo nunca mostro senales de overfitting (train_acc y val_acc se mantuvieron cercanas en todas las corridas) porque el dataset es pequeno (3000 imagenes de entrenamiento) y el modelo es compacto (78K params), asi que la capacidad estaba lejos de saturarse y la curva de val_loss/val_acc seguia mejorando en cada corrida mas larga.

El bloque residual con proyeccion 1x1 permitio profundizar la red (3 etapas, canales 16->16->32->64) sin degradar el gradiente, manteniendo el conteo de parametros muy por debajo del limite de 100K (usa 78,053, efficiency_score = 1.0).

Analisis de errores: la matriz de confusion muestra que `airplane` y `car` se clasifican casi sin error en las tres corridas (siluetas muy distintas al resto de clases). El error se concentra en las clases animales -- `cat` se confunde con `dog` y, en menor medida, con `bird` -- lo cual es esperable porque a 96x96px estas clases comparten textura y forma general (cuerpo con pelaje/plumas, cuatro patas o silueta similar en pose sentada). Este patron se redujo pero no desaparecio al pasar de 30 a 60 epocas, lo que sugiere que mejorar mas esta confusion requeriria augmentations mas especificas (p. ej. mas variacion de escala/crop) o mayor capacidad en las etapas finales del modelo, en vez de solo mas epocas.
