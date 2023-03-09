import json
import logging
import os
import subprocess
import threading
import time

from src import get_project_root
from src.Database import Database
from src.DiscordBot import DiscordBot


class ConsigneBot(threading.Thread):
    def __init__(self, database: Database, discord_bot: DiscordBot, linux=False):
        super(ConsigneBot,self).__init__()
        self.linux = linux
        self.database = database
        self.discord_bot = discord_bot
        self.active_users = discord_bot.active_users
        self.accepted = 0

    def get_bearer(self, token):
        if self.linux:
            file_path = os.path.join(get_project_root(), "curl/linux/curl_chrome110")
            cmd = file_path + f" 'https://sell.wethenew.com/api/auth/session' \
    -H 'authority: sell.wethenew.com' \
    -H 'accept: */*' \
    -H 'cookie: __Secure-next-auth.session-token={token}' \
    -H 'dnt: 1' \
    -H 'referer: https://sell.wethenew.com/fr/consignment'"
        else:
            file_path = os.path.join(get_project_root(), "curl/windows/curl_chrome110.bat")
            cmd = file_path + f" https://sell.wethenew.com/api/auth/session ^\
    -H \"authority: sell.wethenew.com\" ^\
    -H \"accept: */*\" ^\
    -H \"cookie: __Secure-next-auth.session-token={token}\" ^\
    -H \"dnt: 1\" ^\
    -H \"referer: https://sell.wethenew.com/fr/consignment\""
        print(cmd)
        run = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = run.stdout
        try:
            output_json = json.loads(output)
        except json.decoder.JSONDecodeError as e:
            print("Erreur lors de la requête vers l'API :")
            print(e)
            print("Exécution du script :")
            print(run.stderr)
            print(run.stdout)
            return
        print(output_json)
        if "user" not in output_json.keys():
            print("Erreur mauvais token")
            return
        bearer = output_json["user"]["accessToken"]
        return bearer


    def get_consigne(self, bearer: str, num_product):
        if self.linux:
            file_path = os.path.join(get_project_root(), "curl/linux/curl_chrome110")
            cmd = file_path + f" 'https://api-sell.wethenew.com/products/{num_product}/consignments' \
    -H 'authority: api-sell.wethenew.com' \
    -H 'accept: application/json, text/plain, */*' \
    -H 'authorization: Bearer {bearer}' \
    -H 'cache-control: no-cache' \
    -H 'dnt: 1' \
    -H 'origin: https://sell.wethenew.com' \
    -H 'pragma: no-cache' \
    -H 'referer: https://sell.wethenew.com/' \
    -H 'x-xss-protection: 1;mode=block'"
        else:
            file_path = os.path.join(get_project_root(), "curl/windows/curl_chrome110.bat")
            cmd = file_path + f" https://api-sell.wethenew.com/products/{num_product}/consignments ^\
    -H \"authority: api-sell.wethenew.com\" ^\
    -H \"accept: application/json, text/plain, */*\" ^\
    -H \"authorization: Bearer {bearer}\" ^\
    -H \"cache-control: no-cache\" ^\
    -H \"dnt: 1\" ^\
    -H \"origin: https://sell.wethenew.com\" ^\
    -H \"pragma: no-cache\" ^\
    -H \"referer: https://sell.wethenew.com/\" ^\
    -H \"x-xss-protection: 1;mode=block\""
        print(cmd)
        # output: {"pagination":{"totalPages":0,"page":1,"itemsPerPage":25,"totalItems":0},"results":[]}
        run = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        output = run.stdout
        try:
            output_json = json.loads(output)
        except json.decoder.JSONDecodeError as e:
            print("Erreur lors de la requête vers l'API :")
            print(e)
            print("Exécution du script :")
            print(run.stderr)
            print(run.stdout)
            return
        print(output_json)
        if "variants" not in output_json.keys():
            print("Error: " + output_json["message"])
            return
        for consignment in output_json["variants"]:
            if consignment["remaining"] > 0:
                print(consignment)


    def main(self):
        # logging.info("Waiting for new users to start the bot")
        while True:
            print(self.active_users)
            i = 0
            while i < len(self.active_users):
                user = self.active_users[i]
                if self.database.get_token(user) is not None:
                    i += 1
                    token = self.database.get_token(user)
                    num_product = self.database.get_all_consigne(user)
                    print(num_product)
                    bearer = self.get_bearer(token)
                    print(bearer)
                    for product in num_product:
                        self.get_consigne(bearer, product[0])


            time.sleep(2)
                    # bearer = self.get_bearer(token, 1)
                    # self.get_consigne(bearer, 1)
                    # i += 1

    def run(self):
        logging.info("Starting WTNConsigneBot | Thread ID: " + str(self.ident))
        self.main()
