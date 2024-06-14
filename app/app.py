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
import os.path
from secrets import choice
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
import ssl
import string
import locale
import random
from datetime import datetime, timedelta



app = Flask(__name__)
from flask import render_template, request, url_for, redirect, session, flash
import mysql.connector as mysql
app.config['SECRET_KEY'] = 'abcd1234@'
app.config['SESSION_TYPE'] = 'filesystem' 
app.config['JSON_AS_ASCII'] = False

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
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

            # Obtener el id_cliente del cliente
            cur.execute('SELECT id_cliente FROM Cliente WHERE email = %s', (email,))
            cliente_id = cur.fetchone()

            if cliente_id:
                cliente_id = cliente_id[0]

                # Eliminar los registros asociados al consumo
                cur.execute('DELETE FROM consume WHERE id_cliente = %s', (cliente_id,))
                connection.commit()

                # Eliminar los registros asociados al consumo
                cur.execute('DELETE FROM tiene_objetivo WHERE id_cliente = %s', (cliente_id,))
                connection.commit()

                # Eliminar la cuenta de usuario
                cur.execute('DELETE FROM Cliente WHERE email = %s', (email,))
                connection.commit()

                cur.close()
                connection.close()

                # Limpiar la sesión
                session.pop('email', None)
                
                return redirect(url_for('index'))

            else:
                return redirect(url_for('modificarUsuario'))

        except Exception as e:
            return redirect(url_for('modificarUsuario'))

    else:
        return redirect(url_for('modificarUsuario'))

@app.route('/modificarAlergenos', methods=['GET', 'POST'])
def modificarAlergenos():
    if 'email' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        alimento_id = request.form.get('alimento')
        gravedad = request.form.get('gravedad')
        sintomas = request.form.get('sintomas')
        email = session.get('email')

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

            cur.execute('SELECT id_cliente FROM Cliente WHERE email = %s', (email,))
            user = cur.fetchone()

            if user:
                user_id = user[0]
                cur.execute('INSERT INTO tiene_alergia (id_cliente, id_alimento, gravedad, sintomas) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE gravedad = %s, sintomas = %s', 
                            (user_id, alimento_id, gravedad, sintomas, gravedad, sintomas))
                connection.commit()
                cur.close()
                connection.close()
                return redirect(url_for('modificarAlergenos'))
            else:
                return redirect(url_for('modificarAlergenos'))

        except Exception as e:
            return redirect(url_for('modificarAlergenos'))

    else:
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

            cur.execute('SELECT id_alimento, nombreAlimento FROM Alimento')
            alimentos = cur.fetchall()
            cur.close()
            connection.close()

            return render_template('modificarAlergenos.html', alimentos=alimentos)

        except Exception as e:
            return redirect(url_for('modificarAlergenos'))



@app.route('/modificarUsuario', methods=['GET', 'POST'])
def modificarUsuario():
    if 'email' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        usuario = request.form.get('usuario')
        email = session.get('email')
        contrasena = request.form.get('contrasena')
        fecha_nacimiento = request.form.get('fechaNacimiento')
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

            cur.execute('SELECT * FROM Cliente WHERE email = %s', (email,))
            user = cur.fetchone()

            if user:
                if nombre:
                    cur.execute('UPDATE Cliente SET nombre = %s WHERE email = %s', (nombre, email))
                if usuario:
                    cur.execute('UPDATE Cliente SET usuario = %s WHERE email = %s', (usuario, email))
                if contrasena:
                    hashed_password = hashlib.sha256(contrasena.encode('utf-8')).hexdigest()
                    cur.execute('UPDATE Cliente SET contrasena = %s WHERE email = %s', (hashed_password, email))
                if fecha_nacimiento:
                    cur.execute('UPDATE Cliente SET fecha_nacimiento = %s WHERE email = %s', (fecha_nacimiento, email))
                if peso:
                    cur.execute('UPDATE Cliente SET peso = %s WHERE email = %s', (peso, email))
                if altura:
                    cur.execute('UPDATE Cliente SET altura = %s WHERE email = %s', (altura, email))
                if genero:
                    cur.execute('UPDATE Cliente SET genero = %s WHERE email = %s', (genero, email))
                if actividad:
                    cur.execute('UPDATE Cliente SET actividad = %s WHERE email = %s', (actividad, email))

                connection.commit()
                return redirect(url_for('modificarUsuario'))

            else:
                return redirect(url_for('modificarUsuario'))

        except Exception as e:
            return redirect(url_for('modificarUsuario'))
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

            cur.execute('SELECT nombre, contrasena, fecha_nacimiento, peso, altura, genero, actividad FROM Cliente WHERE email = %s', (email,))
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
                return redirect(url_for('modificarUsuario'))

        except Exception as e:
            return redirect(url_for('modificarUsuario'))


