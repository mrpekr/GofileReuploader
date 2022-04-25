from plugins import GoFile
from gofile2 import Gofile
import shutil, requests, time, datetime
from colorama import Fore, Back, Style

#Config
fileiszip = True #Change to true if your file is already zipped.
webhookurl = '' #Put your webhook url here

print(Fore.YELLOW + "Hello Welcome to GoFile Reuploader. This is a simple program that will reupload a file from Gofile to GoFile.\nDo to GoFile's API limitations, this program can only upload files that are in ZIP format.")
print("Do not Worry! We will create zip file for you and then upload it to Gofile. If you file is already in ZIP format,\nPlease Change Config If you havent done alredy and we will just upload it to Gofile.")
input(Fore.WHITE + "Press Any key to continue...")

durl = input("Enter the GoFile url: ")
dpassword = input("Enter the GoFile password (If One): ")

class GofileReuploader:
    def __init__(self):
        self.webhook = webhookurl

        self.main()
    
    def main(self):
        output = "temp/output"
        url = durl
        password = dpassword or None

        api = GoFile()
        for u in api.fetch_resources(url, password):
            api.download_file(u, output)

        g_a = Gofile()

        print(Fore.CYAN + "Successfully downloaded file.")

        if fileiszip == False:
            output_filename = 'temp/reupload'
            input_dir = 'temp/output'
            # shutil also support 'tar' format, here we use 'zip' format
            shutil.make_archive(output_filename, 'zip', input_dir)
            print(Fore.CYAN + "Successfully Created Zip File.")
            uurl1 = g_a.upload(file='temp/reupload.zip')
            uurl2 = g_a.upload(file='temp/reupload.zip')
            uurl3 = g_a.upload(file='temp/reupload.zip')
            self.file1 = f"**Mirror #1: [{uurl1['downloadPage']}]({uurl1['downloadPage']})**"
            self.file2 = f"**Mirror #2: [{uurl2['downloadPage']}]({uurl2['downloadPage']})**"
            self.file3 = f"**Mirror #3: [{uurl3['downloadPage']}]({uurl3['downloadPage']})**"
            self.WebhookSender(self.file1, self.file2, self.file3)
        else:
            fileid = input(Fore.YELLOW + 'Please State name of the Zip File to upload (Without ".zip"): ')
            uurl1 = g_a.upload(file='temp/output/' + fileid + '.zip')
            uurl2 = g_a.upload(file='temp/output/' + fileid + '.zip')
            uurl3 = g_a.upload(file='temp/output/' + fileid + '.zip')
            print(Fore.CYAN + "Successfully Uploaded File.")
            self.file1 = f"**Mirror #1: [{uurl1['downloadPage']}]({uurl1['downloadPage']})**"
            self.file2 = f"**Mirror #2: [{uurl2['downloadPage']}]({uurl2['downloadPage']})**"
            self.file3 = f"**Mirror #3: [{uurl3['downloadPage']}]({uurl3['downloadPage']})**"
            self.WebhookSender(self.file1, self.file2, self.file3)

    def WebhookSender(self, file1, file2, file3):
        today = datetime.date.today()
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
        requests.post(self.webhook, json=embed)
        print(Fore.GREEN + "Successfully Sent Webhook.")

if __name__ == "__main__":
    GofileReuploader()