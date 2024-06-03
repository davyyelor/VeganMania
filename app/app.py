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


app = Flask(__name__)
from flask import render_template, request, flash, url_for, redirect, session
import mysql.connector as mysql
app.config['SECRET_KEY'] = 'abcd1234@'
app.config['SESSION_TYPE'] = 'filesystem'  
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
                flash('¡Usuario modificado correctamente!', 'success')
                return redirect(url_for('modificarUsuario'))

            else:
                flash('¡No se encontró un usuario con ese email!', 'error')
                return redirect(url_for('modificarUsuario'))

        except Exception as e:
            flash(f'¡Error al modificar el usuario: {str(e)}', 'error')
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

            cur.execute('SELECT * FROM Cliente WHERE email = %s', (email,))
            user = cur.fetchone()

            if user:
                flash('¡Ya existe un usuario con ese email!', 'error')
                return redirect(url_for('registro'))

            hashed_password = hashlib.sha256(contrasena.encode('utf-8')).hexdigest()

            # Insertar datos del nuevo cliente
            cur.execute('INSERT INTO Cliente (nombre, nombre_usu, email, contrasena, peso, altura, genero, actividad, fecha_nacimiento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', (nombre, usuario, email, hashed_password, peso, altura, genero, actividad, fechaNacimiento))
            connection.commit()

            # Obtener el id_cliente del nuevo cliente
            cliente_id = cur.execute('SELECT id_cliente FROM Cliente WHERE email = %s', (email,))
            cliente_id = cur.fetchone()[0]

            if cliente_id:
                # Insertar registros en la tabla consume para todos los nutrientes con cantidad 0
                cur.execute('INSERT INTO consume (id_cliente, id_nutriente, fecha_consumo, cantidad) SELECT %s, n.id_nutriente, CURDATE(), 0 FROM Nutriente n', (cliente_id,))
                connection.commit()

                # Establecer un objetivo de 2000 para todos los nutrientes para el nuevo cliente
                cur.execute('INSERT INTO tiene_objetivo (id_cliente, id_nutriente, cantidad) SELECT %s, id_nutriente, 2000 FROM Nutriente', (cliente_id,))
                connection.commit()

                cur.close()
                connection.close()

                # Envío de correo electrónico, etc.

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

