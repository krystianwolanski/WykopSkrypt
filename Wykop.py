import hashlib
import json

import requests

class Wykop:
    def __init__(self):
        self.appkey = ""
        self.secret = ""


    def do_request(self, url, type, data={}, timeout=60):

        if type == "POST":
            userkey = self.getConfigValue('userkey')
            url_wykop = f"{url}appkey/{self.appkey}/userkey/{userkey}/"
        else:
            url_wykop = f"{url}appkey/{self.appkey}/"

        values = ",".join(data.values())
        apisign = hashlib.md5((self.secret + url_wykop + values).encode()).hexdigest()

        response = requests.request(type, url_wykop, data=data, headers=
        {
            "apisign": apisign
        }, timeout=timeout)

        return response.json()

    def new_user_key(self):
        with open("jsons/config.json", "r") as file:
            jsonFile = json.load(file)

        loginData = {
            "login": "",
            "password": "",
            "accountkey": ""
        }

        jsonFile['userkey'] = self.do_request("https://a2.wykop.pl/Login/Index/", "POST", loginData)['data']['userkey']
        with open("jsons/config.json", 'w') as f:
            json.dump(jsonFile, f)

    def get_up_voters(self,id: str):
        request = self.do_request('https://a2.wykop.pl/Entries/Upvoters/' + id + '/', 'GET')
        return request

    def add_comment(self,id: str, body: str, embed=''):
        request = self.do_request('https://a2.wykop.pl/Entries/CommentAdd/' + id + '/', 'POST',
                             {"body": body, 'embed': embed}, 60)
        return request

    def getConfigValue(self,parameter):
        with open("jsons/config.json", "r") as file:
            jsonFile = json.load(file)
            return jsonFile[parameter]