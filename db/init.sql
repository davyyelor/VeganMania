DROP DATABASE IF EXISTS usuarios;
CREATE DATABASE IF NOT EXISTS usuarios;
USE usuarios;

-- Tabla Cliente
CREATE TABLE IF NOT EXISTS Cliente (
  id_cliente INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) NOT NULL,
  nombre_usu VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  contrasena VARCHAR(255) NOT NULL,
  peso DECIMAL(5,2) NOT NULL,
  altura DECIMAL(5,2) NOT NULL,
  genero VARCHAR(10) NOT NULL,
  actividad VARCHAR(255) NOT NULL,
  fecha_nacimiento DATE NOT NULL
);

-- Tabla Alimento
CREATE TABLE IF NOT EXISTS Alimento (
  id_alimento INT AUTO_INCREMENT PRIMARY KEY,
  nombreAlimento VARCHAR(255) NOT NULL,
  descripcion TEXT NOT NULL
);

-- Tabla Comida
CREATE TABLE IF NOT EXISTS Comida (
  id_comida INT AUTO_INCREMENT PRIMARY KEY,
  id_cliente INT,
  nombreComida VARCHAR(255) NOT NULL,
  tipoComida VARCHAR(255) NOT NULL,
  descripcion TEXT NOT NULL,
  fecha DATE NOT NULL,
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
);

-- Tabla Nutriente
CREATE TABLE IF NOT EXISTS Nutriente (
  id_nutriente INT AUTO_INCREMENT PRIMARY KEY,
  nombreNutriente VARCHAR(255) NOT NULL,
  descripcion TEXT NOT NULL,
  unidad VARCHAR(50) NOT NULL,
  categoria VARCHAR(50) NOT NULL
);

-- Tabla tiene_alergia
CREATE TABLE IF NOT EXISTS tiene_alergia (
  id_cliente INT,
  id_alimento INT,
  gravedad VARCHAR(50) NOT NULL,
  sintomas TEXT NOT NULL,
  PRIMARY KEY (id_cliente, id_alimento),
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
  FOREIGN KEY (id_alimento) REFERENCES Alimento(id_alimento)
);

-- Tabla incluye
CREATE TABLE IF NOT EXISTS incluye (
  id_comida INT,
  id_alimento INT,
  unidad VARCHAR(50) NOT NULL,
  cantidad DECIMAL(8,2) NOT NULL,
  PRIMARY KEY (id_comida, id_alimento),
  FOREIGN KEY (id_comida) REFERENCES Comida(id_comida),
  FOREIGN KEY (id_alimento) REFERENCES Alimento(id_alimento)
);

-- Tabla contiene
CREATE TABLE IF NOT EXISTS contiene (
  id_alimento INT,
  id_nutriente INT,
  cantidad DECIMAL(8,2) NOT NULL,
  PRIMARY KEY (id_alimento, id_nutriente),
  FOREIGN KEY (id_alimento) REFERENCES Alimento(id_alimento),
  FOREIGN KEY (id_nutriente) REFERENCES Nutriente(id_nutriente)
);

-- Tabla consume
CREATE TABLE IF NOT EXISTS consume (
  id_cliente INT,
  id_nutriente INT,
  fecha_consumo DATE NOT NULL,
  cantidad DECIMAL(8,2) NOT NULL,
  PRIMARY KEY (id_cliente, id_nutriente, fecha_consumo),
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
  FOREIGN KEY (id_nutriente) REFERENCES Nutriente(id_nutriente)
);

-- Tabla tiene_objetivo
CREATE TABLE IF NOT EXISTS tiene_objetivo (
  id_cliente INT,
  id_nutriente INT,
  cantidad DECIMAL(8,2) NOT NULL,
  PRIMARY KEY (id_cliente, id_nutriente),
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
  FOREIGN KEY (id_nutriente) REFERENCES Nutriente(id_nutriente)
);

-- Insertar datos de ejemplo en Cliente
INSERT INTO Cliente (nombre, nombre_usu, email, contrasena, peso, altura, genero, actividad, fecha_nacimiento)
VALUES
  ('Kepa', 'kepab', 'kepa@example.com', '0ffe1abd1a08215353c233d6e009613e95eec4253832a761af28ff37ac5a150c', 70.5, 180.0, 'Hombre', 'Sedentario', '1990-05-15'),
  ('Ander', 'andere', 'ander@example.com', '0ffe1abd1a08215353c233d6e009613e95eec4253832a761af28ff37ac5a150c', 65.2, 175.0, 'Hombre', 'Sedentario', '1988-08-20');

