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
