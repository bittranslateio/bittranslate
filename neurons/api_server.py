import os
import json
import time

import traceback
from typing import Callable, Awaitable, List, Optional

import bittensor as bt
from bittensor.axon import FastAPIThreadedServer
from fastapi import  APIRouter
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from pyngrok import ngrok
import uvicorn

from neurons.protocol import Translate
from bittranslate import is_api_data_valid

ForwardFn = Callable[[Translate], Awaitable[Translate]]

auth_data = dict()
request_counts = {}


def load_api_config():
    bt.logging.debug("Loading API config")

    try:
        if not os.path.exists("neurons/api.json"):
            raise Exception(f"{'neurons/api.json'} does not exist")

        with open("neurons/api.json", 'r') as file:
            api_data = json.load(file)
            bt.logging.trace("api_data", api_data)

            valid, reason = is_api_data_valid(api_data)
            if not valid:
                raise Exception(f"{'neurons/api.json'} is poorly formatted. {reason}")
            if "change-me" in api_data["keys"]:
                bt.logging.warning("YOU ARE USING THE DEFAULT API KEY. CHANGE IT FOR SECURITY REASONS.")
        return api_data
    except Exception as e:
        bt.logging.error("Error loading API config:", e)
        traceback.print_exc()


async def auth_rate_limiting_middleware(request: Request, call_next):

    # Check if API key is valid
    # TODO use an official "auth key" header 
    # such that programs such as web browsers
    # know to hide this info from JavaScript and other environments.
    auth_api = request.headers.get('auth')
    auth_data = load_api_config()
    time_window = 60

    bt.logging.info("auth_data", auth_data)

    if auth_api not in  auth_data["keys"].keys():
        bt.logging.debug(f"Unauthorized key: {auth_api}")
        return JSONResponse(status_code=401, content={"detail": "Unauthorized",
                                                      "translated_texts": []})

    requests_per_min = auth_data["keys"][auth_api]["requests_per_min"]

    # Rate limiting
    current_time = time.time()
    if auth_api in request_counts:
        requests, start_time = request_counts[auth_api]

        if current_time - start_time > time_window:
            # start a new time period
            request_counts[auth_api] = (1, current_time)
        elif requests < requests_per_min:
            # same time period
            request_counts[auth_api] = (requests + 1, start_time)
        else:
            bt.logging.debug(f"Rate limit exceeded for key: {auth_api}")
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded", "translated_texts": []})
    else:
        request_counts[auth_api] = (1, current_time)

    response = await call_next(request)
    return response

def connect_ngrok_tunnel(local_port: int, domain: str) -> ngrok.NgrokTunnel:
    auth_token = os.environ.get('NGROK_AUTH_TOKEN', None)
    if auth_token is not None:
        ngrok.set_auth_token(auth_token)

    tunnel = ngrok.connect(
        addr=str(local_port),
        proto="http",
        # Domain is required.
        domain=domain
    )
    bt.logging.info(
        f"API is available over NGROK at {tunnel.public_url}"
    )

    return tunnel

class ApiServer:
    app: FastAPI
    fast_server: FastAPIThreadedServer
    router: APIRouter
    forward_fn: ForwardFn
    tunnel: Optional[ngrok.NgrokTunnel]
    ngrok_domain: Optional[str]

    def __init__(
            self, 
            axon_port: int,
            forward_fn: ForwardFn,
            api_json: str,
            lang_pairs: list,
            max_char: int,
            ngrok_domain: Optional[str]
    ):

        self.forward_fn = forward_fn
        self.app = FastAPI()
        self.app.middleware('http')(auth_rate_limiting_middleware)

        self.fast_server = FastAPIThreadedServer(config=uvicorn.Config(
            self.app,
            host="0.0.0.0",
            port=axon_port,
            log_level="trace" if bt.logging.__trace_on__ else "critical"
        ))
        self.router = APIRouter()
        self.router.add_api_route(
            "/translate",
            self.translate,
            methods=["POST"],
        )
        self.app.include_router(self.router)

        self.api_json = api_json

        self.lang_pairs = lang_pairs

        self.max_char = max_char

        self.ngrok_domain = ngrok_domain
        self.tunnel = None

    async def translate(self, request: Translate):
        request_lang_pair = (request.source_lang, request.target_lang)

        if request_lang_pair not in self.lang_pairs:
            return JSONResponse(
                status_code=400, 
                content={
                    "detail": "Invalid language pair", 
                    "translated_texts": []
                }
            )

        for source_text in request.source_texts:
            if len(source_text) > self.max_char :
                return JSONResponse(
                    status_code=400, 
                    content={
                        "detail": (
                            "Source text is too long. "
                            f"Must be under {self.max_char} characters"
                        ), 
                        "translated_texts": []
                    }
                )

        for translated_text in request.translated_texts:
            # also check the length of the translated text for good measure.
            if len(translated_text) > self.max_char:
                return JSONResponse(
                    status_code=400, 
                    content={
                        "detail": (
                            "Translated text is too long. "
                            f"Must be under {self.max_char} characters"
                        ), 
                        "translated_texts": []
                    }
                )

        if len(request.source_texts) > 2:
            return JSONResponse(
                status_code=400,
                content={
                    "detail": (
                        "Batch size for source texts is too large. "
                        "Please set it to <= 2"
                    ), 
                    "translated_texts": []
                }
            )

        response = await self.forward_fn(request)
        bt.logging.debug(f"API: response.translated_texts {response.translated_texts}")
        return JSONResponse(status_code=200,
                            content={"detail": "success", "translated_texts": response.translated_texts})

    def start(self):
        self.fast_server.start()

        if self.ngrok_domain is not None:
            self.tunnel = connect_ngrok_tunnel(
                local_port=self.fast_server.config.port,
                domain=self.ngrok_domain
            )

    def stop(self):
        self.fast_server.stop()

        if self.tunnel is not None:
            ngrok.disconnect(
                public_url=self.tunnel.public_url
            )
            self.tunnel = None




