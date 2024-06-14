DROP DATABASE IF EXISTS usuarios;
CREATE DATABASE IF NOT EXISTS usuarios CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE usuarios;


-- Tabla Cliente
CREATE TABLE IF NOT EXISTS Cliente (
  id_cliente INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  nombre_usu VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  email VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  contrasena VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  peso DECIMAL(5,2) NOT NULL,
  altura DECIMAL(5,2) NOT NULL,
  genero VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  actividad VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  fecha_nacimiento DATE NOT NULL,
  email_verificado BOOLEAN NOT NULL DEFAULT FALSE,
  UNIQUE (email)
);

-- Tabla PasswordReset
CREATE TABLE IF NOT EXISTS PasswordReset (
  id INT AUTO_INCREMENT PRIMARY KEY,
  id_cliente INT NOT NULL,
  token VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  expiration DATETIME NOT NULL,
  requested_at DATETIME NOT NULL,
  used BOOLEAN NOT NULL DEFAULT FALSE,
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente) ON DELETE CASCADE
);

-- Tabla PasswordHistory
CREATE TABLE IF NOT EXISTS PasswordHistory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    hashed_password VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    change_date DATETIME NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente) ON DELETE CASCADE
);

-- Tabla Alimento
CREATE TABLE IF NOT EXISTS Alimento (
  id_alimento INT AUTO_INCREMENT PRIMARY KEY,
  nombreAlimento VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  descripcion TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
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
  ('Ander', 'andere', 'ander@example.com', '0ffe1abd1a08215353c233d6e009613e95eec4253832a761af28ff37ac5a150c', 65.2, 175.0, 'Hombre', 'Sedentario', '1988-08-20'),
  ('David', 'davidd', 'davy.elorza@gmail.com', '0ffe1abd1a08215353c233d6e009613e95eec4253832a761af28ff37ac5a150c', 65.2, 175.0, 'Hombre', 'Sedentario', '1988-08-20');

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

CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Producto TEXT,
    EnTemporada TEXT,
    InicioTemporada TEXT,
    FueraDeTemporada TEXT,
    Descripcion TEXT 
);

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('acelga', 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, JUNIO, JULIO, SEPTIEMBRE, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'AGOSTO', NULL, 'Se puede encontrar acelgas de varios colores (rosas, amarillas, blancas...) dependiendo de su variedad. La acelga se adapta bien a cualquier clima, por lo tanto se recolecta durante casi todo el año.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('aguacate', 'ENERO, FEBRERO, MARZO, ABRIL, NOVIEMBRE, DICIEMBRE', 'MAYO, OCTUBRE', 'JUNIO, JULIO, AGOSTO, SEPTIEMBRE', 'Es un fruto tropical que requiere temperaturas muy cálidas, por lo cual se cultiva muy poco en la península. Pequeño truco para saber su punto de madurez: quitarle el botón superior y mirar el color del fruto. Si es verde, aún será duro. Si es marron, está pasado. Si es amarillo, ¡está perfecto!');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('ajo', 'JUNIO, JULIO', 'MAYO', 'ENERO, FEBRERO, MARZO, ABRIL, AGOSTO, SEPTIEMBRE, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'El ajo se recolecta en primavera y se almacena para poder consumirlo todo el año. En buenas condiciones, se puede conservar durante mucho tiempo. Aunque su olor fuerte pueda molestar a algunos, tiene un montón de beneficios para la salud y es un antibiotico natural.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('albaricoque', 'MAYO, JUNIO, JULIO', 'AGOSTO', 'ENERO, FEBRERO, MARZO, ABRIL, SEPTIEMBRE, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'El albaricoquero da frutos a finales de primavera y durante todo el verano. El albaricoque no soporta larga conservación porque sigue madurando una vez cosechado (se dice de estos frutos que son climatéricos). Cuando viene de lejos, puedes estar seguro que habrá sido recolectado antes de estar maduro.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('alcachofa', 'ABRIL, MAYO', 'MARZO, JUNIO, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'ENERO, FEBRERO, JULIO, AGOSTO, SEPTIEMBRE', 'La alcachofa tiene dos temporadas ideales, una en otoño y otra en primavera, dependiendo del clima de la zona donde se produce. La planta puede vivir varios años y alcanzar hasta los 2 metros de altura, y es en su punta donde nacen las alcachofas.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('apio', 'ENERO, FEBRERO, MARZO, ABRIL, DICIEMBRE', 'MAYO, JUNIO, JULIO, AGOSTO, SEPTIEMBRE, OCTUBRE, NOVIEMBRE', NULL, 'El apio tiene la curiosidad de quitar más calorias de las que aporta cuande se come');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('batata', 'OCTUBRE, NOVIEMBRE', NULL, 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, JUNIO, JULIO, AGOSTO, SEPTIEMBRE, DICIEMBRE', 'Las mejores temporadas para consumir la batata (o boniato) son otoño e invierno. Es un tubérculo dulce que se puede usar en platos o postres (se recomiendan los buñuelos de boniato). La demanda de este producto ha ido aumentando estos últimos años, incitando cada vez más agricultores a producirla.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('berenjena', 'JULIO, AGOSTO, SEPTIEMBRE', 'OCTUBRE', 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, JUNIO, NOVIEMBRE, DICIEMBRE', 'Necesita muchas horas de sol y temperaturas elevadas para crecer, por eso se encuentra principalmente en verano. Las berenjenas que compras en pleno invierno vendrán con mucha probabilidad de invernaderos climatizados o de países lejanos.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('brocoli', 'OCTUBRE, NOVIEMBRE, DICIEMBRE', 'ENERO, FEBRERO, MAYO, JUNIO', 'MARZO, ABRIL, JULIO, AGOSTO, SEPTIEMBRE', 'El brócoli o brécol pertenece a la familia de las coles, y como todos los coles, prefiere las temporadas templadas y frías. Se disfruta en otoño e invierno.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('calabacin', 'JUNIO, JULIO, AGOSTO', 'SEPTIEMBRE', 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'La temporada perfecta para consumir calabacín es el verano porque necesita climas calurosos para crecer. Las flores de la planta también son comestibles y tienen un sabor muy delicado.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('calabaza', 'SEPTIEMBRE, OCTUBRE', 'JULIO, AGOSTO', 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, JUNIO, NOVIEMBRE, DICIEMBRE', 'Aunque sea el producto más grande del huerto, la calabaza es muy sensible a las temporadas frías. Su mejor temporada es el verano y el inició de otoño. La calabaza más grande de España fue cultivada en 2016, ¡pesaba más de 600 kilos!');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('caqui', 'DICIEMBRE', 'OCTUBRE, NOVIEMBRE', 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, JUNIO, JULIO, AGOSTO, SEPTIEMBRE', 'La temporada del caquí, o persimón, se inicia en otoño. En algunos lugares, esta fruta se llama “palosanto” simplemente porque los caquis suelen madurar en noviembre y están disponibles en la festividad de “Todos los Santos”.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('cardo', 'ENERO, NOVIEMBRE, DICIEMBRE', 'FEBRERO, MARZO', 'ABRIL, MAYO, JUNIO, JULIO, AGOSTO, SEPTIEMBRE, OCTUBRE', 'El cardo es un producto de invierno típico de la gastronomía del norte de España. Se consumía mucho en el pasado y está volviendo a ser de moda por sus calidades nutritivas.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('cebolla', 'AGOSTO, SEPTIEMBRE, OCTUBRE', 'MARZO, ABRIL, MAYO, JUNIO, JULIO, NOVIEMBRE, DICIEMBRE', 'ENERO, FEBRERO', 'La cebolla se encuentra durante la mayor parte del año porque se almacena y se conserva bien, como el ajo. Recordamos al famoso Shrek y su expresión sobre este producto indispensable en la cocina.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('cereza', 'MAYO, JUNIO', NULL, 'ENERO, FEBRERO, MARZO, ABRIL, JULIO, AGOSTO, SEPTIEMBRE, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'La cereza, o picota, llega con el calor y tiene una temporada bastante corta, entre mayo y julio. Las cerezas del Jerte son muy populares en el mundo entero por su sabor y calidad.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('col', 'OCTUBRE, NOVIEMBRE, DICIEMBRE', 'ENERO, FEBRERO, SEPTIEMBRE', 'MARZO, ABRIL, MAYO, JUNIO, JULIO, AGOSTO', 'Las coles se disfrutan en otoño e invierno. Aunque esté volviendo a ser de moda, este producto típico de la cultura culinaria de muchos países europeos fue despreciado por los franceses durante años.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('coliflor', 'NOVIEMBRE, DICIEMBRE', 'ENERO, FEBRERO, MARZO, ABRIL, SEPTIEMBRE, OCTUBRE', 'MAYO, JUNIO, JULIO, AGOSTO', 'Su temporada perfecta es el otoño y el invierno. Se puede usar tanto en gratinados como en purés, y es deliciosa en sopa. Dato curioso: en algunos países, es muy popular como sustituto de los granos y se utiliza para hacer masa de pizza.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('col de bruselas', 'NOVIEMBRE, DICIEMBRE', 'ENERO, FEBRERO, MARZO, ABRIL, SEPTIEMBRE, OCTUBRE', 'MAYO, JUNIO, JULIO, AGOSTO', 'Esta variedad de col es perfecta para consumir en otoño e invierno. Se le llama así por su origen: empezó a cultivarse de manera más intensa en Bélgica en el siglo XIX.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('esparrago', 'MARZO, ABRIL', 'FEBRERO, MAYO', 'ENERO, JUNIO, JULIO, AGOSTO, SEPTIEMBRE, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'La temporada ideal del espárrago es la primavera, entre marzo y abril. El espárrago verde y el espárrago blanco pertenecen a la misma planta, lo que los diferencia es su cultivo. Mientras que el primero crece al sol, el segundo lo hace en la tierra, y así mantiene su color blanco.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('espinaca', 'ENERO, FEBRERO, MARZO, ABRIL, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'MAYO, JUNIO, SEPTIEMBRE', 'JULIO, AGOSTO', 'Las espinacas son conocidas por su alto contenido en hierro, aunque en realidad no tienen tanto como se pensaba. Se encuentran principalmente en invierno, pero se pueden consumir todo el año. Muy versátiles en la cocina, se pueden usar crudas en ensaladas o cocidas en diferentes platos.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('fresa', 'MARZO, ABRIL, MAYO', 'FEBRERO, JUNIO', 'ENERO, JULIO, AGOSTO, SEPTIEMBRE, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'La fresa es una fruta muy apreciada que se encuentra principalmente en primavera. Existen muchas variedades de fresas, cada una con su sabor particular. Las fresas de Huelva son muy conocidas en España por su calidad y dulzura.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('frambuesa', 'JUNIO, JULIO, AGOSTO', 'MAYO, SEPTIEMBRE', 'ENERO, FEBRERO, MARZO, ABRIL, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'Las frambuesas son bayas que se disfrutan principalmente en verano. Tienen un sabor dulce y ácido a la vez, y son muy utilizadas en postres y mermeladas.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('granada', 'OCTUBRE, NOVIEMBRE, DICIEMBRE', 'ENERO', 'FEBRERO, MARZO, ABRIL, MAYO, JUNIO, JULIO, AGOSTO, SEPTIEMBRE', 'La granada es una fruta otoñal que se puede encontrar hasta el inicio del invierno. Sus granos rojos y jugosos son muy apreciados tanto en platos salados como en postres. Es conocida por sus propiedades antioxidantes.');

INSERT INTO productos (Producto, EnTemporada, InicioTemporada, FueraDeTemporada, Descripcion)
VALUES ('guisante', 'ABRIL, MAYO', 'MARZO, JUNIO', 'ENERO, FEBRERO, JULIO, AGOSTO, SEPTIEMBRE, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'Aunque comunmente se consideran verduras, los guisantes pertenecen a la familia de las leguminosas. Los meses de primavera son los más indicados para consumir sus dulces granos que, al ser tan tiernos, a diferencia de otras legumbres, se pueden comer crudos.'),
('haba', 'MAYO', 'ABRIL', 'ENERO, FEBRERO, MARZO, JUNIO, JULIO, AGOSTO, SEPTIEMBRE, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'El mejor momento para consumir esta "fruta-legumbre" es durante la primavera. Las habas frescas tienen una temporalidad muy corta, y pueden aguantar en el frigorífico unos cuatro días. Es un producto muy recomendable por sus numerosas propiedades nutricionales'),
('higo', 'AGOSTO, SEPTIEMBRE', 'JULIO', 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, JUNIO, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'Es un fruto mediterráneo que tiene una temporada muy corta'),
('judia', 'JUNIO, JULIO, AGOSTO, SEPTIEMBRE', 'MAYO, OCTUBRE', 'ENERO, FEBRERO, MARZO, ABRIL, NOVIEMBRE, DICIEMBRE', 'La judía está en el TOP 10 de los productos más importados en 2015. El mejor momento para consumirlas es durante los meses de primavera y verano. Las judías frescas presentan un color verde vivo y brillante, y deben tener un aspecto regular y no ser muy duras al tacto. Otros trucos para adivinar la terneza y calidad del producto es que sus granos no deben aparecer muy marcados, y si aparece una gotita de agua al quebrarse.'),
('kiwi', 'ENERO, FEBRERO, MARZO, OCTUBRE, NOVIEMBRE, DICIEMBRE', NULL, 'ABRIL, MAYO, JUNIO, JULIO, AGOSTO, SEPTIEMBRE', 'El kiwi está en el TOP 10 de los productos más importados en 2015 y la mayoría viene de Nueva Zelanda. Un viaje de unos 20,000 km para llegar a tu nevera. Esta fruta madura en invierno y puede consumirse de octubre a marzo. Si se conserva a una temperatura ambiente, sin deshidratarse, puede aguantar hasta 15 días. Entre sus múltiples propiedades nutritivas, destacan su aporte de vitamina C (más del doble que la naranja) y su aporte de fibra, favoreciendo así el tránsito intestinal.'),
('lechuga', 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, JUNIO, JULIO, AGOSTO, SEPTIEMBRE, OCTUBRE, NOVIEMBRE', 'DICIEMBRE', NULL, 'Se puede disfrutar de la lechuga todo el año, y se cultiva en todos los climas. Los cuatro tipos de lechuga verde son muy beneficiosos para la salud, ya que son unas verduras que aportan importantes dosis de vitaminas, antioxidantes y nutrientes aunque, entre las cuatro, destaca la lechuga romana. A la hora de escoger este producto, hay que fijarse en que las hojas, cuanto más oscuras, más nutritivas son.'),
('lima', 'NOVIEMBRE', 'AGOSTO, SEPTIEMBRE, OCTUBRE, DICIEMBRE', 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, JUNIO, JULIO', 'Las limas son más delicadas que los limones, por lo que hay que manipularlas con cuidado. Como sus hermanos, destacan por su aportación de vitamina C, sus propiedades antioxidantes y de acción astringente. Se suele utilizar su jugo como alternativa al vinagre, y también para preparar bebidas refrescantes u otros productos como mermeladas.'),
('limon', 'ENERO, FEBRERO, MARZO, NOVIEMBRE, DICIEMBRE', 'ABRIL, MAYO, JUNIO, OCTUBRE', 'JULIO, AGOSTO, SEPTIEMBRE', 'El limón puede encontrarse desde los meses de otoño hasta ya entrado el verano. Aunque a veces pueda tener pequeñas manchitas marrones en su cáscara, estas no afectan a su sabor, pero sí se deben descartar aquellos que parezcan deshidratados o blandos. Es una fruta muy rica en vitamina C y por sus propiedades antioxidantes y ácido cítrico, idóneo para estimular el sistema inmunitario y las defensas contra virus y bacterias. Un truco para guardar el limón y evitar que se reseque es tapar la mitad con la otra que hayamos cortado, uniéndolas con un palillo.'),
('maiz', 'SEPTIEMBRE', 'AGOSTO, OCTUBRE', 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, JUNIO, JULIO, NOVIEMBRE, DICIEMBRE', 'Aunque estemos acostumbrados a una sola variedad de maíz, existen al menos 300 variedades conocidas de este producto. El maíz dulce destaca por las altas cantidades de hidratos de carbono que contiene y, también, por su aporte de algunos minerales como el magnesio, el fósforo y el potasio. Puede ser un alimento muy recomendable para las personas que tienen celiaquía, ya que el maíz dulce no contiene gluten.'),
('mandarina', 'NOVIEMBRE', 'ENERO, FEBRERO, MARZO, DICIEMBRE', 'ABRIL, MAYO, JUNIO, JULIO, AGOSTO, SEPTIEMBRE, OCTUBRE', 'Se pueden encontrar mandarinas de plena temporada desde comienzos de otoño hasta el mes de marzo. Para elegir las piezas más jugosas se debe tener en cuenta su peso respecto a su tamaño, y la mejor señal de calidad no es tanto el aspecto de su cáscara como su olor, más intenso cuanto más madura está la fruta. Aunque aporta menos cantidad de vitamina C que otros cítricos, es una excelente fuente de esta sustancia, que favorece la formación de anticuerpos y estimula la acción antiinfecciosa.'),
('manzana', 'SEPTIEMBRE', 'JULIO, AGOSTO, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, JUNIO', 'La manzana es una de las frutas más famosas y antiguas de la historia, y se dice que los seres humanos ya la cultivaban y difundían antes del Paleolítico. Esta fruta es una de las más completas desde una perspectiva nutritiva por sus extraordinarias propiedades, e incluso un grupo de científicos de la Universidad china de Hong Kong han llegado a afirmar que alarga la vida. Un truco para saber si la manzana está en su punto óptimo de madurez es comprobar si, al cogerla por el medio, su carne se mantiene firme o su piel se arruga muy poco. Por el contrario, una muestra de que la fruta no se encuentra en buen estado es si aparecen con muchas arrugas, puntos blandos o manchas, aunque las pequeñas motitas que tienen algunas variedades no afectan en absoluto a su calidad.'),
('melocoton', 'JULIO, AGOSTO, SEPTIEMBRE', 'JUNIO', 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'Actualmente, el melocotón es una de las frutas más difundidas del mundo. Sus aportes de nutrientes son muy moderados, por lo que es una fruta idónea para el consumo general. Aunque no destaca por aportar grandes cantidades de ninguna vitamina en concreto, el melocotón confiere a nuestro organismo importantes dosis de fibra y potasio. Una señal de que se encuentra en un grado óptimo de maduración es cuando la última mancha verde torna en un tono amarillo, y si desprende un aroma suave y afrutado.'),
('melon', 'JULIO, AGOSTO, SEPTIEMBRE', NULL, 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, JUNIO, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'El melón es, sin duda, sinónimo de verano. Existen múltiples clases de esta fruta dependiendo de su lugar de procedencia y sus características de cultivo aunque, en el Estado español, la variedad más común es el de piel de sapo, y es uno de los tipos de melones más grandes, con un peso de 2.5 kg de media. El 80% de su composición es agua siendo, por tanto, un hidratante excelente; y su escasa aportación calórica se compensa con las importantes dosis de minerales y vitaminas que lo convierten en un complemento muy recomendable en la dieta diaria.'),
('mora', 'JULIO, AGOSTO, SEPTIEMBRE', 'JUNIO', 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'Resulta muy curioso que llamamos mora a dos bayas que vienen de dos especies vegetales totalmente distintas. Por un lado tenemos moras de moredas, árboles, y por otro las moras de zarzamora, arbustos. Estas deliciosas frutas se pueden recolectar en verano, sobre todo en la parte final cuando alcanzan un color negro brillante indicando un punto óptimo de madurez. Son muy codiciadas para postres, tartas y mermeladas.'),
('nabo', 'NOVIEMBRE, DICIEMBRE', 'SEPTIEMBRE, OCTUBRE', 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, JUNIO, JULIO, AGOSTO', 'El nabo es un tubérculo de climas templados y fríos, se cultiva en Europa desde hace milenios. Era alimento de consumo diario hasta que llegó la patata desde América. Hoy en día, se cultiva en todo el mundo para alimentar al ganado, por su alta producción, facilidad de cultivo y porque produce cuando no hay pasto disponible. Se puede cocinar en guisos, purés, o incluso fritos como chips. Hay incluso algunas recetas utilizando sus ricas hojas.'),
('naranja', 'ENERO, FEBRERO, MARZO, ABRIL, NOVIEMBRE, DICIEMBRE', 'MAYO', 'JUNIO, JULIO, AGOSTO, SEPTIEMBRE, OCTUBRE', 'Las mejores estaciones para consumir las naranjas son otoño e invierno. Se aprecia en la textura y sobre todo en la frescura y sabor cuando una naranja está fuera de temporada, o peor, ha sido congelada. La naranja es uno de los productos que España más exporta y a la vez más importa. Muy arraigada a nuestra cultura, todo un icono del levante y de los palacios andaluces, y que podemos encontrar en una gran variedad de platos dulces o salados. ¿Has probado el remojón con bacalao?'),
('nectarina', 'JULIO, AGOSTO', 'MAYO, JUNIO, SEPTIEMBRE', 'ENERO, FEBRERO, MARZO, ABRIL, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'La nectarina es una variante de melocotón sin vello ni pelusa, y no una hibridación entre melocotón y ciruela como mucha gente piensa. Se cultiva desde hace siglos, pero no es hasta recientemente cuando su interés ha favorecido incrementos de producción local. Se puede consumir además de cruda, en multitud de postres, como bizcochos, mermeladas, macedonias de frutas, o tartas. España es un gran exportador de nectarinas a nuestros vecinos europeos.'),
('patata', 'JUNIO, JULIO, AGOSTO', 'MAYO, SEPTIEMBRE, OCTUBRE', 'ENERO, FEBRERO, MARZO, ABRIL, NOVIEMBRE, DICIEMBRE', 'Se pueden encontrar patatas en prácticamente todo el mundo, pues es uno de los alimentos básicos del ser humano, ayudando a combatir el hambre a lo largo de nuestra historia. Su cultivo es milenario, con origen en América del Sur, fue introducida en Europa por los primeros colonos españoles en el siglo XVI y ahí se expandió a todas las colonias y resto de países. En 2015, fue el producto que más se importó, principalmente desde China, que es el mayor productor del mundo según FAO muy por delante de India y Rusia.'),
('pepino', 'JUNIO, JULIO, AGOSTO, SEPTIEMBRE', NULL, 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'El pepino es una hortaliza típica del verano, cuando los huertos producen a pleno rendimiento, gracias al calor y buen riego. Originaria de India, es una hortaliza típica de la dieta mediterránea. Se consume crudo o encurtido, y está presente en ensaladas, gazpachos, sopas frías y demás platos de verano por su elevada composición en agua. Muy rico y nutritivo para combatir el calor!'),
('pera', 'JULIO, AGOSTO, SEPTIEMBRE', 'OCTUBRE', 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, JUNIO, NOVIEMBRE, DICIEMBRE', 'La pera es uno de los frutos más importantes que se cultivan en regiones templadas. Es curioso pues podemos encontrar peras de invierno o verano según su requerimiento de frío para madurar. Por ello podemos encontrar diferentes variedades de pera según la época del año. Las peras de invierno se conservan mucho mejor que sus primas de verano. Podemos encontrarlas en muchos platos típicos europeos, tanto en postres, mermeladas como en compotas.'),
('pimiento', 'JUNIO, JULIO, AGOSTO, SEPTIEMBRE', 'OCTUBRE', 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, NOVIEMBRE, DICIEMBRE', 'El pimiento es una hortaliza que se presenta en innumerables formas, tamaños, colores y sabores. Aunque China es el mayor productor del mundo, esta hortaliza proviene de Centroamérica. En España, la mayor parte de la producción industrial de pimientos se obtiene en invernaderos por las necesidades de luz, humedad y temperatura. Es por ello que, además de ser España uno de los principales exportadores de Europa, es fácil encontrarlos en cualquier momento del año aunque su temporada natural es el verano.'),
('platano', NULL, NULL, 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, JUNIO, JULIO, AGOSTO, SEPTIEMBRE, OCTUBRE, NOVIEMBRE, DICIEMBRE', '99,9% de los plátanos españoles se cultivan en Canarias y se recogen todo el año. Este proyecto parte de la idea que consumir responsable significa comer de temporada pero también comer local. En la península podemos encontrarlo únicamente en algunas plantaciones de la costa granadina. Es una fruta climatérica, lo que significa que sigue madurando después de haber sido recogida. Se suele recolectar antes de su punto de madurez para que no llegue estropeada al lugar de comercialización.'),
('pomelo', 'DICIEMBRE', 'ENERO, FEBRERO, MARZO, ABRIL', 'MAYO, JUNIO, JULIO, AGOSTO, SEPTIEMBRE, OCTUBRE, NOVIEMBRE', 'El pomelo que consumimos en Europa es un híbrido de los cítricos cultivados desde hace milenios en China y sudeste asiático. Al igual que otros cítricos la mejor época para su consumo es otoño e invierno. En España su consumo es menos habitual que en otros países vecinos, y en lo últimos años se está incrementando notablemenete la producción de pomelos, principalmente en la costa mediterránea y Andalucía. Los principales usos son crudos, en mermeladas o postre.'),
('puerro', 'ENERO, FEBRERO, SEPTIEMBRE, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'MARZO, AGOSTO', 'ABRIL, MAYO, JUNIO, JULIO', 'El puerro es un primo de la cebolla y el ajo. Se cultiva principalmente por su bulbo, aunque también son comestibles las hojas. Se puede comer crudo en ensaladas, cocido en sopas o ricas cremas de puerro.'),
('rabano', 'OCTUBRE, NOVIEMBRE', 'MARZO, MAYO, JUNIO, JULIO, SEPTIEMBRE', 'ENERO, FEBRERO, ABRIL, AGOSTO, DICIEMBRE', 'El rábano es una planta cultivada en casi todo el mundo por sus exquisitas raíces. Principalmente al principio del verano, aunque está muy extendido su cultivo en invernaderos. En algunos países orientales como Japón, el rábano es uno de los ingredientes principales de sus platos típicos. ¿Sabías que el wasabi se obtiene de un rábano picante?'),
('remolacha', 'JULIO, AGOSTO, OCTUBRE, NOVIEMBRE', 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, JUNIO, SEPTIEMBRE, DICIEMBRE', NULL, 'La remolacha es un cultivo típico mediterráneo que se consume habitualmente cocida, en ensaladas, hummus, tartas, o albóndigas. Existen varios tipos destacando sobre todo la variante azucarera, distinta a la remolacha morada de consumo doméstico, por la importancia histórica que ha tenido la obtención industrial de azúcar, sobre todo para la industria andaluza.'),
('sandia', 'JUNIO, JULIO, AGOSTO', 'SEPTIEMBRE', 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'La sandía es una fruta típica de verano. Florece en Mayo-Junio y madura unos 40 días después, que es cuando podemos coger nuestra sandía. Es uno de los productos más exportados por España, principalmente a nuestros vecinos europeos Alemania, Francia y Países bajos. Al mismo tiempo, es un producto que también importamos, sobre todo de Marruecos y Senegal.'),
('tomate', 'JULIO, AGOSTO, SEPTIEMBRE', 'JUNIO, OCTUBRE', 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, NOVIEMBRE, DICIEMBRE', 'El tomate se encuentra todo el año en la península, pero su temporada natural es el verano. Es uno de los productos con mayor producción en invernadero. Los tomates madurados al sol del verano alcanzan un nivel de sabor y textura imposibles de superar. Además, existen muchas variedades distintas que corren el peligro de desaparecer por centrar la producción unicamente en las que mejor se venden. ¿Has probado los tomates azules?'),
('uva', 'SEPTIEMBRE', 'AGOSTO, OCTUBRE', 'ENERO, FEBRERO, MARZO, ABRIL, MAYO, JUNIO, JULIO, NOVIEMBRE, DICIEMBRE', 'La uva es una fruta excepcional y uno de los alimentos básicos de la dieta mediterránea. Podemos encontrar uvas desde mediados de verano a principios del invierno y España es uno de los principales productores del mundo sólo superado por China a la cabeza, EEUU e Italia. Frescas, pasas o en vino, existen varios miles de variedades distintas, cada una con sus características y usos. ¿Cuántos tipos distintos conoces?'),
('zanahoria', 'ABRIL, MAYO, JUNIO, JULIO, AGOSTO, SEPTIEMBRE, OCTUBRE, NOVIEMBRE, DICIEMBRE', 'ENERO, FEBRERO, MARZO', NULL, 'La zanahoria es un producto que podemos encontrar la mayor parte del año y resulta curioso que aunque su color habitual es el naranja, es posible encontrarlas en otros colores. En China, el principal productor del mundo es habitual encontrarlas blancas o púrpura. Disfrútala cada día cruda, frita, cocida, en tartas, guisos o ensaladas.');

-- Paso 1: Agregar la columna 'imagen' a la tabla 'productos'
ALTER TABLE productos
ADD COLUMN imagen VARCHAR(255);

UPDATE productos
SET imagen = 
    CASE 
        WHEN Producto = 'acelga' THEN 'acelga.jpg'
        WHEN Producto = 'aguacate' THEN 'aguacate.jpg'
        WHEN Producto = 'ajo' THEN 'ajo.jpg'
        WHEN Producto = 'albaricoque' THEN 'albaricoque.jpg'
        WHEN Producto = 'alcachofa' THEN 'alcachofa.jpg'
        WHEN Producto = 'apio' THEN 'apio.jpg'
        WHEN Producto = 'batata' THEN 'batata.jpg'
        WHEN Producto = 'berenjena' THEN 'berenjena.jpg'
        WHEN Producto = 'brocoli' THEN 'brocoli.jpg'
        WHEN Producto = 'calabacin' THEN 'calabacin.jpg'
        WHEN Producto = 'calabaza' THEN 'calabaza.jpg'
        WHEN Producto = 'caqui' THEN 'caqui.jpg'
        WHEN Producto = 'cardo' THEN 'cardo.jpg'
        WHEN Producto = 'cebolla' THEN 'cebolla.jpg'
        WHEN Producto = 'cereza' THEN 'cereza.jpg'
        WHEN Producto = 'champiñon' THEN 'champinon.jpg'
        WHEN Producto = 'col de bruselas' THEN 'col_de_bruselas.jpg'
        WHEN Producto = 'col' THEN 'col.jpg'
        WHEN Producto = 'coliflor' THEN 'coliflor.jpg'
        WHEN Producto = 'endibia' THEN 'endibia.jpg'
        WHEN Producto = 'espinaca' THEN 'espinaca.jpg'
        WHEN Producto = 'esparrago' THEN 'esparrago.jpg'
        WHEN Producto = 'frambuesa' THEN 'frambuesa.jpg'
        WHEN Producto = 'fresa' THEN 'fresa.jpg'
        WHEN Producto = 'granada' THEN 'granada.jpg'
        WHEN Producto = 'guisante' THEN 'guisante.jpg'
        WHEN Producto = 'haba' THEN 'haba.jpg'
        WHEN Producto = 'higo' THEN 'higo.jpg'
        WHEN Producto = 'judia' THEN 'judia.jpg'
        WHEN Producto = 'kiwi' THEN 'kiwi.jpg'
        WHEN Producto = 'lechuga' THEN 'lechuga.jpg'
        WHEN Producto = 'lima' THEN 'lima.jpg'
        WHEN Producto = 'limon' THEN 'limon.jpg'
        WHEN Producto = 'mandarina' THEN 'mandarina.jpg'
        WHEN Producto = 'manzana' THEN 'manzana.jpg'
        WHEN Producto = 'maiz' THEN 'maiz.jpg'
        WHEN Producto = 'melocoton' THEN 'melocoton.jpg'
        WHEN Producto = 'melon' THEN 'melon.jpg'
        WHEN Producto = 'mora' THEN 'mora.jpg'
        WHEN Producto = 'nabo' THEN 'nabo.jpg'
        WHEN Producto = 'naranja' THEN 'naranja.jpg'
        WHEN Producto = 'nectarina' THEN 'nectarina.jpg'
        WHEN Producto = 'patata' THEN 'patata.jpg'
        WHEN Producto = 'pepino' THEN 'pepino.jpg'
        WHEN Producto = 'pera' THEN 'pera.jpg'
        WHEN Producto = 'pimiento' THEN 'pimiento.jpg'
        WHEN Producto = 'platano' THEN 'platano.jpg'
        WHEN Producto = 'pomelo' THEN 'pomelo.jpg'
        WHEN Producto = 'puerro' THEN 'puerro.jpg'
        WHEN Producto = 'remolacha' THEN 'remolacha.jpg'
        WHEN Producto = 'rabano' THEN 'rabano.jpg'
        WHEN Producto = 'sandia' THEN 'sandia.jpg'
        WHEN Producto = 'tomate' THEN 'tomate.jpg'
        WHEN Producto = 'uva' THEN 'uva.jpg'
        WHEN Producto = 'zanahoria' THEN 'zanahoria.jpg'
        ELSE NULL
    END;

-- Crear la tabla recetas
CREATE TABLE recetas (
    Id INT PRIMARY KEY,
    Categoria VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    Nombre VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    Valoracion DECIMAL(3, 2),
    Dificultad VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    Num_comensales INT,
    Tiempo VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    Tipo VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    Link_receta VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    Num_comentarios INT,
    Num_reviews INT,
    Fecha_modificacion DATE,
    Ingredientes TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    images VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
);

-- Cargar los datos en la tabla recetas
LOAD DATA INFILE '/var/lib/mysql-files/recetas_con_imagenes3.csv'
INTO TABLE recetas
FIELDS TERMINATED BY '|'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(Id, Categoria, Nombre, @Valoracion, Dificultad, @Num_comensales, Tiempo, Tipo, Link_receta, @Num_comentarios, @Num_reviews, @Fecha_modificacion, Ingredientes, images)
SET 
    Valoracion = NULLIF(@Valoracion, ''),
    Num_comensales = NULLIF(@Num_comensales, ''),
    Num_comentarios = NULLIF(@Num_comentarios, ''),
    Num_reviews = NULLIF(@Num_reviews, ''),
    Fecha_modificacion = NULLIF(@Fecha_modificacion, '');

