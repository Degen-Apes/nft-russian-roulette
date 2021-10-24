from eth_typing import Address
from structlog import get_logger

log = get_logger(__name__)


def generate_gravestone(game_id: int, token_contract_address: Address, token_id: int) -> None:
    log.info(
        "Generating Gravestone",
        game_id=game_id,
        token_contract_address=token_contract_address,
        token_id=token_id,
    )


def generate_or_update_tag(game_id: int, token_contract_address: Address, token_id: int) -> None:
    log.info(
        "Generating tag",
        game_id=game_id,
        token_contract_address=token_contract_address,
        token_id=token_id,
    )