@app.route('/recuperarContraseña/<token>')
def mostrar_contraseña(token):
    try:
        correo = serializer.loads(token, max_age=3600)
        # Aquí deberías permitir al usuario cambiar su contraseña
        nueva_contraseña = generar_contraseña()
        return f"Tu nueva contraseña es: {nueva_contraseña}"
    except:
        return "El enlace de recuperación de contraseña es inválido o ha expirado."


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
                token = generar_token(email)
                contraseña = generar_contraseña()
                enlace = f"http://localhost:5000/recuperarContraseña/{token}"
                
                send_email(email, 0, link=enlace)
    
                cn = hashAPI.hashear(contraseña)
    
                cur.execute('UPDATE Cliente SET contrasena = %s WHERE email = %s', (cn, email))
                connection.commit()
                cur.close()
                connection.close()
                flash('¡Contraseña recuperada con éxito!', 'success')
                flash(f'El enlace de recuperación de contraseña es: {enlace}', 'info')
                return render_template('recuperarContrasena.html', email=email)
            else:
                flash('No se encontró ningún usuario con ese correo electrónico', 'error')
                return render_template('recuperarContrasena.html')
        except Exception as e:
            flash(f'Error al recuperar la contraseña: {str(e)}', 'error')
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
            cur.execute('SELECT id_cliente, contrasena FROM Cliente WHERE email = %s AND contrasena = %s', (email, cn))
            user = cur.fetchone()

            if user and user[1] == cn:
                session['email'] = email
                flash('¡Inicio de sesión exitoso!', 'success')

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
@app.route('/inicioUsu', methods=['GET', 'POST'])
def inicioUsu():
    if 'email' in session:
        try:
            email = session['email']
            frecuencia = request.args.get('frecuencia', 'diario')  # Obtener la frecuencia seleccionada
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
                               IFNULL(SUM(cn.cantidad), 0) as consumido, 
                               o.cantidad * 7 as objetivo, 
                               n.categoria
                        FROM Nutriente n
                        LEFT JOIN contiene c ON n.id_nutriente = c.id_nutriente
                        LEFT JOIN incluye i ON c.id_alimento = i.id_alimento
                        LEFT JOIN Comida m ON i.id_comida = m.id_comida
                        LEFT JOIN Cliente cl ON m.id_cliente = cl.id_cliente
                        LEFT JOIN (
                            SELECT id_cliente, id_nutriente, SUM(cantidad) as cantidad
                            FROM consume
                            WHERE id_cliente = %s AND YEARWEEK(fecha_consumo, 1) = YEARWEEK(CURDATE(), 1)
                            GROUP BY id_cliente, id_nutriente
                        ) cn ON n.id_nutriente = cn.id_nutriente
                        LEFT JOIN tiene_objetivo o ON n.id_nutriente = o.id_nutriente AND o.id_cliente = %s
                        WHERE cl.id_cliente = %s AND YEARWEEK(m.fecha, 1) = YEARWEEK(CURDATE(), 1)
                        GROUP BY n.id_nutriente, o.cantidad, n.categoria
                    ''', (id_cliente, id_cliente, id_cliente))
                elif frecuencia == 'mensual':
                    cur.execute('SELECT DAY(LAST_DAY(CURDATE()))')
                    dias_en_mes = cur.fetchone()[0]
                    dias = dias_en_mes
                    cur.execute('''
                        SELECT n.nombreNutriente, n.descripcion, n.unidad, 
                               IFNULL(SUM(cn.cantidad), 0) as consumido, 
                               o.cantidad * %s as objetivo, 
                               n.categoria
                        FROM Nutriente n
                        LEFT JOIN contiene c ON n.id_nutriente = c.id_nutriente
                        LEFT JOIN incluye i ON c.id_alimento = i.id_alimento
                        LEFT JOIN Comida m ON i.id_comida = m.id_comida
                        LEFT JOIN Cliente cl ON m.id_cliente = cl.id_cliente
                        LEFT JOIN (
                            SELECT id_cliente, id_nutriente, SUM(cantidad) as cantidad
                            FROM consume
                            WHERE id_cliente = %s AND MONTH(fecha_consumo) = MONTH(CURDATE()) AND YEAR(fecha_consumo) = YEAR(CURDATE())
                            GROUP BY id_cliente, id_nutriente
                        ) cn ON n.id_nutriente = cn.id_nutriente
                        LEFT JOIN tiene_objetivo o ON n.id_nutriente = o.id_nutriente AND o.id_cliente = %s
                        WHERE cl.id_cliente = %s AND MONTH(m.fecha) = MONTH(CURDATE()) AND YEAR(m.fecha) = YEAR(CURDATE())
                        GROUP BY n.id_nutriente, o.cantidad, n.categoria
                    ''', (dias_en_mes, id_cliente, id_cliente, id_cliente))
                else:  # Por defecto, diario
                    dias = 1
                    cur.execute('''
                        SELECT n.nombreNutriente, n.descripcion, n.unidad, 
                               IFNULL(SUM(cn.cantidad), 0) as consumido, 
                               o.cantidad as objetivo, 
                               n.categoria
                        FROM Nutriente n
                        LEFT JOIN contiene c ON n.id_nutriente = c.id_nutriente
                        LEFT JOIN incluye i ON c.id_alimento = i.id_alimento
                        LEFT JOIN Comida m ON i.id_comida = m.id_comida
                        LEFT JOIN Cliente cl ON m.id_cliente = cl.id_cliente
                        LEFT JOIN (
                            SELECT id_cliente, id_nutriente, SUM(cantidad) as cantidad
                            FROM consume
                            WHERE id_cliente = %s AND fecha_consumo = CURDATE()
                            GROUP BY id_cliente, id_nutriente
                        ) cn ON n.id_nutriente = cn.id_nutriente
                        LEFT JOIN tiene_objetivo o ON n.id_nutriente = o.id_nutriente AND o.id_cliente = %s
                        WHERE cl.id_cliente = %s AND m.fecha = CURDATE()
                        GROUP BY n.id_nutriente, o.cantidad, n.categoria
                    ''', (id_cliente, id_cliente, id_cliente))

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

                return render_template('inicioUsu.html', nutrientes_por_categoria=nutrientes_por_categoria, frecuencia=frecuencia)

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
                    flash('¡Comida añadida correctamente!', 'success')

                    return redirect(url_for('añadirComida'))
                else:
                    flash('No se encontró al usuario en la base de datos.', 'error')
                    return redirect(url_for('añadirComida'))
            except Exception as e:
                flash(f'Error al cargar la página de inicio: {str(e)}', 'error')
                return redirect(url_for('añadirComida'))
                
        else:
            flash('¡Por favor, rellena todos los campos!', 'error')
            return render_template('añadirComida.html')
    else:
        flash('Acceso no autorizado. Por favor, inicia sesión.', 'error')
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
                cantidad = request.form['cantidad']
                unidad = request.form['unidad']
                email_cliente = session['email']

                alimento = "100 gr de " + nombre_alimento

                print("Buscando receta para:", alimento)
                food = GoogleTranslator(source='auto', target='en').translate(alimento)
                analisis_data = analisisNutricional(food)
                analisis_data = pd.DataFrame(analisis_data)
                if analisis_data.empty:
                    flash('No se pudo realizar el análisis nutricional.', 'error')
                    return redirect(url_for('añadirAlimento'))
                else:
                    # Insertar el alimento
                    insert_alimento_query = "INSERT INTO Alimento (nombreAlimento, descripcion) VALUES (%s, %s)"
                    cur.execute(insert_alimento_query, (nombre_alimento, descripcion_alimento))
                    alimento_id = cur.lastrowid  # Obtener el ID del alimento insertado

                    # Insertar la relación en la tabla incluye
                    insert_incluye_query = "INSERT INTO incluye (id_comida, id_alimento, unidad, cantidad) VALUES (%s, %s, %s, %s)"
                    cur.execute(insert_incluye_query, (comida_id, alimento_id, unidad, cantidad))

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

                            # Obtener el id del nutriente
                            cur.execute("SELECT id_nutriente FROM Nutriente WHERE nombreNutriente = %s", (nombre,))
                            id_nutriente = cur.fetchone()[0]

                            # Insertar en la tabla contiene
                            insert_contiene_query = "INSERT INTO contiene (id_alimento, id_nutriente, cantidad) VALUES (%s, %s, %s)"
                            cur.execute(insert_contiene_query, (alimento_id, id_nutriente, cantidad_nutriente))

                            # Actualizar la tabla consume (si el registro existe)
                            update_consume_query = """
                            INSERT INTO consume (id_cliente, id_nutriente, fecha_consumo, cantidad)
                            VALUES ((SELECT id_cliente FROM Cliente WHERE email = %s), %s, %s, %s)
                            ON DUPLICATE KEY UPDATE cantidad = cantidad + %s
                            """
                            cur.execute(update_consume_query, (email_cliente, id_nutriente, fecha_consumo, cantidad_nutriente, cantidad_nutriente))

                    # Guardar los cambios en la base de datos
                    connection.commit()

                    flash('Alimento y nutrientes añadidos correctamente.', 'success')
                    return redirect(url_for('añadirAlimento'))
            except Exception as e:
                flash(f'Error al añadir el alimento: {str(e)}', 'error')
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
                flash(f'Error al cargar la página de inicio: {str(e)}', 'error')
                return redirect(url_for('añadirAlimento'))
    else:
        flash('Acceso no autorizado. Por favor, inicia sesión.', 'error')
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
                    flash('¡Análisis nutricional realizado con éxito!', 'success')
                    return render_template('infoComida.html', analisis=analisis, query = food)
                flash('¡No se pudo realizar el análisis nutricional!', 'error')
                return render_template('infoComida.html')

        else:
            return render_template('infoComida.html', analisis=None)
    else:
        flash('Acceso no autorizado. Por favor, inicia sesión.', 'error')
        return redirect(url_for('index'))
    
@app.route('/blog', methods=['GET'])
def articulos():
    return render_template('blog.html')

@app.route('/sobreNosotros', methods=['GET'])
def sobreNosotros():
    return render_template('sobreNosotros.html')

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
                SELECT A.nombreAlimento, A.descripcion, I.cantidad, I.unidad
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
            flash('No se encontró la comida especificada.', 'error')
            return redirect(url_for('misComidas'))
    else:
        flash('Acceso no autorizado. Por favor, inicia sesión.', 'error')
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
            flash('¡Comidas cargadas correctamente!', 'success')
            return render_template('misComidas.html', comidas=comidas)
        else:
            cur.close()
            connection.close()
            flash('No se encontró al usuario en la base de datos.', 'error')
            return render_template('inicioUsu.html')
    else:
        flash('Acceso no autorizado. Por favor, inicia sesión.', 'error')
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
            # Primero eliminar los registros en la tabla incluye
            cur.execute("DELETE FROM incluye WHERE id_comida = %s", [id_comida])
            
            # Luego eliminar la comida en sí
            cur.execute("DELETE FROM Comida WHERE id_comida = %s", [id_comida])
            
            connection.commit()
            flash('¡Comida eliminada correctamente!', 'success')
        except Exception as e:
            connection.rollback()
            flash(f'Error al eliminar la comida: {e}', 'error')
        finally:
            cur.close()
            connection.close()
        
        return redirect(url_for('misComidas'))
    else:
        flash('Acceso no autorizado. Por favor, inicia sesión.', 'error')
        return redirect(url_for('index'))



@app.route('/articulosDeTemporada', methods=['GET'])
def articulosDeTemporada():
    in_season_images = os.listdir('./static/images/products/in_season')
    out_of_season_images = os.listdir('./static/images/products/out_of_season')
    start_of_season_images = os.listdir('./static/images/products/start_of_season')
    return render_template('articulosDeTemporada.html', in_season_images=in_season_images, out_of_season_images=out_of_season_images, start_of_season_images=start_of_season_images)

#####################################################################################################################################
###################################################### Funciones Auxiliares ##############################################################
#####################################################################################################################################
def generar_contraseña():
    longitud = 12
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(choice(caracteres) for _ in range(longitud))

def generar_token(correo):
    token = serializer.dumps(correo)
    return token

def send_email(email_receiver, opcion, link):
    password = 'rzxz jhtf lbxf tqus'
    email_sender = 'veganmaniiaa@gmail.com'
    if opcion == 0:
        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = "Recuperación de Contraseña"

        message = render_template('mails/reset_password.html', link=link)

        msg.attach(MIMEText(message, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        print("enviado")
        server.quit()        

    elif opcion == 1:
        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = "Bienvenido a VeganMania"

        message = render_template('mails/welcomeMail.html')

        msg.attach(MIMEText(message, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        print("enviado")
        server.quit()    



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)