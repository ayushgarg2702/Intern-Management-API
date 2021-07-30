import re


def CheckMobileNumber(param: str) -> bool:
    if re.search(r"^[6-9]\d{9}$", str(param)):
        return True
    else:
        return False