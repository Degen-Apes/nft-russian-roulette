import json
from json import JSONDecodeError
from typing import Any

from nft_russian_roulette.constants import CONTRACT_JSON_BASE_PATH, Contract
from nft_russian_roulette.exceptions import NFTRRException


def get_contract_abi(contract: Contract) -> dict[str, Any]:
    path = CONTRACT_JSON_BASE_PATH.joinpath(f"{contract.value}.sol", f"{contract.value}.json")

    try:
        return json.loads(path.read_text())["abi"]
    except (JSONDecodeError, KeyError, OSError) as ex:
        raise NFTRRException("Error loading contract ABI") from ex
