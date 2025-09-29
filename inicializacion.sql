CREATE TABLE rol (
    id SERIAL PRIMARY KEY,
    rol VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE login (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    clave BYTEA NOT NULL
);

CREATE TABLE usuario (
    id INTEGER PRIMARY KEY REFERENCES login(id) ON DELETE CASCADE,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    rol INTEGER REFERENCES rol(id)
);

CREATE TABLE publicacion (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    barrio VARCHAR(100),
    calle VARCHAR(100),
    ambientes INTEGER,
    balcon BOOLEAN,
    usuario_id INTEGER REFERENCES usuario(id) ON DELETE SET NULL,
    autor VARCHAR(50),
    imagenes JSONB,
    precio INTEGER
);
