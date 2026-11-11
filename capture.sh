#!/bin/bash

GRSP=hs40
GRSP=$(awk '/growspace/ {print $3}' config.ini)

# Répertoire de stockage des images
REP="/home/pi/plants/images"
mkdir -p $REP

# Compteur d iterations
ITERATION=0
MAX_ITERATIONS=100

# Entre chaque photo en secondes
INTERVALLE=3600 # 1h par defaut
INTERVALLE=$(awk '/intervalle/ {print $3}' config.ini)


# Lien symbolique pour la derniere image
LAST_IMAGE="$REP/last_image_$GRSP.jpeg"

{

# Boucle principale
while [ $ITERATION -lt $MAX_ITERATIONS ]
do
	datejour=$(date --iso-8601)
	datemin=$(date --iso-8601=minutes)
	echo $datemin

	# repertoire du jour
	mkdir -p $REP/$datejour && echo Creation du repertoire du jour

	# Capture de l image
	IMG=$REP/$datejour/img-$datemin.jpeg
	echo "Capture en cours..."
	rpicam-jpeg -o $IMG --nopreview
	echo "Capture terminee"

	# Mise à jour du lien symbolique
	ln -sf $IMG $LAST_IMAGE

	# Mise a jour dans grafana
	echo envoi de l image $IMG
	scp $IMG root@192.168.1.46:/usr/share/grafana/public/img/last_image_$GRSP.jpeg
	scp $IMG root@192.168.1.34:/usr/share/grafana/public/img/last_image_$GRSP.jpeg
	echo fin de l envoi

    ((ITERATION++))

    # Attente entre chaque photo
    sleep $INTERVALLE
done

# Purge des images de plus de 6 mois
echo find "$REP" -type f -mtime +180 -delete
find "$REP" -name "*.jpeg" -type f -mtime +180 -delete

exit 0

} 
# } >$REP/../log.out 2>&1