#####################################################################################################################################
###################################################### Registro/Login ##############################################################
#####################################################################################################################################
def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=50))

@app.route('/verificar_email', methods=['GET'])
def verificar_email():
    token = request.args.get('token')
    email = verificar_token(token)
    
    if email:
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
            cur.execute('UPDATE Cliente SET email_verificado = TRUE WHERE email = %s', (email,))
            connection.commit()
            cur.close()
            connection.close()

            send_email(email, 1)
            
            return render_template('verificacion_correcta.html')
        except Exception as e:
            flash(f'Error al verificar el correo: {str(e)}', 'error')
            return redirect(url_for('login'))
    else:
        flash('Enlace de verificación inválido o expirado', 'error')
        return redirect(url_for('registro'))



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

            cur.execute('SELECT id_cliente FROM Cliente WHERE email = %s', (email,))
            user = cur.fetchone()

            if user:
                id_cliente = user[0]
                cur.execute('SELECT requested_at FROM PasswordReset WHERE id_cliente = %s ORDER BY requested_at DESC LIMIT 1', (id_cliente,))
                last_request = cur.fetchone()
                
                if last_request and datetime.now() - last_request[0] < timedelta(hours=24):
                    flash('You can only request a password reset once every 24 hours.', 'danger')
                else:
                    token = generate_token()
                    expiration = datetime.now() + timedelta(hours=1)
                    requested_at = datetime.now()
                    cur.execute('INSERT INTO PasswordReset (id_cliente, token, expiration, requested_at) VALUES (%s, %s, %s, %s)', (id_cliente, token, expiration, requested_at))
                    connection.commit()
                    
                    send_email(email, 0, token)
                    flash('An email has been sent with instructions to reset your password.', 'success')
            else:
                flash('Email address not found.', 'danger')
        except Exception as e:
            flash(str(e), 'danger')
        finally:
            cur.close()
            connection.close()

    return render_template('recuperarContrasena.html')

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        token = request.form['token']
        new_password = request.form['password']
        hashed_new_password = hashAPI.hashear(new_password)
        
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
            
            cur.execute('SELECT id_cliente FROM PasswordReset WHERE token = %s AND expiration > %s AND used = FALSE', (token, datetime.now()))
            result = cur.fetchone()

            if result:
                id_cliente = result[0]
                
                # Check if the new password has been used before
                cur.execute('SELECT 1 FROM PasswordHistory WHERE id_cliente = %s AND hashed_password = %s', (id_cliente, hashed_new_password))
                if cur.fetchone():
                    flash('This password has been used before. Please choose a different password.', 'danger')
                    return render_template('reset_password.html', token=token)
                else:
                    # Update the password
                    cur.execute('UPDATE Cliente SET contrasena = %s WHERE id_cliente = %s', (hashed_new_password, id_cliente))
                    
                    # Insert the new password into PasswordHistory
                    cur.execute('INSERT INTO PasswordHistory (id_cliente, hashed_password, change_date) VALUES (%s, %s, %s)', (id_cliente, hashed_new_password, datetime.now()))
                    
                    # Mark the token as used
                    cur.execute('UPDATE PasswordReset SET used = TRUE WHERE token = %s', (token,))
                    connection.commit()
                    
                    flash('Your password has been reset successfully.', 'success')
                    return redirect(url_for('login'))  
            else:
                flash('Invalid or expired token.', 'danger')
                return redirect(url_for('request_reset_token'))  
        except Exception as e:
            flash(str(e), 'danger')
        finally:
            cur.close()
            connection.close()
    
    token = request.args.get('token')
    return render_template('reset_password.html', token=token)


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

            cur.execute('SELECT * FROM Cliente WHERE email = %s', (email,))
            user = cur.fetchone()

            if user:
                flash('Ya existe una cuenta con ese correo electrónico', 'error')
                return redirect(url_for('registro'))

            hashed_password = hashlib.sha256(contrasena.encode('utf-8')).hexdigest()

            cur.execute('INSERT INTO Cliente (nombre, nombre_usu, email, contrasena, peso, altura, genero, actividad, fecha_nacimiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', 
                        (nombre, usuario, email, hashed_password, peso, altura, genero, actividad, fechaNacimiento))
            connection.commit()

            cur.execute('SELECT id_cliente FROM Cliente WHERE email = %s', (email,))
            cliente_id = cur.fetchone()[0]

            if cliente_id:
                cur.execute('INSERT INTO consume (id_cliente, id_nutriente, fecha_consumo, cantidad) SELECT %s, n.id_nutriente, CURDATE(), 0 FROM Nutriente n', (cliente_id,))
                connection.commit()
                cur.execute('INSERT INTO tiene_objetivo (id_cliente, id_nutriente, cantidad) SELECT %s, id_nutriente, 2000 FROM Nutriente', (cliente_id,))
                connection.commit()
                cur.execute('INSERT INTO PasswordHistory (id_cliente, hashed_password, change_date) VALUES (%s, %s, NOW())', (cliente_id, hashed_password))
                connection.commit()

                cur.close()
                connection.close()

                token = generar_token(email)
                send_email(email, 2, token, nombre)

                flash('Usuario registrado correctamente. Por favor verifica tu correo electrónico.', 'success')
                return redirect(url_for('login'))

        except Exception as e:
            flash(f'Error al registrar el usuario: {str(e)}', 'error')
            return redirect(url_for('registro'))

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
            cur.execute('SELECT id_cliente, contrasena FROM Cliente WHERE email = %s AND contrasena = %s', (email, cn))
            user = cur.fetchone()

            if user and user[1] == cn:
                session['email'] = email

                cur.close()
                connection.close()
                return redirect(url_for('inicioUsu'))

            else:
                return redirect(url_for('login'))

        except Exception as e:
            return redirect(url_for('login'))

    return render_template('login.html')



