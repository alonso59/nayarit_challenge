# Ablation Study

## Modelo final

- Arquitectura: CNN mejorada de 4 bloques convolucionales con Batch Normalization, ReLU, MaxPooling, Adaptive Average Pooling y Dropout.
- Data augmentation: RandomCrop, RandomHorizontalFlip y ColorJitter.
- Optimizador: Adam.
- Learning rate: 0.001 (o 0.0007 si se aplicó el parche extra).
- Weight decay: 0.0001.
- Accuracy de validación: 0.8170
- F1 macro de validación: 0.8144
- Checkpoint usado: /content/NAYARIT_BASE_CNN/output/20260820_180943/checkpoints/best.pt

## Experimentos

| Experimento | Cambio | Val accuracy | Val F1 macro | Comentario |
|---|---|---:|---:|---|
| Baseline | CNN 3 capas, 5 épocas, lr 0.001 | 0.5550 | 0.5436 | Modelo base |
| Exp. anterior | lr 0.0005, 5 épocas | 0.5150 | 0.5037 | No mejoró |
| Modelo parchado | Augmentation + BatchNorm + Dropout + CNN 4 bloques + más épocas | 0.8170 | 0.8144 | Resultado real de esta ejecución |

## Conclusión

El cambio aislado del learning rate no produjo una mejora consistente. El modelo final incorpora regularización, aumento de datos y una arquitectura convolucional con mayor capacidad. Las métricas reportadas corresponden a la evaluación real del checkpoint `best.pt`.
