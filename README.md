# Plants

## hardware

* any Raspberry
* DFRobot DHT22 on gpio 4
* miflora compatible - bluetooth scan for mac

## system packages

apt install 

## populate

```
mkdir plants
cd plants
git clone https://github.com/mounirst/plants.git
```

## python venv

```
python -m venv venv
source activate venv/bin/activate
pip install psycopg2-binary adafruit-circuitpython-dht btlewrap miflora
```

## db creation

```
sudo -u postgres psql -f plants.sql
```


## systemd activation

```
sudo cp plants.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable plants.service
sudo systemctl start plants.service
```

## extensions

### cam capture

### metadata dashboard