#####################################################################################################################################
###################################################### Inicio Usu ##############################################################
#####################################################################################################################################
@app.route('/inicioUsu', methods=['GET', 'POST'])
def inicioUsu():
    if 'email' in session:
        try:
            email = session['email']
            frecuencia = request.args.get('frecuencia', 'diario')  # Obtener la frecuencia seleccionada
            orden = request.args.get('orden', 'normal')  # Obtener el orden seleccionado
            config = {
                'user': 'root',
                'password': 'rootasdeg2324',
                'host': 'db',
                'port': '3306',
                'database': 'usuarios'
            }
            connection = mysql.connect(**config)
            cur = connection.cursor()

            # Obtener datos del cliente
            cur.execute('SELECT id_cliente, nombre, nombre_usu, email, contrasena, peso, altura, genero, actividad, fecha_nacimiento FROM Cliente WHERE email = %s', (email,))
            cliente = cur.fetchone()

            if cliente:
                id_cliente = cliente[0]

                # Establecer los días según la frecuencia
                if frecuencia == 'semanal':
                    dias = 7
                    cur.execute('''
                        SELECT n.nombreNutriente, n.descripcion, n.unidad, 
                               IFNULL(SUM(c.cantidad), 0) as consumido, 
                               o.cantidad * 7 as objetivo, 
                               n.categoria
                        FROM Nutriente n
                        LEFT JOIN contiene c ON n.id_nutriente = c.id_nutriente
                        LEFT JOIN incluye i ON c.id_alimento = i.id_alimento
                        LEFT JOIN Comida m ON i.id_comida = m.id_comida
                        LEFT JOIN Cliente cl ON m.id_cliente = cl.id_cliente
                        LEFT JOIN tiene_objetivo o ON n.id_nutriente = o.id_nutriente AND o.id_cliente = %s
                        WHERE cl.id_cliente = %s AND YEARWEEK(m.fecha, 1) = YEARWEEK(CURDATE(), 1)
                        GROUP BY n.id_nutriente, o.cantidad, n.categoria
                    ''', (id_cliente, id_cliente))
                elif frecuencia == 'mensual':
                    cur.execute('SELECT DAY(LAST_DAY(CURDATE()))')
                    dias_en_mes = cur.fetchone()[0]
                    dias = dias_en_mes
                    cur.execute('''
                        SELECT n.nombreNutriente, n.descripcion, n.unidad, 
                               IFNULL(SUM(c.cantidad), 0) as consumido, 
                               o.cantidad * %s as objetivo, 
                               n.categoria
                        FROM Nutriente n
                        LEFT JOIN contiene c ON n.id_nutriente = c.id_nutriente
                        LEFT JOIN incluye i ON c.id_alimento = i.id_alimento
                        LEFT JOIN Comida m ON i.id_comida = m.id_comida
                        LEFT JOIN Cliente cl ON m.id_cliente = cl.id_cliente
                        LEFT JOIN tiene_objetivo o ON n.id_nutriente = o.id_nutriente AND o.id_cliente = %s
                        WHERE cl.id_cliente = %s AND MONTH(m.fecha) = MONTH(CURDATE()) AND YEAR(m.fecha) = YEAR(CURDATE())
                        GROUP BY n.id_nutriente, o.cantidad, n.categoria
                    ''', (dias_en_mes, id_cliente, id_cliente))
                else:  # Por defecto, diario
                    dias = 1
                    cur.execute('''
                        SELECT n.nombreNutriente, n.descripcion, n.unidad, 
                               IFNULL(SUM(c.cantidad), 0) as consumido, 
                               o.cantidad as objetivo, 
                               n.categoria
                        FROM Nutriente n
                        LEFT JOIN contiene c ON n.id_nutriente = c.id_nutriente
                        LEFT JOIN incluye i ON c.id_alimento = i.id_alimento
                        LEFT JOIN Comida m ON i.id_comida = m.id_comida
                        LEFT JOIN Cliente cl ON m.id_cliente = cl.id_cliente
                        LEFT JOIN tiene_objetivo o ON n.id_nutriente = o.id_nutriente AND o.id_cliente = %s
                        WHERE cl.id_cliente = %s AND m.fecha = CURDATE()
                        GROUP BY n.id_nutriente, o.cantidad, n.categoria
                    ''', (id_cliente, id_cliente))

                nutrientes = cur.fetchall()

                cur.close()
                connection.close()

                # Agrupar los nutrientes por categoría
                nutrientes_por_categoria = {}
                for nutriente in nutrientes:
                    categoria = nutriente[5]
                    if categoria not in nutrientes_por_categoria:
                        nutrientes_por_categoria[categoria] = []
                    nutrientes_por_categoria[categoria].append(nutriente)

                # Ordenar nutrientes según el parámetro de ordenación
                for categoria in nutrientes_por_categoria:
                    if orden == 'mayor-menor':
                        nutrientes_por_categoria[categoria].sort(key=lambda x: (x[3] / x[4]) if x[4] > 0 else 0, reverse=True)
                    elif orden == 'menor-mayor':
                        nutrientes_por_categoria[categoria].sort(key=lambda x: (x[3] / x[4]) if x[4] > 0 else 0)
                    # 'normal' mantiene el orden original, no se requiere acción

                return render_template('inicioUsu.html', nombre=cliente[2], nutrientes_por_categoria=nutrientes_por_categoria, frecuencia=frecuencia)
            else:
                return redirect(url_for('login'))

        except Exception as e:
            return render_template('inicioUsu.html', error=f'Error al conectar a la base de datos: {e}')
    else:
        return redirect(url_for('login'))




    


    
