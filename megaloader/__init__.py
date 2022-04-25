def is_video(url: str) -> bool:
    if type(url) != str:
        raise ValueError("URL must be a string.")

    if len(url) < 1:
        raise ValueError("URL can't be empty.")

    for e in ("mp4", "mov", "m4v", "ts", "mkv", "avi", "wmv", "webm", "vob", "gifv", "mpg", "mpeg"):
        if url.endswith(e):
            return True
    return False


def unentitify(string: str) -> str:
    if type(string) != str:
        raise ValueError("String must be a string.")

    if len(string) < 1:
        raise ValueError("String can't be empty.")

    string = string.replace("&quot;", "\"")
    return string
