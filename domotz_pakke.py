from requests import get, post


class Domotz:
    def __init__(self, api_key, api_url, agent_select=""):
        self.api_url = api_url
        self.headers = {'Accept': 'application/json', 'X-Api-Key': api_key}
        self.agent = []
        self.agent_select = agent_select

    def agents(self):
        self.agent = []

        for agent in get(self.api_url + '/agent', headers=self.headers).json():
            self.agent.append({"ID": agent['id'], "NAVN": agent['display_name']})
        return self.agent

    def select(self, agent_id):
        self.agent_select = agent_id

    def devices(self):
        enheter = get(f'{self.api_url}/agent/{self.agent_select}/device', headers=self.headers).json()
        return enheter

    def device_merke(self, enhet_merke=""):
        return [enhet for enhet in self.devices() if enhet['vendor'] == enhet_merke]

