# Ablation Study

## Modelo final

- Arquitectura: SimpleCNN con 3 capas convolucionales (32, 64 y 128 filtros), activaciones ReLU, MaxPooling después de las dos primeras capas, Adaptive Average Pooling y una capa Linear de salida para 5 numero de clases.
- Numero de parametros: 93893
- Accuracy de validacion: 0.6140
- F1 macro de validacion: 0.6057
- Experimento #2 checkpoint usado: output/20260812_214228/checkpoints/best.pt
- Precision Macro: 0.4419
- Sensivity Macro: 0.4460
- Specifity Macro: 0.8615
- AUROC macro: 0.7621
- Loss: 1.2912

## Experimentos

| Experimento | Cambio | Params | Val accuracy | Val F1 macro | Comentario |
|---|---|---:|---:|---:|---|
| Baseline | CNN de 3 capas convolucionales, entrenada durante 5 epocas; se utilizo el mejor checkpoint generado
| 93893 | 0.5550 | 0.5436 | Modelo funcional utilizado para generar las predicciones finales |
| Experimento 1 | 64 a 32        | 93893 | 0.5996 | 0.6057 | Se ejecuto una variante adicional en Batch_Size |
| Experimento 2 | 0.001 a 0.0001 | 93893 | 0.6140 | 0.6057 | Se ejecuto una variante en Learning_rate |

## Conclusion

El modelo final utilizado fue una SimpleCNN compacta de 93893 parametros. 
La ejecucion del Experimento 2 (reduciendo el learning_rate de 0.001 a 0.0001) logro el mejor rendimiento global en validacion, alcanzando una accuracy de 0.6140 y un F1 macro de 0.6057, superando tanto al Baseline (0.5550 acc / 0.5436 F1) como al Experimento 1 con reduccion de batch size (0.5996 acc / 0.6057 F1). 
Los experimentos demostraron que una tasa de aprendizaje mas conservadora favorece una convergencia mas estable del modelo. 
El principal aprendizaje fue completar y optimizar el flujo de trabajo de clasificacion: preparacion del dataset, entrenamiento con ajuste de hiperparametros, seleccion del mejor checkpoint, evaluacion y generacion de predicciones para el conjunto de prueba.

El archivo predictions.csv asociado contiene 2501 predicciones, utiliza unicamente las clases 0 a 4 y no presenta IDs duplicados.
