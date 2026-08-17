# Ablation Study

## Modelo final

- Arquitectura: SimpleCNN con 3 bloques Conv2d + BatchNorm2d + ReLU + MaxPool2d y AdaptiveAvgPool2d
- Numero de parametros: 94341
- Accuracy de validacion: 0.6740
- F1 macro de validacion: 0.6641
- AUROC macro: 0.9069
- Epoca del mejor checkpoint: 4

## Experimentos

| Experimento | Cambio | Params | Val accuracy | Val F1 macro | Comentario |
|---|---|---:|---:|---:|---|
| Baseline | CNN de 3 convoluciones, sin BatchNorm | 93893 | 0.5590 | 0.5506 | Modelo inicial |
| Experimento 1 | CNN + aumentos de datos | 93893 | 0.5540 | 0.5247 | No mejoro respecto al baseline |
| Experimento 2 | CNN + BatchNorm2d | 94341 | 0.6740 | 0.6641 | Mejor resultado obtenido |

## Conclusion

La incorporacion de BatchNorm2d fue la decision de diseno que produjo la mayor mejora.
El modelo final alcanzo 0.6740 de accuracy y 0.6641 de F1 macro en la particion de validacion.
