from plugins import GoFile
from gofile2 import Gofile
from colorama import Fore
import shutil, requests, datetime, os

#Config
fileiszip = True #Change to true if your file is already zipped.
webhookurl = '' #Put your webhook url here

# Welcoming message
print(Fore.GREEN + "   _____        __ _ _        _____                  _                 _           \n  / ____|      / _(_) |      |  __ \                | |               | |          \n | |  __  ___ | |_ _| | ___  | |__) |___ _   _ _ __ | | ___   __ _  __| | ___ _ __ \n | | |_ |/ _ \|  _| | |/ _ \ |  _  // _ \ | | | '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|\n | |__| | (_) | | | | |  __/ | | \ \  __/ |_| | |_) | | (_) | (_| | (_| |  __/ |   \n  \_____|\___/|_| |_|_|\___| |_|  \_\___|\__,_| .__/|_|\___/ \__,_|\__,_|\___|_|   \n                                              | |                                  \n                                              |_|                                  ")
print()
print(Fore.YELLOW + "Hello Welcome to GoFile Reuploader. This is a simple program that will reupload a file from Gofile to GoFile!\nDo to GoFile's API limitations, this program can only upload files that are in ZIP format.\nIts siple you only enter Gofile link and password (if the file has one) we will download it and upload it!\nIf they are not Zip or there are more than 1 there is no problem We Will Create Zip File with all your files inside.\nThen We will upload that file to Gofile and Send Link Straight To Your Discord Channel With Webhook!")
print()
input(Fore.LIGHTRED_EX + "Press Any key to continue...")

#Get Gofile Info
durl = input("Enter the GoFile url: ")
dpassword = input("Enter the GoFile password (If One): ")

class GofileReuploader:
    #Initialize
    def __init__(self):
        self.webhook = webhookurl
        #Create "temp" folder
        os.makedirs('temp', exist_ok=True)
        os.makedirs('temp/output', exist_ok=True)
        #Run Main Script
        self.main()
    
    
    def main(self):
        #Variebles
        output = "temp/output"
        url = durl
        password = dpassword or None

        print(Fore.YELLOW + "Downloading file...")
        #Download File
        api = GoFile()
        for u in api.fetch_resources(url, password):
            api.download_file(u, output)

        g_a = Gofile()

        print(Fore.CYAN + "Successfully downloaded file.")

        #Check if file is zip
        if fileiszip == False:
            output_filename = 'temp/reupload'
            input_dir = 'temp/output'
            #Create zip file
            shutil.make_archive(output_filename, 'zip', input_dir)
            print(Fore.CYAN + "Successfully Created Zip File.")
            #Upload file to Gofile
            uurl1 = g_a.upload(file='temp/reupload.zip')
            uurl2 = g_a.upload(file='temp/reupload.zip')
            uurl3 = g_a.upload(file='temp/reupload.zip')
            self.file1 = f"**Mirror #1: [{uurl1['downloadPage']}]({uurl1['downloadPage']})**"
            self.file2 = f"**Mirror #2: [{uurl2['downloadPage']}]({uurl2['downloadPage']})**"
            self.file3 = f"**Mirror #3: [{uurl3['downloadPage']}]({uurl3['downloadPage']})**"
            #Send Info to Webhook
            self.WebhookSender(self.file1, self.file2, self.file3)
        else:
            #Get File name to upload to Gofile
            fileid = input(Fore.YELLOW + 'Please State name of the Zip File to upload (Without ".zip"): ')
            #Upload file to Gofile
            uurl1 = g_a.upload(file='temp/output/' + fileid + '.zip')
            uurl2 = g_a.upload(file='temp/output/' + fileid + '.zip')
            uurl3 = g_a.upload(file='temp/output/' + fileid + '.zip')
            print(Fore.CYAN + "Successfully Uploaded File.")
            self.file1 = f"**Mirror #1: [{uurl1['downloadPage']}]({uurl1['downloadPage']})**"
            self.file2 = f"**Mirror #2: [{uurl2['downloadPage']}]({uurl2['downloadPage']})**"
            self.file3 = f"**Mirror #3: [{uurl3['downloadPage']}]({uurl3['downloadPage']})**"
            #Send Info to Webhook
            self.WebhookSender(self.file1, self.file2, self.file3)
            #Delete "temp" folder
            shutil.rmtree("./temp")


    def WebhookSender(self, file1, file2, file3):
        #Set today date for webhook
        today = datetime.date.today()
        #Set webhook message
        embed = {
            "avatar_url":"https://cdn.discordapp.com/attachments/717746524200632400/968089328909692928/unknown.png",
            "name":"Gofile Reuploader",
            "embeds": [
                {
                    "author": {
                        "name": "Gofile Reuploade",
                        "icon_url": "https://cdn.discordapp.com/attachments/717746524200632400/968089328909692928/unknown.png",
                        },
                    "description": f"Reuploadet File: \n{file1}\n{file2}\n{file3}",
                    "color": 8421504,
                    "footer": {
                    "text": f"File Reuploadet at・{today}"
                    }
                }
            ]
        }
        #Send webhook
        requests.post(self.webhook, json=embed)
        print(Fore.GREEN + "Successfully Sent Webhook.")
if __name__ == "__main__":
    GofileReuploader()
