from flask import Flask, render_template, request, make_response, redirect, session, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = '4fantasticos'
db = SQLAlchemy(app)

class Accidente_Transito(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tipo_vehiculo = db.Column(db.String(30))
    tipo_choque = db.Column(db.String(80))
    cantidad_personas = db.Column(db.Integer)
    atrapados = db.Column(db.String(2))
    lesiones_visibles = db.Column(db.String(30))
    peligro_incendio = db.Column(db.String(2))
    latitud = db.Column(db.Float(50))
    longitud = db.Column(db.Float(50))
    additionaldata = db.Column(db.String(20))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20))


@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('Denuncia'))
    session['user_ip'] = user_ip
    return response

@app.route('/Denuncia')
def Denuncia():
    return render_template('Denuncia.html')

@app.route('/medica')
def medica():
    return render_template('medica.html')

@app.route('/incendio')
def incendio():
    return render_template('incendio.html')

@app.route('/rescate')
def rescate():
    return render_template('rescate.html')

@app.route('/medica/accidente', methods = ['GET','POST'])
def accidente():
    if request.method == 'POST':
       tipo_vehiculo = request.form['tipo_vehiculo']
       tipo_choque = request.form['tipo_choque']
       cantidad_personas = request.form['cantidad_personas']
       atrapados = request.form['atrapados']
       lesiones_visibles = request.form['lesiones_visibles']
       peligro_incendio = request.form['peligro_incendio']
       fecha = datetime.now()
       status = 'Alerta'
       datos = Accidente_Transito(tipo_vehiculo=tipo_vehiculo,tipo_choque=tipo_choque, cantidad_personas=cantidad_personas, atrapados=atrapados, lesiones_visibles=lesiones_visibles,peligro_incendio=peligro_incendio, fecha=fecha, status=status)
       db.session.add(datos)
       db.session.commit()
    return render_template('accidente.html')

@app.route('/bombero')
def bombero():
    return render_template('bombero.html')

@app.route('/alertas')
def alertas():
    return render_template('alertas.html')

@app.route('/en_proceso') 
def en_proceso():
    datos = Accidente_Transito.query.all()
    # datosleibles = jsonify(datos)
    # print(datosleibles)
    
    return render_template('en-proceso.html', datos=datos)

@app.route('/realizados')
def realizados():
    return render_template('realizados.html')

@app.route('/mapa')
def mapa():
    return render_template('mapa.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)