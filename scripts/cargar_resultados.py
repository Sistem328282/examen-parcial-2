import psycopg2
import os
import sys

db_host = os.getenv("DB_HOST", "db")
db_name = os.getenv("DB_NAME", "datamart")
db_user = os.getenv("DB_USER", "admin")
db_pass = os.getenv("DB_PASS", "secretpass")

output_file = sys.argv[1] if len(sys.argv) > 1 else "/tmp/output_mr/part-00000"

try:
    conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_pass)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS unidades_pago_dia (
            id SERIAL PRIMARY KEY,
            metodo_pago VARCHAR(50) NOT NULL,
            dia_semana VARCHAR(20) NOT NULL,
            unidades_vendidas INT NOT NULL
        );
    """)

    with open(output_file, "r") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) == 3:
                metodo, dia, unidades = parts[0], parts[1], int(parts[2])
                cur.execute(
                    "INSERT INTO unidades_pago_dia (metodo_pago, dia_semana, unidades_vendidas) VALUES (%s, %s, %s);",
                    (metodo, dia, unidades)
                )

    conn.commit()
    cur.close()
    conn.close()
    print("Datos (dígito 4) cargados exitosamente en PostgreSQL.")
except Exception as e:
    print(f"Error al cargar datos: {e}")
