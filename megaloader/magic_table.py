from .validator import validate_url

MAGIC_TABLE = {
    "https://pornlyfans.com": "http://81.171.12.37"
}


def __magic_tablify(url: str) -> str:
    validate_url(url)

    for mt_k, mt_v in MAGIC_TABLE.items():
        if url.startswith(mt_k):
            url = url.replace(mt_k, mt_v)
            break

    return url
