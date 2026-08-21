# Ablation Study

## Modelo final

- Arquitectura: CNN con bloques convolucionales 24 -> 40 -> 64 -> 96, BatchNorm, ReLU, MaxPool, AdaptiveAvgPool y Dropout.
- Numero de parametros: 88,781
- Accuracy de validacion: 0.6590
- F1 macro de validacion: 0.6491
- AUROC macro: 0.9091

## Experimentos

| Experimento | Cambio | Params | Val accuracy | Val F1 macro | Comentario |
|---|---|---:|---:|---:|---|
| Baseline | CNN 32 -> 64 -> 128 | 94,341 | 0.6730 | 0.6661 | Mejor rendimiento de validacion |
| Experimento 2 | CNN 24 -> 40 -> 64 -> 96 | 88,781 | 0.6590 | 0.6491 | Menor numero de parametros |

## Conclusion

El Experimento 2 redujo el numero de parametros de 94,341 a 88,781 respecto al baseline.
Aunque el baseline obtuvo mejores metricas de validacion, el Experimento 2 mantuvo un rendimiento competitivo con una arquitectura mas compacta.

El modelo final seleccionado para la entrega es el Experimento 2.
