# Ablation Study

## Modelo final

- Arquitectura: SimpleCNN con 3 capas convolucionales (32, 64 y 128 filtros), activaciones ReLU, MaxPooling después de las dos primeras capas, Adaptive Average Pooling y una capa Linear de salida para 5 clases.
- Numero de parametros:93,893
- Accuracy de validacion:0.5770
- F1 macro de validacion: 0.5615
- Checkpoint usado:output/20260812_212608/checkpoints/best.pt
-Experimento 1: output/20260812_212608/checkpoints/best.pt
## Experimentos

| Experimento | Cambio | Params | Val accuracy | Val F1 macro | Comentario |
|---|---|---:|---:|---:|---|
| Baseline | CNN de 3 capas, 5 épocas, learning rate 0.001 | 93893 | 0.5550 | 0.5436 | Modelo base |
| Experimento 1 | Se aumentó el entrenamiento de 5 a 10 épocas, manteniendo learning rate 0.001 | 93893 | 0.5770 | 0.5615 | Mejoró respecto al baseline |
| Experimento 2 | Se redujo learning rate de 0.001 a 0.0005, con 5 épocas | 93893 | 0.5770 | 0.5615 | Obtuvo el mismo Accuracy y F1 macro que el Experimento 1 |

## Conclusion

Al realizar los experimentos mostraron una mejora respecto al modelo baseline. El modelo base obtuvo una accuracy de 0.5550 y un F1 macro de 0.5436. Al aumentar el entrenamiento a 10 épocas en el Experimento 1 se alcanzó una accuracy de 0.5770 y un F1 macro de 0.5615. En el Experimento 2, al reducir el learning rate de 0.001 a 0.0005 y utilizar 5 épocas, se obtuvieron igualmente una accuracy de 0.5770 y un F1 macro de 0.5615. Esto indica que ambas modificaciones permitieron mejorar el desempeño respecto al modelo base, aunque ninguna de las dos mostró ventaja en las métricas principales sobre la otra.

