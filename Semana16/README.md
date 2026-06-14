# Semana 16 – Reconocimiento de Señales de Tránsito

## Descripción del problema

El objetivo de este taller es construir una red neuronal capaz de clasificar imágenes de señales de tránsito en 43 categorías distintas, utilizando el dataset German Traffic Sign Recognition Benchmark (GTSRB).

## Instrucciones de ejecución

Se requiere Python 3.10 o superior. Las dependencias se instalan con:

```
pip install tensorflow numpy pandas scikit-learn matplotlib pillow opencv-python
```

El dataset debe estar en la carpeta `archive/` con la siguiente estructura:

```
archive/
  Train/      (subcarpetas 0 a 42 con imágenes)
  Test/       (imágenes planas)
  Train.csv
  Test.csv
```

Para entrenar el modelo se corre `main.py` una sola vez. Esto genera el archivo `models/traffic_sign_model.h5` junto con las gráficas de entrenamiento y la matriz de confusión en la carpeta `models/`.

```
cd Semana16
python main.py
```

Una vez entrenado, la interfaz gráfica se lanza con:

```
python ui.py
```

Desde la interfaz se puede abrir cualquier imagen con el botón "Open Image" y luego presionar "Classify" para obtener la predicción con las top 5 clases más probables.

## Arquitectura del modelo

La red recibe imágenes de 32×32 píxeles en RGB. Está compuesta por tres bloques convolucionales seguidos de una cabeza de clasificación. Cada bloque aplica dos capas Conv2D con activación ReLU, BatchNormalization. La cabeza de clasificación tiene una capa densa de 256 unidades con BatchNormalization y Dropout, seguida de la capa de salida con 43 unidades y activación softmax. El modelo tiene 333,899 parámetros en total (1.27 MB).

El optimizador es Adam con tasa de aprendizaje inicial de 0.001. Durante el entrenamiento se usa ReduceLROnPlateau para bajar el learning rate cuando la pérdida de validación se estanca, y EarlyStopping para detener el entrenamiento si la precisión de validación no mejora en 7 épocas. El split entre entrenamiento y validación se hace de forma estratificada para garantizar que todas las clases estén representadas en ambos conjuntos.

## Métricas obtenidas

El modelo se entrenó durante 20 épocas. La precisión en entrenamiento llegó a 98.24% y la precisión en validación alcanzó 99.57% en la época 19, que fue el mejor checkpoint guardado. Sobre el conjunto de prueba, el modelo obtuvo una precisión de 95.39% con una pérdida de 0.1832.

| Conjunto     | Accuracy | Loss   |
|--------------|----------|--------|
| Entrenamiento | 98.24%  | 0.0533 |
| Validación   | 99.57%   | 0.0156 |
| Prueba       | 95.39%   | 0.1832 |

La diferencia entre validación y prueba se explica por las condiciones fotográficas distintas entre ambos conjuntos, pero el resultado sigue siendo sólido para un modelo entrenado desde cero sin transfer learning.

## Conclusiones

El modelo logra clasificar correctamente más del 95% de las imágenes del conjunto de prueba, lo cual es un resultado competitivo considerando que se entrenó desde cero. El uso de BatchNormalization fue clave para estabilizar el entrenamiento desde las primeras épocas, y el split estratificado corrigió un problema inicial donde la validación obtenía accuracy cercano a 0 porque el split secuencial dejaba clases enteras fuera del conjunto de entrenamiento. El principal cuello de botella del proyecto fue el tiempo de carga del dataset, ya que leer más de 50,000 imágenes desde disco de forma secuencial tarda varios minutos. Una mejora futura sería preprocesar y guardar los arrays en formato `.npy` para acelerar las ejecuciones posteriores.