from flask import Flask
import datetime
import re

app = Flask(__name__)
from flask import render_template, request, flash, url_for, redirect, session
import mysql.connector as mysql
app.config['SECRET_KEY'] = 'abcd1234@'
app.config['SESSION_TYPE'] = 'filesystem'  # Puedes elegir otro tipo de sesión

'''
La ruta raíz '/' se asocia a la función index(), que renderiza una plantilla HTML llamada 'index.html'. Esta ruta se utiliza para mostrar la página principal de la aplicación.
'''
@app.route('/')
def index():
   return render_template('index2.html')


from datetime import datetime

def calcular_calorias_objetivo(fecha_nacimiento, genero):
    edad = datetime.now().year - fecha_nacimiento.year

    if 0 <= edad <= 0.5:
        return 650
    elif 0.5 < edad <= 1:
        return 850
    elif 1 < edad <= 3:
        return 1300
    elif 4 < edad <= 6:
        return 1800
    elif 7 < edad <= 10:
        return 2000
    elif genero == 'Hombre' and 11 < edad <= 14:
        return 2500
    elif genero == 'Hombre' and 15 < edad <= 18:
        return 3000
    elif genero == 'Hombre' and 19 < edad <= 24:
        return 2900
    elif genero == 'Hombre' and 25 < edad <= 50:
        return 2900
    elif genero == 'Hombre' and edad > 50:
        return 2300
    elif genero == 'Mujer' and 11 < edad <= 14:
        return 2200
    elif genero == 'Mujer' and 15 < edad <= 18:
        return 2200
    elif genero == 'Mujer' and 19 < edad <= 24:
        return 2200
    elif genero == 'Mujer' and 25 < edad <= 50:
        return 2200
    elif genero == 'Mujer' and edad > 50:
        return 1900
    else:
        return 0



