from flask import Flask
import hashlib
import datetime
import re
import hashAPI
from datetime import datetime

app = Flask(__name__)
from flask import render_template, request, flash, url_for, redirect, session
import mysql.connector as mysql
app.config['SECRET_KEY'] = 'abcd1234@'
app.config['SESSION_TYPE'] = 'filesystem'  # Puedes elegir otro tipo de sesión

from edamamApi import recipe_search, nut_analysis
import pandas as pd

'''
La ruta raíz '/' se asocia a la función index(), que renderiza una plantilla HTML llamada 'index.html'. Esta ruta se utiliza para mostrar la página principal de la aplicación.
'''
@app.route('/')
def index():
    session.pop('email', None)
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        usuario = request.form['usuario']
        email = request.form['email']
        contrasena = request.form['contrasena']
        fechaNacimiento = request.form['fechaNacimiento']
        peso = request.form['peso']
        altura = request.form['altura']
        genero = request.form['genero']
        actividad = request.form['actividad']

        try:
            config = {
                'user': 'root',
                'password': 'rootasdeg2324',
                'host': 'db',
                'port': '3306',
                'database': 'usuarios'
            }
            connection = mysql.connect(**config)
            cur = connection.cursor()

            # Verificar si el usuario ya existe
            cur.execute('SELECT * FROM clientes WHERE email = %s', (email,))
            user = cur.fetchone()

            if user:
                flash('¡Ya existe un usuario con ese email!', 'error')
                return redirect(url_for('registro'))

            # Generar hash de la contraseña
            hashed_password = hashlib.sha256(contrasena.encode('utf-8')).hexdigest()


            # Insertar datos en la tabla clientes
            cur.execute('INSERT INTO clientes (nombre, usuario, email, contrasena, fechaNacimiento, peso, altura, genero, actividad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (nombre, usuario, email, hashed_password, fechaNacimiento, peso, altura, genero, actividad))
            connection.commit()

            # Obtener el ID del cliente recién registrado
            cur.execute('SELECT id FROM clientes WHERE email = %s', (email,))
            cliente_id = cur.fetchone()

            if cliente_id:
                cliente_id = cliente_id[0]

                # Insertar un registro en la tabla registro_calorias_diario
                fecha_actual = datetime.now().date()
                cur.execute('INSERT INTO registro_calorias_diario (cliente_id, calorias_consumidas, fecha_consumo) VALUES (%s, %s, %s)', (cliente_id, 0, fecha_actual))
                connection.commit()

                cur.close()
                connection.close()
                flash('¡Registro exitoso!', 'success')
                return redirect(url_for('login'))

        except Exception as e:
            flash(f'¡Error al insertar en la base de datos: {str(e)}', 'error')

    return render_template('registro.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['contrasena']

        try:
            config = {
                'user': 'root',
                'password': 'rootasdeg2324',
                'host': 'db',
                'port': '3306',
                'database': 'usuarios'
            }
            connection = mysql.connect(**config)
            cur = connection.cursor()
            cn = hashAPI.hashear(contrasena)
            cur.execute('SELECT id, contrasena FROM clientes WHERE email = %s AND contrasena = %s', (email, cn))
            user = cur.fetchone()

            if user and user[1] == cn:
                session['email'] = email
                flash('¡Inicio de sesión exitoso!', 'success')
                cliente_id = user[0]

                # Comprobar si existe un registro de calorías para hoy
                cur.execute('SELECT id FROM registro_calorias_diario WHERE cliente_id = %s AND fecha_consumo = CURDATE()', (cliente_id,))
                registro_hoy = cur.fetchone()

                if not registro_hoy:  # Si no existe registro de hoy, crea uno
                    cur.execute('INSERT INTO registro_calorias_diario (cliente_id, calorias_consumidas, fecha_consumo) VALUES (%s, %s, %s)', (cliente_id, 0, datetime.now().date()))
                    connection.commit()
                    flash('¡Registro de calorías diario creado!', 'success')

                cur.close()
                connection.close()
                return redirect(url_for('inicioUsu'))

            else:
                flash('Credenciales incorrectas. Inténtalo de nuevo.', 'error')

        except Exception as e:
            flash(f'Error al iniciar sesión: {str(e)}', 'error')

    return render_template('login.html')


@app.route('/inicioUsu')
def inicioUsu():
    if 'email' in session:
        try:
            email = session['email']
            config = {
                'user': 'root',
                'password': 'rootasdeg2324',
                'host': 'db',
                'port': '3306',
                'database': 'usuarios'
            }
            connection = mysql.connect(**config)
            cur = connection.cursor()

            fecha_actual = datetime.now().date()
            cur.execute('SELECT clientes.nombre, clientes.calorias_objetivo, registro_calorias_diario.calorias_consumidas FROM clientes INNER JOIN registro_calorias_diario ON clientes.id = registro_calorias_diario.cliente_id WHERE clientes.email = %s AND registro_calorias_diario.fecha_consumo = %s', (email, fecha_actual))
            data = cur.fetchone()
            cur.close()
            connection.close()

            if data:
                nombre = data[0]
                calorias_objetivo = data[1]
                calorias_consumidas = data[2]
                calorias_restantes = calorias_objetivo - calorias_consumidas

                return render_template('inicioUsu.html', nombre=nombre, calorias_objetivo=calorias_objetivo, calorias_consumidas=calorias_consumidas, calorias_restantes=calorias_restantes)
            # Obtener el ID del cliente actual
        except Exception as e:
            flash(f'Error al cargar la página de inicio: {str(e)}', 'error')

        return redirect(url_for('login'))

    else:
        flash('Acceso no autorizado. Por favor, inicia sesión.', 'error')
        return redirect(url_for('login'))
    

@app.route('/recetas', methods=['GET', 'POST'])
def recetas():
    if 'email' in session:  # Verificar si el usuario ha iniciado sesión
        if request.method == 'POST':
            ingredient = request.form['query']
            dataframe_receta = recipe_search(ingredient)
            
            # Renderizar la plantilla con el DataFrame como contexto
            return render_template('recetas.html', recipes_list=dataframe_receta.to_dict(orient='records'))
        
        # Si el método de solicitud es GET, renderizar la plantilla con None
        return render_template('recetas.html', recipes_list=None)
    
    else:
        flash('Acceso no autorizado. Por favor, inicia sesión.', 'error')
        return redirect(url_for('login'))
    

@app.route('/infoComida', methods=['GET', 'POST'])
def infoComida():
    if request.method == 'POST':
        food = request.form['query']
        df = nut_analysis(food)
        if df is not None:
            df_list = df.to_dict(orient='records')
            return render_template('infoComida.html', df_list=df_list)
        else:
            mensaje = f"No se encontraron datos nutricionales para {food}."
            return render_template('infoComida.html', mensaje=mensaje)

    mensaje = "Bienvenido a la página de información sobre comida"
    return render_template('infoComida.html', mensaje=mensaje)



# Dados las calorias introducidas por le cliente se actualiza las calorias consumidas de ese cliente en el dia actual
@app.route('/añadirCalorias', methods=['GET', 'POST'])
def añadirCalorias():
    if request.method == 'POST':
        calorias = request.form['calorias']

        try:
            config = {
                'user': 'root',
                'password': 'rootasdeg2324',
                'host': 'db',
                'port': '3306',
                'database': 'usuarios'
            }
            connection = mysql.connect(**config)
            cur = connection.cursor()

            cur.execute('UPDATE registro_calorias_diario SET calorias_consumidas = calorias_consumidas + %s WHERE cliente_id = (SELECT id FROM clientes WHERE email = %s) AND fecha_consumo = CURDATE()', (calorias, session['email']))
            connection.commit()

            cur.close()
            connection.close()
            flash('¡Calorías añadidas correctamente!', 'success')

            return redirect(url_for('inicioUsu'))
        except Exception as e:
            flash(f'¡Error al añadir las calorías: {str(e)}', 'error')

    return render_template('BuenHome.html')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)