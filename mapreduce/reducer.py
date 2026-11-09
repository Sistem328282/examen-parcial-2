#!/usr/bin/env python3
import sys
from collections import defaultdict

totales = defaultdict(int)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    parts = line.strip().split("\t")
    if len(parts) != 3:
        continue
    
    metodo_pago, dia_semana, cantidad_str = parts[0], parts[1], parts[2]
    try:
        totales[(metodo_pago, dia_semana)] += int(cantidad_str)
    except ValueError:
        continue

for (metodo_pago, dia_semana), total_unidades in sorted(totales.items()):
    print(f"{metodo_pago}\t{dia_semana}\t{total_unidades}")
