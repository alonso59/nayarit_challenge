# Ablation Study

## Modelo final

- Arquitectura: SimpleCNN — 4 capas Conv2d(3x3)+BatchNorm2d+ReLU+MaxPool2d (canales 3->16->32->64->64), seguido de AdaptiveAvgPool2d(1), Dropout(0.3) y una capa Linear(64->5).
- Numero de parametros: 61,189
- Accuracy de validacion: 0.7160
- F1 macro de validacion: 0.7130
- Checkpoint usado: output/20260711_150827/checkpoints/best.pt

## Experimentos

| Experimento   | Cambio                              | Params | Val accuracy | Val F1 macro | Comentario                                                                                                          |
| ------------- | ----------------------------------- | -----: | -----------: | -----------: | ------------------------------------------------------------------------------------------------------------------- |
| Baseline      | 5 epocas, con aumentos de datos     | 61,189 |       0.6340 |       0.6140 | El modelo aun no convergia; la curva de loss/accuracy seguia moviendose activamente en la epoca 5.                  |
| Experimento 1 | 18 epocas, mismos aumentos de datos | 61,189 |       0.7160 |       0.7130 | Accuracy sube +8.2 puntos y F1 macro +9.9 puntos respecto al baseline, dandole mas tiempo al modelo para converger. |
| Experimento 2 | 18 épocas, sin aumentos de datos  | 61,189 |       0.7560 |       0.7529 | Accuracy sube +4.0 puntos adicionales respecto al Experimento 1, al quitar los aumentos de datos                    |


## Conclusion

La decision con mayor impacto fue aumentar las epocas de 5 a 18 (+8.2 puntos de accuracy). Un hallazgo adicional fue que, con solo 18 epocas, el modelo sin aumentos de datos obtuvo mejor accuracy de validacion (0.7560) que el modelo con aumentos (0.7160), probablemente porque los aumentos necesitan mas tiempo de entrenamiento para mostrar su beneficio. Aun asi, se eligio el modelo con aumentos como final, ya que el objetivo del reto es generalizar a test (no solo a validacion), y los aumentos favorecen esa generalizacion.
