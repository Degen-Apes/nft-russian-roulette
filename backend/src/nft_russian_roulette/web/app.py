from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Path
from nft_russian_roulette.constants import (GRAVESTONE_REDIS_KEY_TEMPLATE,
                                            IMAGE_GRAVESTONE_PATH,
                                            IMAGE_SURVIVED_PATH,
                                            SURVIVED_TAG_REDIS_KEY_TEMPLATE)
from nft_russian_roulette.utils import get_redis_from_env
from nft_russian_roulette.web.models import EthAddress
from redis import Redis
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response
from structlog import get_logger

log = get_logger(__name__)

_REDIS: Optional[Redis] = None


def get_redis() -> Redis:
    global _REDIS
    if _REDIS is None:
        _REDIS = get_redis_from_env()
    return _REDIS


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def index():
    return """<html><body><h1>NFT Russian Roulette</h1><p><a href="/docs">API docs</a>"""


@app.get("/tag/{address}/{token_id}")
def nftag(
    address: EthAddress = Depends(EthAddress.depends),
    token_id: str = Path(...),
    request: Request = ...,
):
    redis = get_redis()
    survived_count_key = SURVIVED_TAG_REDIS_KEY_TEMPLATE.format(
        token_contract_address=address.address, token_id=token_id
    )
    survived_count = redis.get(survived_count_key)

    log.debug(
        "Survived count", token_address=address.address, token_id=token_id, count=survived_count
    )

    if not survived_count:
        raise HTTPException(status_code=404, detail="Nothing found")

    return {
        "description": "NFT Russian Roulette Survivor",
        "image": f"{request.url.scheme}://{request.url.netloc}/image/survived",
        "name": f"NFTRR Survivor {address.address}:{token_id}",
        "attributes": [
            {
                "display_type": "number",
                "trait_type": "Rounds Survived",
                "value": redis.get(survived_count_key),
            }
        ],
    }


@app.get("/gravestone/{token_id}")
def gravestone(token_id: str = Path(...), request: Request = ...):
    redis = get_redis()
    gravestone_key = GRAVESTONE_REDIS_KEY_TEMPLATE.format(gravestone_id=token_id)
    gravestone = redis.hgetall(gravestone_key)
    if not gravestone:
        raise HTTPException(status_code=404, detail="Gravestone doesn't exist")
    return {
        "description": "NFT Russian Roulette Gravestone",
        "image": f"{request.url.scheme}://{request.url.netloc}/image/gravestone",
        "name": f"NFTRR Gravestone for {gravestone[b'token_contract_address']}:{gravestone[b'token_id']}",
        "attributes": [],
    }


@app.get("/image/{kind}")
def image_survived(kind: str):
    if kind == "survived":
        image = IMAGE_SURVIVED_PATH.read_bytes()
    elif kind == "gravestone":
        image = IMAGE_GRAVESTONE_PATH.read_bytes()
    else:
        raise HTTPException(status_code=404)
    return Response(image, media_type="image/png")