@app.route('/añadirComida', methods=['GET', 'POST'])
def añadirComida():
    if 'email' in session:
        if request.method == 'POST':
            nombreComida = request.form['nombreComida']
            tipoComida = request.form['tipoComida']
            descripcion = request.form['descripcion']
            fecha = request.form['fecha']

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

                cur.execute('SELECT id_cliente FROM Cliente WHERE email = %s', (session['email'],))
                cliente_id = cur.fetchone()

                if cliente_id:
                    cliente_id = cliente_id[0]
                    cur.execute('INSERT INTO Comida (nombreComida, tipoComida, descripcion, fecha, id_cliente) VALUES (%s, %s, %s, %s, %s)', (nombreComida, tipoComida, descripcion, fecha, cliente_id))
                    connection.commit()

                    cur.close()
                    connection.close()

                    return redirect(url_for('añadirComida'))
                else:
                    return redirect(url_for('añadirComida'))
            except Exception as e:
                return redirect(url_for('añadirComida'))
                
        else:
            return render_template('añadirComida.html')
    else:
        return redirect(url_for('index'))
    


@app.route('/añadirAlimento', methods=['GET', 'POST'])
def añadirAlimento():
    if 'email' in session:
        
        if request.method == 'POST':
            try:
                config = {
                    'user': 'root',
                    'password': 'rootasdeg2324',
                    'host': 'db',
                    'port': '3306',
                    'database': 'usuarios'
                }

                # Conectarse a la base de datos
                connection = mysql.connect(**config)
                cur = connection.cursor()

                # Obtener los datos del formulario
                nombre_alimento = request.form['nombreAlimento']
                descripcion_alimento = request.form['descripcion']
                comida_id = request.form['comida']
                cantidadAlimento = request.form['cantidad']
                unidad = request.form['unidad']
                email_cliente = session['email']

                alimento = "100 gr de " + nombre_alimento

                print("Buscando receta para:", alimento)
                food = GoogleTranslator(source='auto', target='en').translate(alimento)
                analisis_data = analisisNutricional(food)
                analisis_data = pd.DataFrame(analisis_data)
                if analisis_data.empty:
                    return redirect(url_for('añadirAlimento'))
                else:
                    # Insertar el alimento
                    insert_alimento_query = "INSERT INTO Alimento (nombreAlimento, descripcion) VALUES (%s, %s)"
                    cur.execute(insert_alimento_query, (nombre_alimento, descripcion_alimento))
                    alimento_id = cur.lastrowid  # Obtener el ID del alimento insertado

                    # Insertar la relación en la tabla incluye
                    insert_incluye_query = "INSERT INTO incluye (id_comida, id_alimento, unidad, cantidad) VALUES (%s, %s, %s, %s)"
                    cur.execute(insert_incluye_query, (comida_id, alimento_id, unidad, cantidadAlimento))

                    # Obtener la fecha de la comida
                    cur.execute("SELECT fecha FROM Comida WHERE id_comida = %s", (comida_id,))
                    fecha_consumo = cur.fetchone()[0]

                    # Insertar nutrientes en la tabla contiene y actualizar la tabla consume
                    nutrientes = {
                        'ENERC_KCAL': 'Energia',
                        'FAT': 'Lipidos totales (grasas)',
                        'FASAT': 'Acidos grasos, saturados totales',
                        'FATRN': 'Acidos grasos, trans totales',
                        'FAMS': 'Acidos grasos monoinsaturados totales',
                        'FAPU': 'Acidos grasos poliinsaturados totales',
                        'CHOCDF': 'Carbohidratos, por diferencia',
                        'FIBTG': 'Fibra dietetica total',
                        'SUGAR': 'Azucares, total incluyendo NLEA',
                        'PROCNT': 'Proteina',
                        'CHOLE': 'Colesterol',
                        'NA': 'Sodio Na',
                        'CA': 'Calcio',
                        'MG': 'Magnesio, Mg',
                        'K': 'Potasio, K',
                        'FE': 'Hierro, Fe',
                        'ZN': 'Zinc, Zn',
                        'P': 'Fosforo, P',
                        'VITA_RAE': 'Vitamina A, RAE',
                        'VITC': 'Vitamina C, acido ascorbico total',
                        'THIA': 'Tiamina',
                        'RIBF': 'Riboflavina',
                        'NIA': 'Niacina',
                        'VITB6A': 'Vitamina B-6',
                        'FOLDFE': 'Folato, DFE',
                        'FOLFD': 'Folato, comida',
                        'FOLAC': 'Acido folico',
                        'VITB12': 'Vitamina B12',
                        'VITD': 'Vitamina D (D2 + D3)',
                        'TOCPHA': 'Vitamina E (alfa-tocoferol)',
                        'VITK1': 'Vitamina K (filoquinona)',
                        'WATER': 'Agua'
                    }

                    for nutriente, nombre in nutrientes.items():
                        if nutriente in analisis_data.index:
                            cantidad_nutriente = analisis_data.loc[nutriente, 'quantity']
                            unidad_nutriente = analisis_data.loc[nutriente, 'unit']
                            cantidad = cantidad_nutriente*float(cantidadAlimento)/100

                            # Obtener el id del nutriente
                            cur.execute("SELECT id_nutriente FROM Nutriente WHERE nombreNutriente = %s", (nombre,))
                            id_nutriente = cur.fetchone()[0]

                            # Insertar en la tabla contiene
                            insert_contiene_query = "INSERT INTO contiene (id_alimento, id_nutriente, cantidad) VALUES (%s, %s, %s)"
                            cur.execute(insert_contiene_query, (alimento_id, id_nutriente, cantidad))

                            # Actualizar la tabla consume (si el registro existe)
                            update_consume_query = """
                            INSERT INTO consume (id_cliente, id_nutriente, fecha_consumo, cantidad)
                            VALUES ((SELECT id_cliente FROM Cliente WHERE email = %s), %s, %s, %s)
                            ON DUPLICATE KEY UPDATE cantidad = cantidad + %s
                            """
                            cur.execute(update_consume_query, (email_cliente, id_nutriente, fecha_consumo, cantidad, cantidad))

                    # Guardar los cambios en la base de datos
                    connection.commit()

                    return redirect(url_for('añadirAlimento'))
            except Exception as e:
                return redirect(url_for('añadirAlimento'))
            finally:
                cur.close()
                connection.close()
        else:
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

                cur.execute('SELECT Cliente.id_cliente, Comida.id_comida, Comida.nombreComida FROM Cliente JOIN Comida ON Cliente.id_cliente = Comida.id_cliente WHERE Cliente.email = %s', (session['email'],))

                data = cur.fetchall()
                cur.close()
                connection.close()

                # Transformar los resultados en un diccionario
                comidas_dict = {row[1]: row[2] for row in data}

                return render_template('añadirAlimento.html', data=comidas_dict)
            except Exception as e:
                return redirect(url_for('añadirAlimento'))
    else:
        return redirect(url_for('login'))







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
                    return render_template('infoComida.html', analisis=analisis, query = food)
                return render_template('infoComida.html')

        else:
            return render_template('infoComida.html', analisis=None)
    else:
        return redirect(url_for('index'))
    
