#!/home/pi/plants/venv/bin/python
import time
import configparser
import psycopg2
import datetime
import board
import os
import math
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

debug=True

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
dht_gpio = config['sensors']['dht_gpio']
mi_mac = config['sensors']['mi_mac']

# Initialisation du capteur DHT22
dht_device = adafruit_dht.DHT22(board.D4)

# Fonction pour insérer les données dans la base
def insert_data(tsz, tint, hrint, tpot, hrpot, lumiere, conductivite, batterie, vpd):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        query = """
        INSERT INTO capteurs (tsz, tint, hrint, tpot, hrpot, lumiere, conductivite, batterie, vpd)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (tsz, tint, hrint, tpot, hrpot, lumiere, conductivite, batterie, vpd))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erreur lors de l'insertion des données : {e}")
        exit(-1)

# Boucle principale
def main():
    iteration = 0
    if debug: print("Nouvelle instance - pid: ", os.getpid())
    while iteration < 200:
        try:
            # Maintenant
            maintenant = datetime.datetime.now(datetime.timezone.utc)
            print ("")
            print ("Iteration: ", iteration)
            print("Maintenant: ", maintenant)

            # Lecture du capteur DHT22
            tint = dht_device.temperature + 0.8
            hrint = dht_device.humidity
            if debug: print ("tint: ", tint, "    hrint: ", hrint)

            # calculs vpd
            # https://www.unige.ch/sciences/physique/tp/tpi/Liens/Protocoles/Van_Der_Waals_14.pdf
            # https://pulsegrow.com/blogs/learn/vpd#:~:text=VPD%20%3D%20SVP%20%E2%80%93%20AVP,air%20for%20more%20water%20vapor.
            pvsatair = 610.78 * math.exp((17.2694 * tint) / (tint + 237.3) )
            vpd = round(pvsatair * (1 - hrint/100) / 1000, 3)
            print("VPD: ", vpd)

            # Lecture du capteur MiFlora
            poller = MiFloraPoller(mi_mac, BluepyBackend)
            tpot = poller.parameter_value(MI_TEMPERATURE) - 0.8
            hrpot = poller.parameter_value(MI_MOISTURE)
            lumiere = poller.parameter_value(MI_LIGHT)
            conductivite = poller.parameter_value(MI_CONDUCTIVITY)
            batterie = poller.parameter_value(MI_BATTERY)
            if debug: print ("tpot", tpot, "    hrpot: ", hrpot, "  lumiere: ", lumiere, "  conductivite: ", conductivite, "  batterie: ", batterie)

            # Insertion des données
            insert_data(maintenant, tint, hrint, tpot, hrpot, lumiere, conductivite, batterie, vpd)
            if debug: print ("Donnees inserees")

        except Exception as e:
            print(f"Erreur lors de la lecture des capteurs : {e}")

        iteration += 1
        time.sleep(300)  # 5 minutes

if __name__ == "__main__":
    main()

