import os
import requests
from .magic_table import __magic_tablify
from .validator import validate_custom_headers, validate_url


def __build_headers(url: str, custom_headers: dict = None, as_list: bool = False):
    validate_url(url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0",
        "Accept": "*/*",
        "Referer": url + ("/" if not url.endswith("/") else ""),
        "Origin": url,
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache"
    }

    if custom_headers is not None:
        validate_custom_headers(custom_headers)

        for k, v in custom_headers.items():
            headers[str(k)] = str(v)

    if not as_list:
        return headers

    headers_list = [None] * len(headers.keys())

    i = 0
    for k, v in headers.items():
        headers_list[i] = (str(k), str(v))
        i += 1

    return headers_list


def http_download(url: str, output_folder: str, custom_headers: dict = None):
    validate_url(url)
    validate_custom_headers(custom_headers)

    filename = url.split('/')[-1].split('?')[0]
    filename = filename.replace("%20", ' ')
    output = os.path.join(output_folder, filename)
    if os.path.exists(output):
        return

    url = __magic_tablify(url)
    headers = __build_headers(url, custom_headers)

    with requests.get(url, headers=headers, stream=True) as response_stream:
        if response_stream.status_code in (403, 404, 405, 500):
            return

        with open(output, 'wb') as stream:
            for chunk in response_stream.iter_content(chunk_size=8192):
                if chunk:
                    stream.write(chunk)
        stream.close()
    response_stream.close()