@app.route('/blog', methods=['GET'])
def articulos():
    return render_template('blog.html')

@app.route('/sobreNosotros', methods=['GET'])
def sobreNosotros():
    return render_template('sobreNosotros.html')

@app.route('/verAlimento/<int:id_alimento>', methods=['GET'])
def verAlimento(id_alimento):
    if 'email' in session:
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

        # Obtener información del alimento
        cur.execute("SELECT nombreAlimento, descripcion FROM Alimento WHERE id_alimento = %s", [id_alimento])
        alimento = cur.fetchone()

        if alimento:
            alimento = {
                'nombreAlimento': alimento[0],
                'descripcion': alimento[1]
            }

            # Obtener nutrientes asociados con el alimento
            cur.execute("""
                SELECT N.nombreNutriente, N.descripcion, C.cantidad, N.unidad
                FROM contiene C
                JOIN Nutriente N ON C.id_nutriente = N.id_nutriente
                WHERE C.id_alimento = %s
            """, [id_alimento])
            nutrientes = cur.fetchall()

            cur.close()
            connection.close()

            return render_template('verAlimento.html', alimento=alimento, nutrientes=nutrientes)
        else:
            cur.close()
            connection.close()
            return redirect(url_for('misComidas'))
    else:
        return redirect(url_for('index'))


