import json
import os
from json import JSONDecodeError
from typing import Any

from nft_russian_roulette.constants import CONTRACT_JSON_BASE_PATH, Contract
from nft_russian_roulette.exceptions import NFTRRException
from redis import Redis


def get_contract_abi(contract: Contract) -> dict[str, Any]:
    path = CONTRACT_JSON_BASE_PATH.joinpath(f"{contract.value}.sol", f"{contract.value}.json")

    try:
        return json.loads(path.read_text())["abi"]
    except (JSONDecodeError, KeyError, OSError) as ex:
        raise NFTRRException("Error loading contract ABI") from ex


def get_redis_from_env() -> Redis:
    return Redis(
        host=os.environ.get("NFTRR_REDIS_HOST", "localhost"),
        port=int(os.environ.get("NFTRR_REDIS_PORT", 6379)),
    )
