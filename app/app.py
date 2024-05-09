#####################################################################################################################################
###################################################### Importaciones ##############################################################
#####################################################################################################################################
from deep_translator import GoogleTranslator
from flask import Flask
import hashlib
import datetime
import re
import hashAPI
from datetime import datetime
from random import sample
from sendMailAPI import send_email
import os.path

app = Flask(__name__)
from flask import render_template, request, flash, url_for, redirect, session
import mysql.connector as mysql
app.config['SECRET_KEY'] = 'abcd1234@'
app.config['SESSION_TYPE'] = 'filesystem'  #
import pandas as pd

from edamamApi import buscar_receta, analisisNutricional

global recipes_list
recipes_list = []


#####################################################################################################################################
###################################################### Index ##############################################################
#####################################################################################################################################

@app.route('/')
def index():
    session.pop('email', None)
    return render_template('index.html')

@app.route('/eliminarCuenta', methods=['POST'])
def eliminarCuenta():
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

            # Obtener el ID del cliente
            cur.execute('SELECT id FROM clientes WHERE email = %s', (email,))
            cliente_id = cur.fetchone()

            if cliente_id:
                cliente_id = cliente_id[0]

                # Eliminar los registros asociados en registro_calorias_diario
                cur.execute('DELETE FROM registro_calorias_diario WHERE cliente_id = %s', (cliente_id,))
                connection.commit()

                # Eliminar la cuenta de usuario
                cur.execute('DELETE FROM clientes WHERE email = %s', (email,))
                connection.commit()

                cur.close()
                connection.close()

                # Limpiar la sesión
                session.pop('email', None)
                flash('¡Cuenta eliminada correctamente!', 'success')
                return redirect(url_for('index'))

            else:
                flash('No se encontró al usuario en la base de datos.', 'error')
                return redirect(url_for('modificarUsuario'))

        except Exception as e:
            flash(f'Error al eliminar la cuenta: {str(e)}', 'error')
            return redirect(url_for('modificarUsuario'))

    else:
        flash('No se pudo encontrar la sesión del usuario.', 'error')
        return redirect(url_for('modificarUsuario'))