def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

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

            # Insertar datos en la tabla clientes
            cur.execute('SELECT * FROM clientes WHERE email = %s', (email,))
            user = cur.fetchone()

            if not nombre or not usuario or not email or not contrasena or not fechaNacimiento or not peso or not altura or not genero:
                flash('Por favor, rellena todos los campos.', 'error')
                return redirect(url_for('registro'))
            
            if not validate_email(email):
                flash('El correo electrónico no cumple con el formato requerido. Por favor, utiliza otro correo.', 'error')
                return redirect(url_for('registro'))

            if user:
                flash('¡Ya existe un usuario con ese email!', 'error')
                return redirect(url_for('registro'))
            


            # Insertar datos en la tabla clientes
            cur.execute('INSERT INTO clientes (nombre, usuario, email, contrasena, fechaNacimiento, peso, altura, genero) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (nombre, usuario, email, contrasena, fechaNacimiento, peso, altura, genero))
            connection.commit()


            update_query = """
            UPDATE clientes
            SET calorias_objetivo = 
                CASE 
                    WHEN TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 0 AND 0.5 THEN 650
                    WHEN TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 0.5 AND 1 THEN 850
                    WHEN TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 1 AND 3 THEN 1300
                    WHEN TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 4 AND 6 THEN 1800
                    WHEN TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 7 AND 10 THEN 2000
                    WHEN genero = 'Hombre' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 11 AND 14 THEN 2500
                    WHEN genero = 'Hombre' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 15 AND 18 THEN 3000
                    WHEN genero = 'Hombre' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 19 AND 24 THEN 2900
                    WHEN genero = 'Hombre' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 25 AND 50 THEN 2900
                    WHEN genero = 'Hombre' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) > 50 THEN 2300
                    WHEN genero = 'Mujer' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 11 AND 14 THEN 2200
                    WHEN genero = 'Mujer' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 15 AND 18 THEN 2200
                    WHEN genero = 'Mujer' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 19 AND 24 THEN 2200
                    WHEN genero = 'Mujer' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 25 AND 50 THEN 2200
                    WHEN genero = 'Mujer' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) > 50 THEN 1900
                    ELSE 0 
                END;
            """
            cur.execute(update_query)
            connection.commit()

            # Obtener el ID del cliente recién registrado
            cur.execute('SELECT id FROM clientes WHERE email = %s', (email,))
            cliente_id = cur.fetchone()

            if cliente_id:  # Verificar si se encontró el ID del cliente
                cliente_id = cliente_id[0]  # Convertir la tupla en un valor único (ID)
                try:
                    # Insertar un registro en la tabla registro_calorias_diario
                    fecha_actual = datetime.now().date()
                    cur.execute('INSERT INTO registro_calorias_diario (cliente_id, calorias_consumidas, fecha_consumo) VALUES (%s, %s, %s)', (cliente_id, 0, fecha_actual))
                    connection.commit()

                    cur.close()
                    connection.close()
                except Exception as e:
                    flash(f'¡Error al insertar en la base de datos: {str(e)}', 'error')
        except Exception as e:
            flash(f'¡Error al insertar en la base de datos: {str(e)}', 'error')

        return redirect(url_for('login'))

    else:
        return render_template('registro.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

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

            return redirect(url_for('buenHome'))
        except Exception as e:
            flash(f'¡Error al añadir las calorías: {str(e)}', 'error')

    return render_template('BuenHome.html')




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
            cur.execute('SELECT id FROM clientes WHERE email = %s AND contrasena = %s', (email, contrasena))
            user = cur.fetchone()

            if user:
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
                return redirect(url_for('buenHome'))

            else:
                flash('Credenciales incorrectas. Inténtalo de nuevo.', 'error')

        except Exception as e:
            flash(f'Error al iniciar sesión: {str(e)}', 'error')

    return render_template('login.html')


@app.route('/admin')
def admin():
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
        cur.execute('SELECT * FROM clientes')
        data=cur.fetchall()
        cur.close()
        connection.close()
        flash('¡Operación completada con éxito!', 'success')
    except Exception as e:
        flash('¡Error al obtener los clientes de la base de datos:', 'error')   
    return render_template('admin.html', usuarios=data)


@app.route('/buenHome')
def buenHome():
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

                return render_template('buenHome.html', nombre=nombre, calorias_objetivo=calorias_objetivo, calorias_consumidas=calorias_consumidas, calorias_restantes=calorias_restantes)
            # Obtener el ID del cliente actual
        except Exception as e:
            flash(f'Error al cargar la página de inicio: {str(e)}', 'error')

        return redirect(url_for('login'))

    else:
        flash('Acceso no autorizado. Por favor, inicia sesión.', 'error')
        return redirect(url_for('login'))



def actualizarDia():
    today = datetime.date.today()
    last_date = session.get('last_date')

    # Si la fecha ha cambiado desde la última solicitud
    if last_date != today:
        try:
            config = {
                'user': 'root',
                'password': 'rootasdeg2324',
                'host': 'db',
                'port': '3306',
                'database': 'usuarios'
            }

            connection = mysql.connect(**config)
            cursor = connection.cursor()

            # Actualizar las calorías objetivo para todos los usuarios
            update_query = """
            UPDATE clientes
            SET calorias_objetivo = 
                CASE 
                    WHEN TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 0 AND 0.5 THEN 650
                    WHEN TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 0.5 AND 1 THEN 850
                    WHEN TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 1 AND 3 THEN 1300
                    WHEN TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 4 AND 6 THEN 1800
                    WHEN TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 7 AND 10 THEN 2000
                    WHEN genero = 'Hombre' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 11 AND 14 THEN 2500
                    WHEN genero = 'Hombre' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 15 AND 18 THEN 3000
                    WHEN genero = 'Hombre' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 19 AND 24 THEN 2900
                    WHEN genero = 'Hombre' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 25 AND 50 THEN 2900
                    WHEN genero = 'Hombre' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) > 50 THEN 2300
                    WHEN genero = 'Mujer' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 11 AND 14 THEN 2200
                    WHEN genero = 'Mujer' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 15 AND 18 THEN 2200
                    WHEN genero = 'Mujer' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 19 AND 24 THEN 2200
                    WHEN genero = 'Mujer' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) BETWEEN 25 AND 50 THEN 2200
                    WHEN genero = 'Mujer' AND TIMESTAMPDIFF(YEAR, fechaNacimiento, CURDATE()) > 50 THEN 1900
                    ELSE 0 
                END;
            """
            cursor.execute(update_query)
            connection.commit()

            cursor.close()
            connection.close()

            # Actualizar la fecha de la última solicitud en la sesión
            session['last_date'] = today

        except Exception as e:
            # Manejar cualquier error que pueda ocurrir durante la actualización
            flash(f'Error al actualizar las calorías: {str(e)}', 'error')




'''
@app.route('/borrar/<string:id>')
def borrar_cliente(id):
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
        cur.execute('DELETE FROM clientes WHERE id= %s',(id))
        data=cur.fetchall()
        cur.close()
        connection.close()
        flash('¡Correctamente borrado!', 'success')
    except Exception as e:
        flash('¡Error al borrar en la base de datos:', 'error')   
    return redirect (url_for('admin'))   
  
'''
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
