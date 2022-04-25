from plugins import GoFile
from gofile2 import Gofile
from colorama import Fore
import shutil, requests, datetime, os

#Config
fileiszip = False #Change to true if your file is already zipped.
webhookurl = '' #Put your webhook url here

# Welcoming message
print(Fore.YELLOW + "Hello Welcome to GoFile Reuploader. This is a simple program that will reupload a file from Gofile to GoFile.\nDo to GoFile's API limitations, this program can only upload files that are in ZIP format.")
print("Do not Worry! We will create zip file for you and then upload it to Gofile. If you file is already in ZIP format,\nPlease Change Config If you havent done alredy and we will just upload it to Gofile.")
input(Fore.WHITE + "Press Any key to continue...")

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
