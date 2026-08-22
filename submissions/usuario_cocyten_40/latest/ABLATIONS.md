# Ablation Study

## Modelo final
- Arquitectura: SimpleCNN (3 bloques Conv+BatchNorm+ReLU+MaxPool, AdaptiveAvgPool, Dropout 0.3)
- Numero de parametros: 94341
- Optimizador: adam
- Learning rate: 0.001
- Epocas: 5
- Tamano de imagen: 96
- Checkpoint usado: output/20260822_012858/checkpoints/best.pt

## Metricas de validacion (src/eval.py)
```
accuracy: 0.6820
precision_macro: 0.6887
sensitivity_macro: 0.6820
specificity_macro: 0.9205
f1_macro: 0.6827
loss: 0.8116
auroc_macro: 0.9060
```

## Experimentos (historial de corridas en esta notebook)
| # | Epocas | LR | Optimizador | Image size | Params |
|---|---|---|---|---|---|
| 1 | 5 | 0.001 | adam | 96 | 94341 |
| 2 | 5 | 0.001 | adam | 96 | 94341 |

## Conclusion
Se obtuvo un accuracy de 0.682 y un F1 macro de 0.6827. El modelo aún puede mejorar entrenando más épocas, ya que el F1 macro es lo que más pesa en el score final.
