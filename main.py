from pakker.crestron import *
from pakker.domotz import *
from json import load

config = load(open('config.json'))

id = 0
agent_valg = "CB6"
crestron_brukernavn = "admin"
crestron_passord = "admin"


def getCrestron():
    domotz = Domotz(api_key=config['api_key'], api_url=config['api_url'])
    for agent in domotz.agents():
        if agent['NAVN'] == agent_valg:
            domotz.select(agent['ID'])

    enheter = {}
    for enhet in domotz.devices():
        if enhet['vendor'] == 'CRESTRON ELECTRONICS, INC.' and enhet['status'] == 'ONLINE':
            enheter.update({enhet['id']: {'ip': enhet['ip_addresses'][0], 'navn': enhet['names']['host'], 'id': enhet['id'],
                             'model': enhet['model']}})

    return enheter

for enhet in getCrestron().values():
    crestron = EasyCrestron(ip=enhet['ip'], brukernavn=crestron_brukernavn, passord=crestron_passord)
    print(f'ID: {enhet["id"]} | Model: {crestron.EnhetInfo()["Model"]} | Firmware: {crestron.FirmwareInfo()}')
