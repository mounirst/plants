-- Création de la base de données
CREATE DATABASE plants;

-- Connexion à la base de données
\c plants

-- Création de la table
CREATE TABLE capteurs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    temp_dht FLOAT,
    humidity_dht FLOAT,
    temp_mi FLOAT,
    moisture INTEGER,
    light INTEGER,
    conductivity INTEGER,
    battery INTEGER,
    vpd FLOAT
);

-- Création de l'utilisateur et attribution des droits
CREATE USER plants_user WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE plants TO plants_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO plants_user;

