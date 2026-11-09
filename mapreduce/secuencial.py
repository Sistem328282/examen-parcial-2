import pandas as pd
import time
import sys

dataset_path = sys.argv[1] if len(sys.argv) > 1 else "/data/input/dataset.csv"

inicio = time.time()

df = pd.read_csv(dataset_path)
df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
df['dia_semana'] = df['fecha_hora'].dt.day_name()

resultado = df.groupby(['metodo_pago', 'dia_semana'])['cantidad'].sum().reset_index()

fin = time.time()

print(resultado)
print(f"\nTiempo de ejecución secuencial: {fin - inicio:.2f} segundos")
