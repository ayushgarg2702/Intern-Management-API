"""
For Reference : https://github.com/realpython/flask-jwt-auth/blob/master/project/server/models.py
"""
import jwt
import datetime
from common.read_configuration import read_config
from common.read_logger import LoggerSetup

logger = LoggerSetup(loggerName=str(__file__)).getLogger()


def encode_auth_token(data: dict, timedeltavalue: int = 60) -> str:
    """
    This function encode jwt token
    :param token: this is string type of input which contains jwt token.
        Sample token:
    :return:
    """
    try:
        config = read_config()
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=timedeltavalue),
            "iat": datetime.datetime.utcnow(),
            "sub": data["userid"],
        }
        jwt_secret_key = config["JWT"]["jwt_secret_key"]
        jwt_algo = config["JWT"]["jwt_algo"]
        return {
            "status": "SUCCESS",
            "message": str(
                jwt.encode(payload, jwt_secret_key, jwt_algo).decode("utf-8")
            ),
        }
    except Exception as e:
        logger.error(e, exc_info=True)
        return {"status": "ERROR", "message": "An error occured on server-side"}


def decode_auth_token(auth_token: str) -> str:
    """
    Validates the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        config = read_config()
        payload = jwt.decode(auth_token, config["JWT"]["jwt_algo"])
        return {"status": "SUCCESS", "message": str(payload["sub"])}
    except jwt.ExpiredSignatureError:
        return {
            "status": "ERROR",
            "message": " Signature expired. Please log in again.",
        }
    except jwt.InvalidTokenError:
        return {"status": "ERROR", "message": "Invalid token. Please log in again."}
    except Exception as e:
        logger.error(e, exc_info=True)
        return {"status": "ERROR", "message": "An error occured on server-side"}
