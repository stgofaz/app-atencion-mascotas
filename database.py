import sqlite3
import pandas as pd
import os
import random
import threading
excel_lock = threading.Lock()

# Crear base de datos si no existe
def init_db():
    conn = sqlite3.connect('datos.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS atenciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rut TEXT,
            nombre TEXT,
            tipo TEXT,
            servicios TEXT,
            numero_atencion INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Validar RUT (puedes expandir esta lógica)
def validar_rut(rut):
    df_ruts = pd.read_excel("rut_validos.xlsx")
    ruts_validos = df_ruts['Rut'].astype(str).str.strip().tolist()
    return rut.strip() in ruts_validos

# Generar número de atención aleatorio
def generar_numero_atencion():
    return random.randint(1000, 9999)

# Guardar datos en SQLite y en Excel
def guardar_datos(rut, form_data, numero_atencion):
    from datetime import datetime
    conn = sqlite3.connect('datos.db')
    c = conn.cursor()

    total = len([key for key in form_data if key.startswith("nombre_")])
    n_perros = int(form_data.get("perros", 0))  # del formulario

    registros = []

    for i in range(1, total+1):
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nombre = form_data.get(f'nombre_{i}')
        servicios = form_data.getlist(f'servicio_{i}')
        tipo = "Perro" if i <= n_perros else "Gato"

        # Guardar en SQLite
        c.execute('''
    INSERT INTO atenciones (rut, nombre, tipo, servicios, numero_atencion, fecha_hora)
    VALUES (?, ?, ?, ?, ?, ?)
''', (rut, nombre, tipo, ', '.join(servicios), numero_atencion, fecha_actual))

        # Preparar para Excel
        registros.append({
            "RUT": rut,
            "Nombre": nombre,
            "Tipo": tipo,
            "Servicios": ", ".join(servicios),
            "Número Atención": numero_atencion,
            "Fecha y Hora": fecha_actual
        })

    conn.commit()
    conn.close()

    # Guardar en Excel con lock
    archivo = "datos.xlsx"
    df_nuevo = pd.DataFrame(registros)

    if os.path.exists(archivo):
        df_existente = pd.read_excel(archivo)
        df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
    else:
        df_final = df_nuevo

    # 🔐 Protección de escritura simultánea
    with excel_lock:
        df_final.to_excel(archivo, index=False)




