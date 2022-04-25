# Private tests

def __validate_string(string: str, target: str):
    if type(string) != str:
        raise ValueError(target + " must be of type string.")

    if len(string) < 1:
        raise ValueError(target + " can't be empty.")


def __validate_integer(integer: int, target: str, _min: int = None, _max: int = None):
    if type(integer) != int:
        raise ValueError(target + " must be of type integer.")

    if _min is not None and integer < _min:
        raise ValueError(target + " can't be lower than " + str(_min) + ".")

    if _max is not None and integer > _max:
        raise ValueError(target + " can't be greater than " + str(_max) + ".")


def __validate_list(l: list, target: str, inside_type: type = None):
    if type(l) not in (list, tuple):
        raise ValueError(target + " must be either of type list or tuple.")

    if len(l) < 1:
        raise ValueError(target + " cannot be empty.")

    if inside_type is not None:
        for i in range(len(l)):
            if type(l[i]) != inside_type:
                raise ValueError(
                    target + "[" + str(i) + "] must be of type " + str(inside_type) + ".")


def __validate_dict(d: dict, target: str):
    if type(d) != dict:
        raise ValueError(target + " must be of type dict.")

    if len(d.keys()) < 1:
        raise ValueError(target + " cannot be empty.")

# Public tests

def validate_url(url: str):
    __validate_string(url, "URL")


def validate_output(output: str):
    __validate_string(output, "Output")


def validate_password(password: str):
    __validate_string(password, "Password")


def validate_html(html: str):
    __validate_string(html, "HTML")


def validate_tag(tag: str):
    __validate_string(tag, "Tag")


def validate_short_code(short_code: str):
    __validate_string(short_code, "Shortcode")


def validate_creator_id(creator_id: str):
    __validate_string(creator_id, "Creator ID")


def validate_artwork_id(artwork_id: str):
    __validate_string(artwork_id, "Artwork ID")


def validate_PHPSESSID(PHPSESSID: str = None):
    if PHPSESSID is not None:
        __validate_string(PHPSESSID, "PHPSESSID")


def validate_pid(pid: int):
    __validate_integer(pid, "PID", 0)


def validate_limit(limit: int):
    __validate_integer(limit, "Limit", 1, 100)


def validate_custom_headers(custom_headers: dict = None):
    if custom_headers is not None:
        __validate_dict(custom_headers, "Custom headers")


def validate_page(page: int):
    __validate_integer(page, "Page", 1)


def validate_tags(tags: list):
    __validate_list(tags, "Tags", str)
