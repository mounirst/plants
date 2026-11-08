#!/bin/bash

# Répertoire de stockage des images
REP="/home/pi/plants/images"
mkdir -p $REP

# Compteur d'itérations
ITERATION=0
MAX_ITERATIONS=100

# Entre chaque photo en secondes
INTERVALLE=900 # 15mn

# Lien symbolique pour la dernière image
LAST_IMAGE="$REP/last-image.jpeg"

{

# Boucle principale
while [ $ITERATION -lt $MAX_ITERATIONS ]
do
	datejour=$(date --iso-8601)
	datemin=$(date --iso-8601=minutes)

	# repertoire du jour
	mkdir -p $REP/$datejour

	# Capture de l'image
	IMG=$REP/$datejour/img-$datemin.jpeg
	rpicam-jpeg -o $IMG --nopreview

	# Mise à jour du lien symbolique
	ln -sf $IMG $LAST_IMAGE

	# Mise à jour du lien dans grafana
	sudo cp $IMG /usr/share/grafana/public/img/capture-last.jpeg

    # Incrémentation du compteur
    ((ITERATION++))

    # Attente entre chaque photo
    sleep $INTERVALLE
done

# Purge des images de plus de 6 mois
echo find "$REP" -type f -mtime +180 -delete
find "$REP" -name "*.jpeg" -type f -mtime +180 -delete

exit 0

} >$REP/../log.out 2>&1
