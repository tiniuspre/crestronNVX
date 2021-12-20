from crestron_pakke import *
from domotz_pakke import *
from json import load

config = load(open('config.json'))

id = 0
agent_valg = "CB6"


def getCrestron():
    domotz = Domotz(api_key=config['api_key'], api_url=config['api_url'])
    for agent in domotz.agents():
        if agent['NAVN'] == agent_valg:
            domotz.select(agent['ID'])

    enheter = {}
    for enhet in domotz.devices():
        if enhet['vendor'] == 'CRESTRON ELECTRONICS, INC.':
            enheter.update({enhet['id']: {'ip': enhet['ip_addresses'][0], 'navn': enhet['names']['host'], 'id': enhet['id'],
                             'model': enhet['model']}})

    return enheter
