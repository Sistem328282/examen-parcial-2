#!/usr/bin/env python3
import sys
from datetime import datetime

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("id,"):
        continue
    
    parts = line.split(",")
    if len(parts) != 8:
        continue
    
    try:
        fecha_hora_str = parts[1]
        cantidad = int(parts[5])
        metodo_pago = parts[7]
        
        fecha_dt = datetime.strptime(fecha_hora_str, "%Y-%m-%d %H:%M:%S")
        dia_semana = fecha_dt.strftime("%A")
        
        print(f"{metodo_pago}\t{dia_semana}\t{cantidad}")
    except (IndexError, ValueError):
        continue