-- Insertar nutrientes con categorías
INSERT INTO Nutriente (nombreNutriente, descripcion, unidad, categoria) VALUES
('Energia', 'Cantidad de energia proporcionada por el alimento', 'kcal', 'Energia'),
('Lipidos totales (grasas)', 'Grasas totales presentes en el alimento', 'g', 'Grasas'),
('Acidos grasos, saturados totales', 'Grasas saturadas presentes en el alimento', 'g', 'Grasas'),
('Acidos grasos, trans totales', 'Grasas trans presentes en el alimento', 'g', 'Grasas'),
('Acidos grasos monoinsaturados totales', 'Grasas monoinsaturadas presentes en el alimento', 'g', 'Grasas'),
('Acidos grasos poliinsaturados totales', 'Grasas poliinsaturadas presentes en el alimento', 'g', 'Grasas'),
('Carbohidratos, por diferencia', 'Carbohidratos presentes en el alimento', 'g', 'Carbohidratos'),
('Fibra dietetica total', 'Fibra dietetica presente en el alimento', 'g', 'Carbohidratos'),
('Azucares, total incluyendo NLEA', 'Azucares totales presentes en el alimento', 'g', 'Carbohidratos'),
('Proteina', 'Proteina presente en el alimento', 'g', 'Proteinas'),
('Colesterol', 'Colesterol presente en el alimento', 'mg', 'Minerales'),
('Sodio Na', 'Sodio presente en el alimento', 'mg', 'Minerales'),
('Calcio', 'Calcio presente en el alimento', 'mg', 'Minerales'),
('Magnesio, Mg', 'Magnesio presente en el alimento', 'mg', 'Minerales'),
('Potasio, K', 'Potasio presente en el alimento', 'mg', 'Minerales'),
('Hierro, Fe', 'Hierro presente en el alimento', 'mg', 'Minerales'),
('Zinc, Zn', 'Zinc presente en el alimento', 'mg', 'Minerales'),
('Fosforo, P', 'Fosforo presente en el alimento', 'mg', 'Minerales'),
('Vitamina A, RAE', 'Vitamina A presente en el alimento', 'mcg', 'Vitaminas'),
('Vitamina C, acido ascorbico total', 'Vitamina C presente en el alimento', 'mg', 'Vitaminas'),
('Tiamina', 'Tiamina presente en el alimento', 'mg', 'Vitaminas'),
('Riboflavina', 'Riboflavina presente en el alimento', 'mg', 'Vitaminas'),
('Niacina', 'Niacina presente en el alimento', 'mg', 'Vitaminas'),
('Vitamina B-6', 'Vitamina B-6 presente en el alimento', 'mg', 'Vitaminas'),
('Folato, DFE', 'Folato presente en el alimento', 'mcg', 'Vitaminas'),
('Folato, comida', 'Folato de origen alimentario presente en el alimento', 'mcg', 'Vitaminas'),
('Acido folico', 'Acido folico presente en el alimento', 'mcg', 'Vitaminas'),
('Vitamina B12', 'Vitamina B12 presente en el alimento', 'mcg', 'Vitaminas'),
('Vitamina D (D2 + D3)', 'Vitamina D presente en el alimento', 'mcg', 'Vitaminas'),
('Vitamina E (alfa-tocoferol)', 'Vitamina E presente en el alimento', 'mg', 'Vitaminas'),
('Vitamina K (filoquinona)', 'Vitamina K presente en el alimento', 'mcg', 'Vitaminas'),
('Agua', 'Contenido de agua en el alimento', 'g', 'Otros');

-- Establecer un objetivo de 2000 para todos los nutrientes para cada cliente
INSERT INTO tiene_objetivo (id_cliente, id_nutriente, cantidad)
SELECT c.id_cliente, n.id_nutriente, 2000
FROM Cliente c, Nutriente n;

INSERT INTO consume (id_cliente, id_nutriente, fecha_consumo, cantidad)
SELECT c.id_cliente, n.id_nutriente, CURDATE(), 0
FROM Cliente c, Nutriente n
ON DUPLICATE KEY UPDATE cantidad = 0;

