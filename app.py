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
        guardar_datos(rut, request.form, nro_atencion)  # ✅ PASA request.form completo
        return f"Gracias, tu número de atención es: <b>{nro_atencion}</b>"
    return render_template('atencion.html', rut=rut)

if __name__ == '__main__':
    app.run(debug=True)