@app.route('/verComida/<int:id_comida>', methods=['GET'])
def verComida(id_comida):
    if 'email' in session:
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

        # Obtener información de la comida
        cur.execute("SELECT * FROM Comida WHERE id_comida = %s", [id_comida])
        comida = cur.fetchone()

        if comida:
            # Obtener alimentos y nutrientes asociados con la comida
            cur.execute("""
                SELECT A.nombreAlimento, A.descripcion, I.cantidad, I.unidad, A.id_alimento
                FROM incluye I
                JOIN Alimento A ON I.id_alimento = A.id_alimento
                WHERE I.id_comida = %s
            """, [id_comida])
            alimentos = cur.fetchall()

            cur.close()
            connection.close()

            return render_template('verComida.html', comida=comida, alimentos=alimentos)
        else:
            cur.close()
            connection.close()
            return redirect(url_for('misComidas'))
    else:
        return redirect(url_for('index'))

import math
def convertir_tiempo_a_minutos(tiempo_str):
    tiempo_minutos = 0
    if 'h' in tiempo_str:
        partes = tiempo_str.split('h')
        tiempo_minutos += int(partes[0]) * 60
        if 'm' in partes[1]:
            tiempo_minutos += int(partes[1].replace('m', '').strip())
    elif 'm' in tiempo_str:
        tiempo_minutos += int(tiempo_str.replace('m', '').strip())
    return tiempo_minutos
