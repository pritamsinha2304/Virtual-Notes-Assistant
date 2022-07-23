""" Holds the Csrf Settings Token """

# pylint: disable=no-name-in-module

import secrets
from pydantic import BaseModel

class CsrfSettings(BaseModel):
    """Generate the secret token

    Args:
        BaseModel (_type_)
    """
    secret_key:str = secrets.token_hex(64)
    