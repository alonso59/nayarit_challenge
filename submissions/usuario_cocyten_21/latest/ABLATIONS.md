# Ablation Study

## Arquitectura
CNN simple con 2 bloques convolucionales (16 -> 32 canales), cada uno
con ReLU y MaxPool(2), seguido de una capa Linear final directa a
5 clases (sin capas ocultas extra, sin BatchNorm, sin Dropout).
Total: 97,253 parametros.

## Configuracion
- image_size: 96
- batch_size: 64
- epochs: 5
- optimizer: adam (lr=0.001, betas=[0.9, 0.999])

## Resultados en validacion (best checkpoint)
- accuracy: 0.6880
- f1_macro: 0.6876
- precision_macro: 0.7231
- sensitivity_macro: 0.6880
- specificity_macro: 0.9220
- auroc_macro: 0.9067
