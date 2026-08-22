# Ablations

## Arquitectura (version final)
CNN con 4 bloques residuales (16 -> 32 -> 64 -> 112 canales). Cada
bloque tiene una rama principal Conv3x3 + BatchNorm y una rama de
shortcut Conv1x1 + BatchNorm que se suman antes del ReLU y el
MaxPool(2), seguido de Global Average Pooling y una capa lineal final
a 5 clases. Total: 99,669 parametros (efficiency_score = 1.0).

## Configuracion
- image_size: 96
- batch_size: 64
- epochs: 30
- optimizer: adam (lr=0.001, betas=[0.9, 0.999])
- scheduler: CosineAnnealingLR (T_max=epochs)
- augmentations: RandomHorizontalFlip(0.5), RandomRotation(10),
  ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2)

## Resultados en validacion (best checkpoint)
- accuracy: 0.7900
- f1_macro: 0.7895

## Observaciones
Ablation 1 (baseline): CNN de 3 bloques con Flatten + FC(18432->256),
4.8M parametros, val_acc 0.667, val_f1 0.665, efficiency_score ~0.021
(penalizado fuertemente por el tamano del modelo).

Ablation 2: se reemplazo Flatten+FC grande por Global Average Pooling
+ Linear(128->5), reduciendo el modelo a ~98.5K parametros
(efficiency_score = 1.0), se agrego data augmentation geometrica/color,
y se subieron las epocas de 5 a 30. Resultado: val_acc 0.7740,
val_f1_macro 0.7708. El val_acc oscilaba bastante entre epocas (LR fijo).

Ablation 3 (version final, este experimento): se agregaron conexiones
residuales (shortcut Conv1x1+BN por bloque, canales ajustados a
16-32-64-112 para mantenerse bajo 100K parametros) y un scheduler
CosineAnnealingLR para estabilizar el entrenamiento. Resultado:
val_acc 0.7900, val_f1_macro 0.7895, con las ultimas epocas mucho mas
estables (menos oscilacion) gracias al decaimiento del learning rate.

## Posibles mejoras futuras
- Bloques Squeeze-and-Excitation (SE) si se acepta bajar un poco la
  eficiencia (quedaria justo arriba de 100K parametros).
- Test-Time Augmentation (promediar prediccion normal + flip horizontal)
  en predict.py, sin tocar el modelo entrenado.
- Validacion cruzada usando los folds de config.yaml (num_folds/fold_index).
