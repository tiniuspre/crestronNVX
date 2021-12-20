from requests import get, post, urllib3
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

urllib3.disable_warnings()


class Crestron:
    def __init__(self, ip, brukernavn='', passord=''):
        self.url = "https://" + str(ip)
        self.passord = passord
        self.brukernavn = brukernavn
        self.cookies = self.login()["cookies"]
        self.headers = self.login()["headers"]

    def login(self):
        cred = post(f"{self.url}/userlogin.html", headers={
            "Cookie": f"TRACKID={get(f'{self.url}/userlogin.html', verify=False).cookies.get_dict()['TRACKID']}",
            "Origin": f"{self.url}/", "Referer": f"{self.url}/userlogin.html"}, data=f"login={self.brukernavn}&&passwd={self.passord}",
                    verify=False)
        return {"headers": cred.headers, "cookies": cred.cookies}

    def send_command(self, path_to_execute, data):
        data = post(self.url+path_to_execute, headers=self.headers, cookies=self.cookies, data=data, verify=False)
        return json.loads(data.text)

    def hent_info(self, path_til_info):
        data = get(self.url+path_til_info, headers=self.headers, cookies=self.cookies, verify=False)
        return json.loads(data.text)['Device']

    def upgrade(self, path_til_fil):
        fil = {'file': ('dm-nvx_4.1.4472.00021.puf', open(path_til_fil, 'rb'), 'multipart/form-data', {'Expires': '0'})}
        data = {
            "Device": {
                "DeviceOperations": {
                    "FirmwareUpgrade": "dm-nvx_4.1.4472.00021.puf",
                    "FirmwareUpgradeType": "Http",
                    "FirmwareUpgradePath": "dm-nvx_4.1.4472.00021.puf"
                }
            }
        }

        fil_upload = post(self.url+"/Device/DeviceOperations/FirmwareUpgrade", headers=self.headers, data=data, cookies=self.cookies, files=fil, verify=False)
        print("------------------------------------------------------")
        print(fil_upload.json())
        print(fil_upload.text)
        print(fil_upload.status_code)
        print("------------------------------------------------------")
        return fil_upload.json()


class EasyCrestron(Crestron):
    def __init__(self, ip, brukernavn, passord):
        super().__init__(ip, brukernavn, passord)

    def AllInfo(self):
            return self.hent_info("/Device/")

    def GenerellInfo(self):
        return self.hent_info(f"/Device/DeviceInfo/")['DeviceInfo']

    def VifteInfo(self):
        return self.hent_info(f"/Device/FanControl/")['FanControl']

    def EnhetInfo(self):
        return self.hent_info(f"/Device/DeviceInfo/")['DeviceInfo']

    def FirmwareInfo(self):
        return self.hent_info(f"/Device/DeviceInfo/")['DeviceInfo']['DeviceVersion']

    def DeviceOp(self):
        return self.hent_info(f"/Device/DeviceOperations/")

    def Restart(self):
        return post(self.url+'/Device/DeviceOperations/', headers=self.headers, cookies=self.cookies, data={"DeviceOperations": {"Reboot": True}}, verify=False)