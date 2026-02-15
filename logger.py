#!/home/pi/plants/bin/python
import time
import configparser
import psycopg2
from datetime import datetime
import board
import adafruit_dht

# pour miflora
import re

from btlewrap import BluepyBackend, GatttoolBackend, PygattBackend, available_backends

from miflora import miflora_scanner
from miflora.miflora_poller import (
    MI_BATTERY,
    MI_CONDUCTIVITY,
    MI_LIGHT,
    MI_MOISTURE,
    MI_TEMPERATURE,
    MiFloraPoller,
)
# fin miflora


# from btlewrap import BluepyBackend
# from miflora.miflora_poller import MiFloraPoller, MI_CONDUCTIVITY, MI_BRIGHTNESS, MI_TEMPERATURE, MI_MOISTURE, MI_BATTERY

# Charger la configuration
config = configparser.ConfigParser()
config.read('/home/pi/plants/config.ini')

# Paramètres de la base de données
db_config = {
    'dbname': config['postgresql']['dbname'],
    'user': config['postgresql']['user'],
    'password': config['postgresql']['password'],
    'host': config['postgresql']['host'],
    'port': config['postgresql']['port']
}

# Paramètres des capteurs
dht_gpio = int(config['sensors']['dht_gpio'])
mi_mac = config['sensors']['mi_mac']

# Initialisation du capteur DHT22
dht_device = adafruit_dht.DHT22(board.D{dht_gpio})

# Fonction pour calculer le DVP (Déficit de Pression de Vapeur)
def calculate_vpd(temp, humidity):
    # Constantes
    a = 17.27
    b = 237.7
    # Calcul de la pression de vapeur saturante (es)
    es = 0.6108 * (10 ** ((a * temp) / (b + temp)))
    # Calcul de la pression de vapeur réelle (ea)
    ea = (humidity / 100) * es
    # Calcul du DVP
    vpd = es - ea
    return vpd

# Fonction pour insérer les données dans la base
def insert_data(temp_dht, humidity_dht, temp_mi, moisture, light, conductivity, battery, vpd):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        query = """
        INSERT INTO capteurs (timestamp, temp_dht, humidity_dht, temp_mi, moisture, light, conductivity, battery, vpd)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (datetime.now(), temp_dht, humidity_dht, temp_mi, moisture, light, conductivity, battery, vpd))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erreur lors de l'insertion des données : {e}")

# Boucle principale
def main():
    iteration = 0
    while iteration < 200:
        try:
            # Lecture du capteur DHT22
            temp_dht = dht_device.temperature
            humidity_dht = dht_device.humidity
            vpd = calculate_vpd(temp_dht, humidity_dht)

            # Lecture du capteur MiFlora
            poller = MiFloraPoller(mi_mac, BluepyBackend)
            temp_mi = poller.parameter_value(MI_TEMPERATURE)
            moisture = poller.parameter_value(MI_MOISTURE)
            light = poller.parameter_value(MI_BRIGHTNESS)
            conductivity = poller.parameter_value(MI_CONDUCTIVITY)
            battery = poller.parameter_value(MI_BATTERY)

            # Insertion des données
            insert_data(temp_dht, humidity_dht, temp_mi, moisture, light, conductivity, battery, vpd)
            print(f"Itération {iteration + 1} : Données insérées avec succès.")

        except Exception as e:
            print(f"Erreur lors de la lecture des capteurs : {e}")

        iteration += 1
        time.sleep(300)  # Attendre 5 minutes

if __name__ == "__main__":
    main()

