# Plants

## hardware

* Raspberry pi
* DHT22/AM2302 on gpio - requires resistor if not embedded
* miflora compatible - bluetooth scan for mac

## system packages / softwares

Raspbberry os 14 - Trixie

### python

Comes with raspberry os

### postgresql database
```
apt install postgresql
```
Influxdb possibly more performant

## populate
```
mkdir plants
cd plants
git clone https://github.com/mounirst/plants.git
```

## python venv

```
python -m venv venv
source venv/bin/activate
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

# extensions

## cam capture

## metadata dashboard