@app.route('/recetas', methods=['GET', 'POST'])
def recetas():
    if 'email' in session:
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

        recetas_por_pagina = 9
        pagina_actual = request.args.get('pagina', 1, type=int)
        offset = (pagina_actual - 1) * recetas_por_pagina

        ingredientes = categoria = tiempo_min = tiempo_max = tipo = dificultad = valoracion = None
        if request.method == 'POST':
            ingredientes = request.form.get('ingredientes')
            categoria = request.form.getlist('categoria')
            tiempo_min = request.form.get('tiempo_min', type=int)
            tiempo_max = request.form.get('tiempo_max', type=int)
            tipo = request.form.get('tipo')
            dificultad = request.form.get('dificultad')
            valoracion = request.form.get('valoracion', type=float)
        else:
            if 'ingredientes' in request.args:
                ingredientes = request.args.get('ingredientes')
            if 'categoria' in request.args:
                categoria = request.args.getlist('categoria')
            if 'tiempo_min' in request.args:
                tiempo_min = request.args.get('tiempo_min', type=int)
            if 'tiempo_max' in request.args:
                tiempo_max = request.args.get('tiempo_max', type=int)
            if 'tipo' in request.args:
                tipo = request.args.get('tipo')
            if 'dificultad' in request.args:
                dificultad = request.args.get('dificultad')
            if 'valoracion' in request.args:
                valoracion = request.args.get('valoracion', type=float)

        if categoria is None:
            categoria = []

        query_count = "SELECT COUNT(*) FROM recetas WHERE images IS NOT NULL AND images != ''"
        query_recetas = "SELECT * FROM recetas WHERE images IS NOT NULL AND images != ''"

        filters = []
        params = []

        if ingredientes:
            filters.append("nombre LIKE %s")
            params.append('%' + ingredientes + '%')
        if categoria:
            filters.append("categoria IN (%s)" % ','.join(['%s']*len(categoria)))
            params.extend(categoria)
        if tiempo_min is not None and tiempo_max is not None:
            filters.append("""
                (
                    tiempo LIKE %s AND CAST(SUBSTRING_INDEX(tiempo, 'h', 1) AS UNSIGNED) * 60 + CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(tiempo, ' ', -1), 'm', 1) AS UNSIGNED) BETWEEN %s AND %s
                )
                OR 
                (
                    tiempo LIKE %s AND CAST(SUBSTRING_INDEX(tiempo, 'm', 1) AS UNSIGNED) BETWEEN %s AND %s
                )
            """)
            params.extend(['%h%', tiempo_min, tiempo_max, '%m%', tiempo_min, tiempo_max])
        if dificultad:
            filters.append("dificultad = %s")
            params.append(dificultad)
        if valoracion:
            filters.append("valoracion >= %s")
            params.append(valoracion)

        if filters:
            filter_clause = " AND " + " AND ".join(filters)
            query_count += filter_clause
            query_recetas += filter_clause

        params_count = params.copy()
        params_count.extend([recetas_por_pagina, offset])

        query_recetas += " LIMIT %s OFFSET %s"
        params.extend([recetas_por_pagina, offset])

        print(f"query_count: {query_count}, params: {params}")
        print(f"query_recetas: {query_recetas}, params: {params}")

        cur.execute(query_count, tuple(params[:len(params_count) - 2]))
        total_recetas = cur.fetchone()[0]

        cur.execute(query_recetas, tuple(params))
        recetas = cur.fetchall()

        total_paginas = math.ceil(total_recetas / recetas_por_pagina)

        if recetas:
            recetas = [{'id_receta': receta[0], 'categoria': receta[1], 'nombre': receta[2], 
                        'valoracion': receta[3], 'dificultad': receta[4], 'num_comensales': receta[5], 
                        'tiempo': receta[6], 'tipo': receta[7], 'link_receta': receta[8], 
                        'num_comentarios': receta[9], 'num_reviews': receta[10], 'fecha_modificacion': receta[11], 
                        'ingredientes': receta[12], 'imagen': receta[13]} for receta in recetas]
            cur.close()
            connection.close()
            return render_template('recetas.html', recetas=recetas, total_paginas=total_paginas, pagina_actual=pagina_actual, max=max, min=min, ingredientes=ingredientes, categoria=categoria, tiempo_min=tiempo_min, tiempo_max=tiempo_max, tipo=tipo, dificultad=dificultad, valoracion=valoracion)
        else:
            cur.close()
            connection.close()
            return render_template('recetas.html', total_paginas=total_paginas, pagina_actual=pagina_actual, max=max, min=min, ingredientes=ingredientes, categoria=categoria, tiempo_min=tiempo_min, tiempo_max=tiempo_max, tipo=tipo, dificultad=dificultad, valoracion=valoracion)
    else:
        return redirect(url_for('index'))






@app.route('/misComidas', methods=['GET'])
def misComidas():
    if 'email' in session:
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

        cur.execute("SELECT id_cliente FROM Cliente WHERE email = %s", [email])

        cliente = cur.fetchall()
        if cliente:
            cliente = cliente[0][0]
            cur.execute("SELECT * FROM Comida WHERE id_cliente = %s", [cliente])
            comidas = cur.fetchall()
            cur.close()
            connection.close()
            return render_template('misComidas.html', comidas=comidas)
        else:
            cur.close()
            connection.close()
            return render_template('inicioUsu.html')
    else:
        return redirect(url_for('index'))
    

@app.route('/borrarAlimento/<int:id_alimento>', methods=['POST'])
def borrarAlimento(id_alimento):
    if 'email' in session:
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

        try:
            cur.execute("SELECT id_comida FROM incluye WHERE id_alimento = %s", [id_alimento])
            comida = cur.fetchone()

            if comida:
                cur.execute("DELETE FROM incluye WHERE id_alimento = %s", [id_alimento])
                cur.execute("DELETE FROM contiene WHERE id_alimento = %s", [id_alimento])
                cur.execute("DELETE FROM Alimento WHERE id_alimento = %s", [id_alimento])
                connection.commit()
                return redirect(url_for('misComidas'))
            else:
                return redirect(url_for('misComidas'))
        except Exception as e:
            connection.rollback()
            return redirect(url_for('misComidas'))
        finally:
            cur.close()
            connection.close()
    else:
        return redirect(url_for('index'))
    