@app.route('/modificarUsuario', methods=['GET', 'POST'])
def modificarUsuario():
    if 'email' not in session:
        flash('Acceso no autorizado. Por favor, inicia sesión.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        usuario = request.form.get('usuario')
        email = session.get('email')
        contrasena = request.form.get('contrasena')
        fechaNacimiento = request.form.get('fechaNacimiento')
        peso = request.form.get('peso')
        altura = request.form.get('altura')
        genero = request.form.get('genero')
        actividad = request.form.get('actividad')

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

            cur.execute('SELECT * FROM clientes WHERE email = %s', (email,))
            user = cur.fetchone()

            if user:
                if nombre:
                    cur.execute('UPDATE clientes SET nombre = %s WHERE email = %s', (nombre, email))
                if usuario:
                    cur.execute('UPDATE clientes SET usuario = %s WHERE email = %s', (usuario, email))
                if contrasena:
                    hashed_password = hashlib.sha256(contrasena.encode('utf-8')).hexdigest()
                    cur.execute('UPDATE clientes SET contrasena = %s WHERE email = %s', (hashed_password, email))
                if fechaNacimiento:
                    cur.execute('UPDATE clientes SET fechaNacimiento = %s WHERE email = %s', (fechaNacimiento, email))
                if peso:
                    cur.execute('UPDATE clientes SET peso = %s WHERE email = %s', (peso, email))
                if altura:
                    cur.execute('UPDATE clientes SET altura = %s WHERE email = %s', (altura, email))
                if genero:
                    cur.execute('UPDATE clientes SET genero = %s WHERE email = %s', (genero, email))
                if actividad:
                    cur.execute('UPDATE clientes SET actividad = %s WHERE email = %s', (actividad, email))

                connection.commit()
                flash('¡Usuario modificado correctamente!', 'success')
            else:
                flash('¡No se encontró un usuario con ese email!', 'error')

        except Exception as e:
            flash(f'¡Error al modificar el usuario: {str(e)}', 'error')
    else:
        email = session['email']
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

            cur.execute('SELECT nombre, contrasena, fechaNacimiento, peso, altura, genero, actividad FROM clientes WHERE email = %s', (email,))
            user_data = cur.fetchone()
            cur.close()
            connection.close()

            # Pasar los datos actuales del usuario a la plantilla
            if user_data:
                nombre_actual = user_data[0]
                fechaNacimiento_actual = user_data[2]
                peso_actual = user_data[3]
                altura_actual = user_data[4]
                genero_actual = user_data[5]
                actividad_actual = user_data[6]

                # Puedes seguir extrayendo los otros campos de usuario aquí
                return render_template('modificarUsuario.html', nombre_actual=nombre_actual, fechaNacimiento_actual=fechaNacimiento_actual, peso_actual=peso_actual, altura_actual=altura_actual, genero_actual=genero_actual, actividad_actual=actividad_actual)
            else:
                flash('No se encontró al usuario en la base de datos.', 'error')
                return redirect(url_for('modificarUsuario'))

        except Exception as e:
            flash(f'Error al obtener los datos del usuario: {str(e)}', 'error')
            return redirect(url_for('modificarUsuario'))


#####################################################################################################################################
###################################################### Registro/Login ##############################################################
#####################################################################################################################################
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

            cur.execute('SELECT * FROM clientes WHERE email = %s', (email,))
            user = cur.fetchone()

            if user:
                flash('¡Ya existe un usuario con ese email!', 'error')
                return redirect(url_for('registro'))

            hashed_password = hashlib.sha256(contrasena.encode('utf-8')).hexdigest()


            cur.execute('INSERT INTO clientes (nombre, usuario, email, contrasena, fechaNacimiento, peso, altura, genero, actividad) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (nombre, usuario, email, hashed_password, fechaNacimiento, peso, altura, genero, actividad))
            connection.commit()

            cur.execute('SELECT id FROM clientes WHERE email = %s', (email,))
            cliente_id = cur.fetchone()

            if cliente_id:
                cliente_id = cliente_id[0]

                fecha_actual = datetime.now().date()
                cur.execute('INSERT INTO registro_calorias_diario (cliente_id, calorias_consumidas, fecha_consumo) VALUES (%s, %s, %s)', (cliente_id, 0, fecha_actual))
                connection.commit()

                cur.close()
                connection.close()
                flash('¡Registro exitoso!', 'success')
                return redirect(url_for('login'))

        except Exception as e:
            flash(f'¡Error al insertar en la base de datos: {str(e)}', 'error')
            return redirect(url_for('registro'))

    return render_template('registro.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/recuperarContraseña', methods=['GET', 'POST']) 
def recuperarContraseña():
    if request.method == 'POST':
        email = request.form['email']
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
            contraseña = password_generator(8)
            send_email(email, contraseña)
            cn = hashAPI.hashear(contraseña)
            cur.execute('SELECT id, contrasena FROM clientes WHERE email = %s AND contrasena = %s', (email, cn))
            user = cur.fetchone()
            cur.execute('UPDATE clientes SET contrasena = %s WHERE email = %s', (cn, email))
            connection.commit()
            cur.close()
            connection.close()
            return render_template('recuperarContrasena.html', email=email)
        except Exception as e:
            return render_template('recuperarContrasena.html')
    else:
        return render_template('recuperarContrasena.html')

    

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

                cur.execute('SELECT id FROM registro_calorias_diario WHERE cliente_id = %s AND fecha_consumo = CURDATE()', (cliente_id,))
                registro_hoy = cur.fetchone()

                if not registro_hoy:  
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


#####################################################################################################################################
###################################################### Inicio Usu ##############################################################
#####################################################################################################################################
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

        except Exception as e:
            flash(f'Error al cargar la página de inicio: {str(e)}', 'error')

        return redirect(url_for('login'))

    else:
        flash('Acceso no autorizado. Por favor, inicia sesión.', 'error')
        return redirect(url_for('index'))



def slow_loading_function(food: str):
    """Simulates a time consuming process (wait 10 seconds and return a reversed string)"""

    buscar_receta(food)
    dataframe_receta = pd.read_csv(f"{food}_recipes_dataframe.csv")

    # Traducir todas las columnas excepto la columna de la imagen
    dataframe_receta_translated = dataframe_receta.copy()
    for column in dataframe_receta_translated.columns:
        if column != 'image':
            dataframe_receta_translated[column] = dataframe_receta_translated[column].apply(lambda x: GoogleTranslator(source='auto', target='es').translate(str(x)))

    recipes_list = dataframe_receta_translated.to_dict(orient='records')
    return recipes_list


@app.route("/loading", methods=["POST"])
def loading():
    if request.method == "POST":
        global recipes_list
        food = request.form['query']
        session['food'] = food
        if food == '':
            return render_template('recetas.html')
        else:
            return render_template("loading.html")


@app.route('/results')
def results():
    if 'food' not in session:
        flash('Please provide a food query.', 'error')
        return redirect(url_for('index'))
    else:
        food = session.get('food')
        recipes_list = slow_loading_function(food)
        return render_template('recetas.html', recipes_list=recipes_list)



@app.route('/recetas', methods=['GET', 'POST'])
def recetas():
    if 'email' in session:
        global recipes_list
        if request.method == 'POST':
            food = request.form['query']
            if food == '':
                flash('Por favor, introduce un alimento.', 'error')
                return render_template('recetas.html')
            else:
                buscar_receta(food)
                dataframe_receta = pd.read_csv(f"{food}_recipes_dataframe.csv")

                # Traducir todas las columnas excepto la columna de la imagen
                dataframe_receta_translated = dataframe_receta.copy()
                for column in dataframe_receta_translated.columns:
                    if column != 'image':
                        dataframe_receta_translated[column] = dataframe_receta_translated[column].apply(lambda x: GoogleTranslator(source='auto', target='es').translate(str(x)))

                recipes_list = dataframe_receta_translated.to_dict(orient='records')

                return render_template('recetas.html', recipes_list=recipes_list)
        else:
            return render_template('recetas.html', recipes_list=None)
    else:
        flash('Acceso no autorizado. Por favor, inicia sesión.', 'error')
        return redirect(url_for('index'))


@app.route('/añadirComida', methods=['GET', 'POST'])
def añadirComida():
    if 'email' in session:
        if request.method == 'POST':
            # Lógica para procesar los datos del formulario y añadir la comida
            # a la base de datos debería ir aquí
            flash('Comida añadida con éxito!', 'success')
            return redirect(url_for('añadirComida'))  # Redireccionar a la página principal, por ejemplo
        else:
            # Mostrar el formulario para añadir comida
            return render_template('añadirAlimento.html')
    else:
        flash('Acceso no autorizado. Por favor, inicia sesión.', 'error')
        return redirect(url_for('index'))




@app.route('/infoComida', methods=['GET', 'POST'])
def infoComida():
    if 'email' in session:
        if request.method == 'POST':
            food = request.form['query']
            if food == '':
                return render_template('infoComida.html', analisis=None)
            else:
                food = GoogleTranslator(source='auto', target='en').translate(food)
                analisis_data = analisisNutricional(food)
                if analisis_data is not None:
                    analisis = pd.DataFrame(analisis_data)

                    for column in analisis.columns:
                        if column == 'label':
                            analisis[column] = analisis[column].apply(lambda x: GoogleTranslator(source='auto', target='es').translate(str(x)))
                    flash('¡Análisis nutricional realizado con éxito!', 'success')
                    return render_template('infoComida.html', analisis=analisis, query = food)
                flash('¡No se pudo realizar el análisis nutricional!', 'error')
                return render_template('infoComida.html')

        else:
            return render_template('infoComida.html', analisis=None)
    else:
        flash('Acceso no autorizado. Por favor, inicia sesión.', 'error')
        return redirect(url_for('index'))
    
@app.route('/articulos', methods=['GET'])
def articulos():
    return render_template('articulos.html')

#####################################################################################################################################
###################################################### Funciones Auxiliares ##############################################################
#####################################################################################################################################
def password_generator(longitud):
  
    # Definimos los caracteres y simbolos
    
    abc_minusculas = "abcdefghijklmnopqrstuvwxyz"
    
    # HACK: upper() transforma las letras de una cadena en mayusculas
    abc_mayusculas = abc_minusculas.upper() 
    
    numeros = "0123456789"
    simbolos = "{}[]()*;/,_-"
    
    # Definimos la secuencia
    secuencia = abc_minusculas + abc_mayusculas + numeros + simbolos
    
    # Llamamos la función sample() utilizando la secuencia, y la longitud
    password_union = sample(secuencia, longitud)
    
    # Con join insertamos los elementos de una lista en una cadena
    password_result = "".join(password_union)
    
    # Retornamos la variables "password_result"
    return password_result

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