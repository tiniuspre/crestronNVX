from crestron_pakke import *
from domotz_pakke import *
from json import load

config = load(open('config.json'))

crestron = EasyCrestron(ip="10.0.11.181", brukernavn="admin", passord="admin")
domotz = Domotz(api_key=config['api_key'], api_url=config['api_url'])

