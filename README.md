# Proyecto VeganMania
Una aplicación Python Flask + MySQL 5.7 + Nginx en Docker Compose.

***Documentación básica de la app***

David Elorza

## Tabla de contenido
- [Requisitos Windows](#requisitos-windows).
- [Requisitos Linux](#requisitos-linux).
- [Contribuir](#contribuir).


### Requisitos Windows
- IDE para ejecutar todo el programa, se ha usado VS Code
- Docker Desktop para poder administrar los contenedores e imágenes creados y utilizados.

Para descargar ambas buscar en Internet y descargar la versión más reciente:
- Link VSCode: https://code.visualstudio.com/download
- Link Docker Desktop: https://docs.docker.com/desktop/install/windows-install/

## Instrucciones específicas para Linux
#### Requisitos (opcionales, es una forma de hacerlo)
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


### Requisitos Linux

