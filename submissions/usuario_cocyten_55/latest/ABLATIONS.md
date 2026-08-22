# Ablations - Challenge STL-5

## Experiment 1: Model Selection

**Model**: ResNet-18 preentrenado en ImageNet.

## Experiment 2: Training Strategy

**Strategy**: Sondeo Lineal (linear probe).

- Solo la cabeza (fc) entrenable

- Backbone congelado

## Experiment 3: Hyperparameters

- **Image Size**: 224x224

- **Batch Size**: 64

- **Épocas**: 10

- **Optimizer**: Adam (lr=0.001)

- **Weight Decay**: 0.0001

## Experiment 4: Data Preprocessing

- Mean/Std: \[0.485, 0.456, 0.406\] / \[0.229, 0.224, 0.225\]

- Augmentation: HorizontalFlip, Rotation, ColorJitter

## Ablation Results

| Experiment | Accuracy | F1 |
| - | - | - |
| Linear Probe (5 epochs) | 86.90% | 86.77% |
| Linear Probe (10 epochs) | 88.60% | 88.65% |


## Conclusiones

Los experimentos muestran que extender el entrenamiento a 10 épocas con un tamaño de lote (*batch size*) de 64 mejora la precisión en un 1,70 %. Por otra parte, Transfer Learning con ResNet-18 mejora significativa al usar GPU RTX 3060 (batch\_size=64, 10 épocas). El modelo tiene alta precisión pero baja eficiencia (11M parámetros).
