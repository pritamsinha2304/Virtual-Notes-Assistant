""" Holds the model schema """

# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument

from fastapi import File, UploadFile
from pydantic import BaseModel, validator


class FormData(BaseModel):
    """Foem Data Validator

    Args:
        BaseModel (_type_): BaseModel

    Returns:
        FormData: Form Data
    """
    file: UploadFile

    @validator('file')
    def check_extension(cls, data):
        """File Field Validation

        Args:
            data (_type_): _description_

        Returns:
            Form Field
        """
        if not data.filename.endswith(('.wav',
                                       '.mp3',
                                       '.aac',
                                       '.aiff',
                                       '.flac',
                                       '.m4a',
                                       '.ogg',
                                       '.opus',
                                       '.wma')):
            return ValueError('Invalid File Format')
        return data

    @classmethod
    def as_form(cls, file: UploadFile = File(...)):
        """Return Form Data

        Args:
            file (UploadFile): Uploaded file. Defaults to File(...).

        Returns:
            FormData
        """
        return cls(file=file)
    