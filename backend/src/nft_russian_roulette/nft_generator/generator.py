from eth_typing import Address
from nft_russian_roulette.constants import SURVIVED_TAG_REDIS_KEY_TEMPLATE
from nft_russian_roulette.utils import get_redis_from_env
from structlog import get_logger

log = get_logger(__name__)


def generate_gravestone(game_id: int, token_contract_address: Address, token_id: int) -> None:
    log.info(
        "Generating Gravestone",
        game_id=game_id,
        token_contract_address=token_contract_address,
        token_id=token_id,
    )
    redis = get_redis_from_env()
    redis.hset()


def generate_or_update_tag(game_id: int, token_contract_address: Address, token_id: int) -> None:
    log.info(
        "Generating tag",
        game_id=game_id,
        token_contract_address=token_contract_address,
        token_id=token_id,
    )
    redis = get_redis_from_env()

    survived_count_key = SURVIVED_TAG_REDIS_KEY_TEMPLATE.format(
        token_contract_address=token_contract_address, token_id=token_id
    )
    redis.incr(survived_count_key)
