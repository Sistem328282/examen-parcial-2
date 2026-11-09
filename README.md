# Examen Parcial 2 - Pipeline de Big Data Contenedorizado

**Estudiante:** José  
**Matrícula:** 125052284  
**Dígito de Matrícula (Último):** 4  

---

## 1. Arquitectura del Sistema

El proyecto implementa una arquitectura distribuida y contenedorizada compuesta por tres servicios principales orquestados con **Docker Compose**:

1. **`hadoop_service` (Hadoop Streaming):** Contenedor Debian con OpenJDK 17 y Hadoop 3.3.6 configurado para ejecutar trabajos MapReduce mediante scripts en Python (`mapper.py` y `reducer.py`). Incluye acceso SSH con llaves RSA sin contraseña.
2. **`db_service` (PostgreSQL 15):** Base de datos relacional para la persistencia de los resultados procesados por el pipeline de Big Data.
3. **`api_service` (FastAPI + Uvicorn):** Servicio API REST expuesto en el puerto `8000` que interactúa con PostgreSQL para consulta y modificación de resultados.

---

## 2. Lógica de Negocio (Dígito 4)

Con base en la regla del examen para la matrícula finalizada en **4**, el pipeline calcula:
* **Métrica:** Total de unidades vendidas (`cantidad`).
* **Agrupación:** Agrupado por **Método de Pago** (`metodo_pago`) y **Día de la Semana** (`dia_semana`).

---

## 3. Autenticación SSH (Parte B)

Se configuró el par de claves RSA (`id_rsa` / `id_rsa.pub`) sin contraseña para el usuario `hadoopuser`.
* **Comando de prueba:** `su - hadoopuser && ssh localhost`
* **Resultado:** Conexión exitosa directa a través del puerto 22 sin solicitar contraseña.

---

## 4. Comparativa de Rendimiento (Parte C)

Se procesó un dataset masivo de **~5 millones de registros (352 MB)**:

* **Ejecución Secuencial (Pandas Python):** `28.79 segundos`
* **Ejecución Distribuida (Hadoop MapReduce Streaming):** `~18.50 segundos`

**Conclusión de Rendimiento:**  
MapReduce demuestra mayor velocidad y eficiencia en el procesamiento paralelo del dataset al dividir la carga de trabajo entre el proceso Mapper y Reducer, superando el tiempo de procesamiento en memoria secuencial de Pandas.

---

## 5. Documentación de API REST (Parte D)

* **GET `/resultados`**: Retorna el listado completo de unidades vendidas agrupadas por método de pago y día de la semana.
* **GET `/resultados/{filtro}`**: Filtra los registros por un método de pago específico (ej. `Tarjeta`) o día de la semana (ej. `Monday`).
* **POST `/resultados`**: Inserta un nuevo registro manualmente en la base de datos PostgreSQL.

---

## 6. Instrucciones de Reproducibilidad

1. Iniciar los contenedores:
   ```bash
   docker-compose up --build -d