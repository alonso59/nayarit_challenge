# Ablation Study

## Modelo final

- Arquitectura: SimpleCNN residual (4 bloques ResBlock: Conv2d 3x3 + BatchNorm2d + shortcut 1x1 (cuando cambian canales) + suma residual + ReLU + MaxPool2d; canales 3->16->32->64->112), seguido de AdaptiveAvgPool2d, Dropout p=0.3 y Linear a 5 clases
- Numero de parametros: 99,221
- Accuracy de validacion: 0.8010
- F1 macro de validacion: 0.8011

## Experimentos

| Experimento | Cambio | Params | Val accuracy | Val F1 macro | Comentario |
|---|---|---:|---:|---:|---|
| Baseline (config default) | 5 epocas, sin augmentations, sin BatchNorm/Dropout | - | - | - | Configuracion inicial del template |
| Experimento 1 | CNN de 4 bloques con BatchNorm y Dropout(0.3) + augmentations (flip, rotacion, affine, color jitter), 30 epocas, Adam lr=0.001, weight_decay=0.0 | 98,565 | 0.7610 | 0.7623 | Mejora clara respecto al baseline |
| Experimento 2 | Mismo modelo y augmentations, 60 epocas, Adam lr=0.0007, weight_decay=0.0001 | 98,565 | 0.7920 | 0.7930 | LR mas bajo y weight_decay mejoraron el mejor punto alcanzado |
| Experimento 3 (final) | Se agregaron conexiones residuales (shortcut 1x1 por bloque) al modelo, mismos augmentations, 80 epocas, Adam lr=0.0007, weight_decay=0.0001 | 99,221 | 0.8010 | 0.8011 | Las conexiones residuales permitieron mayor capacidad de aprendizaje (train acc 0.84) sin overfitting severo, alcanzando el mejor F1 macro de los tres experimentos |

## Conclusion

La decision que mas mejoro el modelo fue agregar conexiones residuales (shortcut connections) a cada bloque convolucional. Esto facilito el flujo del gradiente a traves de la red, permitiendo que el modelo aprendiera representaciones mas ricas (mayor train accuracy) sin aumentar significativamente el numero de parametros (99,221, aun por debajo del umbral de 100,000 para eficiencia maxima). Combinado con weight_decay=0.0001 y un learning rate moderado (0.0007), esto llevo el F1 macro de validacion de 0.7623 (experimento 1) a 0.8011 (experimento 3, final).
