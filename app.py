from flask import Flask, render_template, request, redirect, url_for
from database import validar_rut, guardar_datos, generar_numero_atencion, init_db
import sqlite3



app = Flask(__name__)

# Inicializar base de datos
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        rut = request.form['rut']
        if validar_rut(rut):
            return redirect(url_for('atencion', rut=rut))
        else:
            return render_template('index.html', error="RUT no autorizado.")
    return render_template('index.html')

@app.route('/atencion', methods=['GET', 'POST'])
def atencion():
    rut = request.args.get('rut')
    if request.method == 'POST':
        nro_atencion = request.form.get("numero_atencion")
        guardar_datos(rut, request.form, nro_atencion)
        return f'''
<h2>Gracias, tu número de atención es: <b>{nro_atencion}</b></h2>
<br>
<form action="/">
    <button type="submit">Volver al inicio</button>
</form>
'''
    return render_template('atencion.html', rut=rut)
from flask import send_file
import pandas as pd
import os

@app.route('/exportar')
def exportar_datos():
    archivo = "datos.xlsx"
    if os.path.exists(archivo):
        return send_file(archivo, as_attachment=True)
    else:
        return "Archivo no encontrado", 404

@app.route('/editar', methods=['GET', 'POST'])
def editar():
    if request.method == 'POST':
        rut = request.form['rut'].strip().upper()

        # Buscar coincidencias en la base SQLite
        conn = sqlite3.connect('datos.db')
        c = conn.cursor()
        c.execute("SELECT id, nombre, tipo, servicios FROM atenciones WHERE rut = ?", (rut,))
        resultado = c.fetchall()
        conn.close()

        if resultado:
            return render_template('editar_resultado.html', atenciones=resultado, rut=rut)
        else:
            return render_template('editar.html', error="No se encontraron registros con ese RUT y número de atención.")

    return render_template('editar.html')

@app.route('/actualizar', methods=['POST'])
def actualizar():
    import sqlite3
    import pandas as pd
    from datetime import datetime

    rut = request.form['rut']
    total = int(request.form['total'])

    conn = sqlite3.connect('datos.db')
    c = conn.cursor()

    for i in range(1, total + 1):
        atencion_id = int(request.form[f'id_{i}'])
        nuevos_servicios = request.form[f'servicios_{i}']

        c.execute("UPDATE atenciones SET servicios = ? WHERE id = ?", (nuevos_servicios, atencion_id))

    conn.commit()

    # Reescribir Excel completo desde la base de datos
    df = pd.read_sql_query("SELECT rut, nombre, tipo, servicios, numero_atencion, fecha_hora FROM atenciones", conn)
    df.columns = ["RUT", "Nombre", "Tipo", "Servicios", "Número Atención", "Fecha y Hora"]
    df.to_excel("datos.xlsx", index=False)

    conn.close()

    return render_template("gracias.html", mensaje="Servicios actualizados correctamente.")


@app.route('/reiniciar_db')
def reiniciar_db():
    import sqlite3
    conn = sqlite3.connect('datos.db')
    c = conn.cursor()
    c.execute("DELETE FROM atenciones")  # Borra todos los datos
    conn.commit()
    conn.close()
    return "Base de datos reiniciada con éxito."


if __name__ == '__main__':
    app.run(debug=True)



