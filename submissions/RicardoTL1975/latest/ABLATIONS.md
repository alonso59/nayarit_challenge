# Ablation Study

## Final model

- Architecture: ImprovedCNN with three convolution layers, Batch Normalization, SiLU, pooling, global average pooling, dropout, and a five-class linear output.
- Trainable parameters: 94,117
- Parameter constraint below 95,000: PASS
- Best validation accuracy: 0.7990
- Best validation macro F1: 0.7989
- Best validation EMA epoch: 49
- Final labeled training samples: 4,000
- Test-time augmentation: five translated views plus horizontal flips

## Experiments

| Experiment | Main change | Validation result |
|---|---|---|
| Baseline | Original SimpleCNN, 5 epochs, no augmentation | Acc 0.5550, F1 0.5436 |
| Baseline extension | Original SimpleCNN with adjusted epochs/LR | Acc 0.5770, F1 0.5615 |
| Final model | BatchNorm, EMA, augmentation, AdamW, cosine schedule, label smoothing | Acc 0.7990, F1 0.7989 |

## Notes

The final EMA checkpoint was selected by validation macro F1. After model selection, a fresh model was trained with all labeled train and validation images. Hidden test labels were not used.
