# Ablation Study

## Modelo final

- Arquitectura: CNN de 3 bloques conv (16->32->64) + bloque residual (64 canales) + bloque conv final (64->96), seguido de Global Average Pooling y clasificador Linear(96->48)->ReLU->Dropout(0.5)->Linear(48->5)
- Numero de parametros: 158,277
- Accuracy de validacion: 0.8280
- F1 macro de validacion: 0.8265

## Experimentos

| Experimento | Cambio | Params | Val accuracy | Val F1 macro | Comentario |
|---|---|---:|---:|---:|---|
| Baseline (v1, 3 bloques) | CNN simple 3 conv, sin BN | ~4.8M | 0.675 | - | Primer modelo funcional |
| v2 (4 bloques + BN) | + BatchNorm, + 4to bloque conv | 2,750,213 | 0.833 | - | Mejor accuracy cruda, pero overfitting fuerte (gap train-val ~6 pts) y efficiency_score muy bajo (0.036) |
| v3 (GAP + canales reducidos) | Flatten -> AdaptiveAvgPool2d(1), canales reducidos, 100 epocas | 106,501 | 0.7820 | 0.7751 | Elimina el cuello de botella de parametros. Gap train-val minimo (~1.3 pts), pero techo de accuracy mas bajo |
| v4 (residual grande) | + ResidualBlock, canales ensanchados (24->48->96->160), + label smoothing, + GaussianBlur/RandomErasing | 371,269 | 0.8370 | 0.8365 | Mayor accuracy absoluta, pero overfitting reaparece (gap ~6.6 pts) y penalizacion de eficiencia alta (0.269) |
| v5 (residual chico + mas weight_decay) | ResidualBlock en canales reducidos (16->32->64->96), weight_decay 0.0001->0.0003 | 158,277 | 0.8280 | 0.8265 | Mejor balance: retiene la mayor parte de la ganancia de accuracy de v4 con gap train-val moderado (~4.5 pts) y efficiency_score razonable (0.632) |

## Conclusion

La metrica final del reto (`0.70*F1 + 0.20*accuracy + 0.10*efficiency_score`) penaliza fuertemente el numero de parametros, por lo que la mejor decision de diseno no fue maximizar accuracy sino encontrar el balance optimo entre capacidad del modelo y eficiencia. v3 elimino el overfitting casi por completo via Global Average Pooling, pero sacrifico demasiada capacidad (score ~0.793). v4 recupero accuracy con un bloque residual y canales mas anchos, pero la penalizacion de eficiencia (0.269) no compenso la ganancia (score ~0.780). v5 combino el bloque residual de v4 con canales mas chicos y mayor weight_decay (0.0001->0.0003) para controlar el overfitting, logrando el mejor score estimado (~0.807): retiene el 94% de la ganancia de accuracy de v4 mientras recupera mas de la mitad del efficiency_score perdido.