@app.route('/borrarComida/<int:id_comida>', methods=['POST'])
def borrarComida(id_comida):
    if 'email' in session:
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
        
        try:
            cur.execute("SELECT id_alimento FROM incluye WHERE id_comida = %s", [id_comida])
            alimentos = cur.fetchall()

            # Primero eliminar los registros en la tabla incluye
            cur.execute("DELETE FROM incluye WHERE id_comida = %s", [id_comida])
            
            # Luego eliminar la comida en sí
            cur.execute("DELETE FROM Comida WHERE id_comida = %s", [id_comida])

            for alimento in alimentos:
                cur.execute("DELETE FROM contiene WHERE id_alimento = %s", [alimento[0]])
                cur.execute("DELETE FROM Alimento WHERE id_alimento = %s", [alimento[0]])
            
            connection.commit()
        except Exception as e:
            connection.rollback()
        finally:
            cur.close()
            connection.close()
        
        return redirect(url_for('misComidas'))
    else:
        return redirect(url_for('index'))




@app.route('/articulosDeTemporada', methods=['GET'])
def articulosDeTemporada():
    if 'email' in session:
        email = session['email']
        config = {
            'user': 'root',
            'password': 'rootasdeg2324',
            'host': 'db',
            'port': '3306',
            'database': 'usuarios'
        }

        mes_seleccionado = request.args.get('mes', datetime.now().strftime("%b"))
        meses_en_espanol = {
            'Ene': 'ENERO',
            'Feb': 'FEBRERO',
            'Mar': 'MARZO',
            'Abr': 'ABRIL',
            'May': 'MAYO',
            'Jun': 'JUNIO',
            'Jul': 'JULIO',
            'Ago': 'AGOSTO',
            'Sep': 'SEPTIEMBRE',
            'Oct': 'OCTUBRE',
            'Nov': 'NOVIEMBRE',
            'Dic': 'DICIEMBRE'
        }
        mes_actual = meses_en_espanol.get(mes_seleccionado)

        try:
            connection = mysql.connect(**config)
            cur = connection.cursor()

            cur.execute("SELECT * FROM productos")
            productos = cur.fetchall()
            cur.close()
            connection.close()

            in_season = []
            out_of_season = []
            start_of_season = []

            for producto in productos:
                temporada = producto[2]  # Suponiendo que la temporada actual está en la columna 1
                inicio_temporada = producto[3]  # Suponiendo que el inicio de temporada está en la columna 2

                if temporada is not None and mes_actual in temporada:
                    in_season.append(producto)
                elif inicio_temporada is not None and mes_actual in inicio_temporada:
                    start_of_season.append(producto)
                else:
                    out_of_season.append(producto)

            return render_template(
                'articulosDeTemporada.html', 
                in_season=in_season, 
                out_of_season=out_of_season, 
                start_of_season=start_of_season,
                current_month=mes_seleccionado
            )
        except Exception as e:
            return render_template('articulosDeTemporada.html', current_month=mes_seleccionado)
    else:
        return redirect(url_for('index'))

#####################################################################################################################################
###################################################### Funciones Auxiliares ##############################################################
#####################################################################################################################################
def generar_contraseña():
    longitud = 12
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(choice(caracteres) for _ in range(longitud))

def generar_token(correo):
    token = serializer.dumps(correo, salt=app.secret_key)
    return token

# Verificar token
def verificar_token(token, expiration=3600):
    try:
        email = serializer.loads(token, salt=app.secret_key, max_age=expiration)
    except:
        return False
    return email

def send_email(email_receiver, opcion, token=None, nombre=None):
    password = 'rzxz jhtf lbxf tqus'
    email_sender = 'veganmaniiaa@gmail.com'
    if opcion == 0:
        subject = "Recuperación de Contraseña"
        message = render_template('mails/reset_password.html', link=f'http://localhost:5000/reset_password?token={token}')
    elif opcion == 1:
        subject = "Bienvenido a VeganMania"
        message = render_template('mails/welcomeMail.html')
    else:
        subject = "Verificación de Cuenta"
        message = render_template('mails/verificarMail.html', link=f'http://localhost:5000/verificar_email?token={token}', nombre=nombre)

    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        server.quit()
        print("Correo enviado")
    except Exception as e:
        print(f"Error al enviar correo: {e}")



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)