"""This is the `Main File`. It connects and run all the modules and function together """

# Standard python Imports
import os
import logging
import logging.config
from typing import Optional
import uvicorn

# Fastapi Imports
from fastapi import FastAPI, Request, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from starlette.routing import Mount
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from transformers.utils import logging as transformers_logging
import yaml
from csrf import CsrfSettings

# Imports from Project Directory
from schema import FormData
from app_files.model_processor_caller import ModelProcessorCaller
from app_files.main_processor import MainProcessor


# Loading Log YAML file
with open('log_config.yaml', 'r', encoding='UTF-8') as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)

# Setting transformer verbosity level
transformers_logging.set_verbosity_error()

logging.info("Main Files Loading....")

# Call Model Processor
try:
    model, processor = ModelProcessorCaller()()
    logging.info("Model and Processor Loaded")
except ImportError as imp_err:
    logging.error("Exception encountered in ModelProcessorCaller(): %s", imp_err)

routes = [
    Mount('/static', StaticFiles(directory='static'), name='static'),
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=[
               '*'], allow_methods=["*"], allow_headers=["*"])
]

app = FastAPI(routes=routes, middleware=middleware, docs_url=None, redoc_url=None)
logging.info("App initialized")


templates = Jinja2Templates(directory='templates')
logging.info("Templates initialized")


# csrf protect
@CsrfProtect.load_config
def get_csrf_config():
    """Load the csrf config

    Returns:
        CsrfSettings: Holds the secret token
    """
    return CsrfSettings()


logging.info("CsrfProtect config loaded")

logging.info("Main Files Loading Complete")


@app.get('/', response_class=HTMLResponse, name='homepage')
async def get_main_data(request: Request,
                        csrf_protect: CsrfProtect = Depends(),
                        msg: Optional[str] = None,
                        result: Optional[str] = None):
    """GET Template Response

    Args:
        request (Request): Request
        csrf_protect (CsrfProtect): CsrProtection. Defaults to Depends().

    Returns:
        _TemplateResponse: A template response
    """
    if msg:
        response = templates.TemplateResponse('home.html', {'request': request, 'msg': msg})
    elif result:
        response = templates.TemplateResponse('home.html', {'request': request, 'result': result})
    else:
        response = templates.TemplateResponse('home.html', {'request': request})
    # Generate csrf token
    csrf_protect.set_csrf_cookie(response)
    return response


@app.post('/', response_model=FormData, name='homepage_post')
async def post_main_data(request: Request,
                         file: FormData = Depends(FormData.as_form),
                         csrf_protect: CsrfProtect = Depends()):
    """POST Request

    Args:
        request (Request): Request
        file (FormData): Form Data. Defaults to Depends(FormData.as_form).
        csrf_protect (CsrfProtect): Csrf Protection. Defaults to Depends().

    Returns:
        TemplateResponse: A template response
    """
    # Validate csrf token
    csrf_protect.validate_csrf_in_cookies(request)

    # If there is no Validation Error
    if not isinstance(file.file, ValueError):
        try:
            # Read the uploaded file
            content = await file.file.read()
            logging.info("%s uploaded successfully", file.file.filename)
        except OSError as os_err:
            logging.error("Error in reading file: %s", os_err)
            return RedirectResponse(app.url_path_for(name='homepage') + '?msg=' + str(os_err),
                                    status_code=status.HTTP_302_FOUND)

        file_extension = os.path.splitext(file.file.filename)[1]
        # If file exists delete it
        try:
            if os.path.exists(os.path.join("temp", "temp" + file_extension)):
                os.remove(os.path.join("temp", "temp" + file_extension))
                logging.info("temp%s removed", file_extension)
        except OSError as os_remove_err:
            logging.error("Error in removing file: %s", os_remove_err)
            return RedirectResponse(app.url_path_for(name='homepage')
                                    + '?msg='
                                    + str(os_remove_err),
                                    status_code=status.HTTP_302_FOUND)

        # Write the content as .wav
        try:
            with open(os.path.join("temp", "temp" + file_extension), 'bx') as temp_file:
                temp_file.write(content)
                logging.info("Content written to temp%s", file_extension)
        except OSError as os_open_err:
            logging.error("Error in opening and writing to file: %s", os_open_err)
            return RedirectResponse(app.url_path_for(name='homepage') + '?msg=' + str(os_open_err),
                                    status_code=status.HTTP_302_FOUND)

        # Call MainProcessor
        transcriptions = MainProcessor(os.path.join("temp", "temp" + file_extension),
                                       model, processor)()
        logging.info("Speech Decoded to Text")

        return RedirectResponse(app.url_path_for(name='homepage')
                                + '?result=' + str(transcriptions[0]),
                                status_code=status.HTTP_303_SEE_OTHER)

    # If there is validation Error
    logging.error("Validation Error")
    return RedirectResponse(app.url_path_for(name='homepage') + '?msg=' + str(file.file),
                            status_code=status.HTTP_302_FOUND)


@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(exc: CsrfProtectError):
    """Exception Handler for Csrf

    Args:
        request (Request): Request
        exc (CsrfProtectError): Csrf Protection

    Returns:
        _TemplateResponse: A template response
    """
    logging.error("Csrf Exception Encountered: %s", str(exc.message))
    return RedirectResponse(app.url_path_for(name='homepage') + '?msg=' + str(exc.message),
                            status_code=status.HTTP_302_FOUND)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    """Handles any HTTP Exception

    Returns:
        RedirectResponse
    """
    logging.error("Invalid URL entered: %s, with detail %s and status code %s",
                  str(request),
                  str(exc.detail),
                  str(exc.status_code))
    return RedirectResponse("/")


if __name__ == "__main__":
    # Loading Env file
    ENV_PATH = '.env'

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True,
                env_file=ENV_PATH)
