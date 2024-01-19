# Proyecto VeganMania
Una aplicación Python Flask + MySQL 5.7 + Nginx en Docker Compose.

***Documentación básica de la app***

David Elorza

## Tabla de contenido
- [Contribuir](#contribuir).
- [Requisitos Windows](#requisitos-windows).
- [Requisitos Linux](#requisitos-linux).
  - [Instalación Docker](#instalacion-docker).
  - [Instalación Chrome](#instalacion-chrome).


### Contribuir

Utiliza las opciones de GitHub como **Pull Request** o un **Fork** para colaborar con el proyecto:

**Fork**: Hace un clon de este repositorio en tu cuenta de GitHub. En el podrás hacer modificaciones o simplemente para tener una copia (con opción de clonarlo a tu PC también). De esa forma garantizas la información para tu uso personal.

**Pull Request**: Envía la sugerencias de cambio para este repositorio, los cuales hicistes en tu clon. Si son aceptadas por el master, se fucionan los cambios y el repositorio del proyecto queda actualizado.

### Requisitos Windows

(Es una forma de hacerlo)
- IDE para ejecutar todo el programa, se ha usado VS Code
- Docker Desktop para poder administrar los contenedores e imágenes creados y utilizados.

Para descargar ambas buscar en Internet y descargar la versión más reciente:
- Link VSCode: https://code.visualstudio.com/download
- Link Docker Desktop: https://docs.docker.com/desktop/install/windows-install/

### Requisitos Linux

#### Instalación Docker
(Es una forma de hacerlo)
- Docker 
- Se recomienda usar Google Chrome o Chromium en su defecto

Para instalar Docker:
Primero, actualice su lista de paquetes existente:
```bash
$ sudo apt update
```

A continuación, instale algunos paquetes de requisitos previos que permitan a apt usar paquetes a través de HTTPS:
```bash
$ sudo apt install apt-transport-https ca-certificates curl software-properties-common
```
Luego, añada la clave de GPG para el repositorio oficial de Docker en su sistema:
```bash
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

Agregue el repositorio de Docker a las fuentes de APT:
```bash
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
```

A continuación, actualice el paquete de base de datos con los paquetes de Docker del repositorio recién agregado:
```bash
$ sudo apt update
```

Asegúrese de estar a punto de realizar la instalación desde el repositorio de Docker en lugar del repositorio predeterminado de Ubuntu:
```bash
$ apt-cache policy docker-ce
```
Si bien el número de versión de Docker puede ser distinto, verá un resultado como el siguiente:
Observe que docker-ce no está instalado, pero la opción más viable para la instalación es del repositorio de Docker para Ubuntu 20.04 (focal).

Por último, instale Docker:
```bash
$ sudo apt install docker-ce
```

Con esto, Docker quedará instalado, el demonio se iniciará y el proceso se habilitará para ejecutarse en el inicio. Compruebe que funcione:
```bash
$ sudo apt install docker-cesudo systemctl status docker
```
El resultado debe ser similar al siguiente, y mostrar que el servicio está activo y en ejecución:
<p align="center">
  <img src="https://github.com/davyyelor/VeganMania/blob/master/statusDocker.png" height=300>
</p>

#### Instalación Chrome

Primero actualizamos el sistema:
```bash
$ sudo apt-get update
```

Descargamos el paquete para la instalación de chrome:
```bash
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
```

Instalamos el paquete:
```bash
$ sudo apt install ./google-chrome-stable_current_amd64.deb
```

### Instrucciones de Uso 

Abra una terminal, la normal en Linux y en Windows La de Visual Studio que aparece arriba a la derecha.

Para obtener los archivos del directorio del proyecto se ha de emplear el siguiente comando:
```bash
$git clone https://github.com/davyyelor/VeganMania
```

Tras esto, desplegamos los servicios mediante:
```bash
$ docker-compose up
```

O pruebe si no funciona con:
```bash
$ docker compose up
```

Una vez hecho esto la página web estará corriendo en el [puerto 80](http://localhost).
Una vez dentro y que funcione correctamente tendrá acceso a todas las funcionalidades para cuidar su alimentación vegana/vegetariana.




