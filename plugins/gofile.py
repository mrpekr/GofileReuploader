import re
import hashlib
import requests
from megaloader.http import http_download
from megaloader.validator import validate_password, validate_url, validate_output


class GoFileErrorPageNotFound(Exception):
    pass


class GoFile:
    def __init__(self) -> None:
        self.api_key = self.__get_api_key()

    def fetch_resources(self, url: str, password: str = None) -> list:
        validate_url(url)

        if not re.match(r"^http(?:s):\/\/gofile\.io\/d\/", url):
            raise ValueError("URL must be a GoFile URL.")

        content_id = url[len("https://gofile.io/d/"):]
        if len(content_id) == 0:
            raise ValueError(
                "An error occured while extracting the Content ID from '" + url + "'.")

        url = "https://api.gofile.io/getContent?contentId=" + content_id + \
            "&token=" + self.api_key + "&websiteToken=12345&cache=true"

        if password is not None:
            validate_password(password)
            password = hashlib.sha256(password.encode()).hexdigest()
            url += "&password=" + password

        resources = requests.get(url).json()
        if "contents" not in resources["data"].keys():
            raise GoFileErrorPageNotFound()

        links = []
        contents = resources["data"]["contents"]

        for content in contents.values():
            link = content["link"]
            if link not in links:
                links.append(link)

        return links

    def download_file(self, url: str, output: str):
        validate_url(url)
        validate_output(output)
        http_download(url, output, custom_headers={
            "Cookie": "accountToken=" + self.api_key,
            "Accept-Encoding": "gzip, deflate, br"
        })

    @staticmethod
    def __get_api_key() -> str:
        # Gets a new account token
        data = requests.get("https://api.gofile.io/createAccount").json()
        api_token = data["data"]["token"]

        # Activate the new token
        data = requests.get(
            "https://api.gofile.io/getAccountDetails?token=" + api_token).json()
        if data["status"] != 'ok':
            raise Exception("The account was not successfully activated.")

        return api_token
