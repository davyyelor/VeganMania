DROP DATABASE IF EXISTS usuarios;
CREATE DATABASE IF NOT EXISTS usuarios;
USE usuarios;


CREATE TABLE IF NOT EXISTS clientes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  usuario VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  contrasena VARCHAR(255) NOT NULL,
  fechaNacimiento DATE NOT NULL,
  peso DECIMAL(5,2) NOT NULL,
  altura DECIMAL(5,2) NOT NULL,
  genero VARCHAR(10) NOT NULL,
  actividad VARCHAR(255) NOT NULL,
  calorias_objetivo DECIMAL(8,2) NOT NULL DEFAULT 0
);


CREATE TABLE IF NOT EXISTS registro_calorias_diario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  cliente_id INT NOT NULL,
  calorias_consumidas DECIMAL(8,2) NOT NULL DEFAULT 0,
  fecha_consumo DATE NOT NULL,
  FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);


INSERT INTO clientes
  (nombre, usuario, email, contrasena, fechaNacimiento, peso, altura, genero, actividad)
VALUES
  ('Kepa', 'kepab', 'kepa@example.com', '0ffe1abd1a08215353c233d6e009613e95eec4253832a761af28ff37ac5a150c', '1990-01-01', 70.5, 180.0, 'Hombre', 'Sedentario'),
  ('Ander', 'andere', 'ander@example.com', '0ffe1abd1a08215353c233d6e009613e95eec4253832a761af28ff37ac5a150c', '1995-05-05', 65.2, 175.0, 'Hombre', 'Sedentario');



INSERT INTO registro_calorias_diario (cliente_id, calorias_consumidas, fecha_consumo)
SELECT id, 0, CURDATE() FROM clientes WHERE nombre IN ('Kepa', 'Ander');



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