# Plants

## hardware

* Raspberry pi arm64 running 64 bits raspberry pi os
* DHT22/AM2302 on gpio - requires resistor if not embedded
* miflora compatible - bluetooth scan for mac

## system packages / softwares

Working on Raspbberry os 13 - bookworm or 14 - Trixie

You may want to turn off raspberry pi leds in greenhouse, add to /boot/firmware/config.txt:
```
dtparam=act_led_trigger=none
dtparam=pwr_led_trigger=none
```

### minimum system package
```
sudo apt install locales-all swig vim
sudo apt install libglib2.0-dev liblgpio-dev
```

### python

Comes with raspberry os

### postgresql database
```
sudo apt install postgresql
```
Influxdb possibly more performant

## populate
```
git clone https://github.com/mounirst/plants.git
cd plants
```

## python venv

```
python -m venv venv
source venv/bin/activate
pip install psycopg2-binary adafruit-circuitpython-dht btlewrap miflora bluepy
```

## db creation
Check file plants.sql for customization.

```
sudo -u postgres psql -f plants.sql
```


## systemd activation
Check file config.ini for password and miflora mac address customization.

```
sudo cp plants.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable plants.service
sudo systemctl start plants.service
```

# Camera capture
## Confirm camera operation
## Capture script
# Dashboard
## Grafana installation
https://grafana.com/tutorials/install-grafana-on-raspberry-pi/
## Metadata dashboard
## Image link to capture
