from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI(title="DataMart Analytics API - Dígito 4")

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "datamart"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASS", "secretpass"),
        cursor_factory=RealDictCursor
    )

class RegistroUnidades(BaseModel):
    metodo_pago: str
    dia_semana: str
    unidades_vendidas: int

@app.get("/resultados")
def get_todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM unidades_pago_dia ORDER BY metodo_pago, dia_semana;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.get("/resultados/{filtro}")
def get_por_filtro(filtro: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM unidades_pago_dia WHERE LOWER(metodo_pago) = LOWER(%s) OR LOWER(dia_semana) = LOWER(%s);",
        (filtro, filtro)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="No se encontraron registros.")
    return rows

@app.post("/resultados", status_code=201)
def crear_registro(item: RegistroUnidades):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO unidades_pago_dia (metodo_pago, dia_semana, unidades_vendidas) VALUES (%s, %s, %s) RETURNING id;",
        (item.metodo_pago, item.dia_semana, item.unidades_vendidas)
    )
    nuevo_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    conn.close()
    return {"mensaje": "Registro insertado exitosamente", "id": nuevo_id}
