from enum import Enum
from pathlib import Path


class Contract(Enum):
    ROULETTE = "Roulette"
    GRAVESTONE = "Gravestone"
    RouletteNFTag = "RouletteNFTag"


CONTRACT_JSON_BASE_PATH = (
    Path(__file__)
    .parent.parent.parent.parent.joinpath(
        "contracts",
        "artifacts",
        "contracts",
    )
    .resolve()
)


ROULETTE_TRIGGER_EVENT = "PulledTrigger"

SURVIVED_TAG_REDIS_KEY_TEMPLATE = "survived:{token_contract_address}:{token_id}"
GRAVESTONE_REDIS_KEY_TEMPLATE = "gravestone:{gravestone_id}"

IMAGE_SURVIVED_PATH = Path(__file__).parent.joinpath("images", "survived.png")
IMAGE_GRAVESTONE_PATH = Path(__file__).parent.joinpath("images", "gravestone.png")
