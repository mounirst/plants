-- Création de la base de données
CREATE DATABASE plants;

-- Connexion à la base de données
\c plants

-- Création de la table
CREATE TABLE capteurs (
    id SERIAL PRIMARY KEY,
    tsz TIMESTAMP with time zone NOT NULL,
    tint FLOAT,
    hrint FLOAT,
    tpot1 FLOAT,
    hrpot1 INTEGER,
    lum1 INTEGER,
    conduct1 INTEGER,
    batt1 INTEGER,
    tpot2 FLOAT,
    hrpot2 INTEGER,
    lum2 INTEGER,
    conduct2 INTEGER,
    batt2 INTEGER,
    vpd FLOAT
);

-- Création de l'utilisateur et attribution des droits
CREATE USER plants_user WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE plants TO plants_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO plants_user;
GRANT USAGE, SELECT, UPDATE ON SEQUENCE capteurs_id_seq to plants_user;
