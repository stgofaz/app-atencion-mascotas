from flask import Flask, render_template, request, redirect, url_for
from database import validar_rut, guardar_datos, generar_numero_atencion, init_db

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
        nro_atencion = generar_numero_atencion()
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

