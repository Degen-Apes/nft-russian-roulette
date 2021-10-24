import time
from typing import Any

from eth_typing import Address
from nft_russian_roulette.constants import ROULETTE_TRIGGER_EVENT
from nft_russian_roulette.nft_generator.generator import (
    generate_gravestone, generate_or_update_tag)
from rq import Queue
from structlog import get_logger
from web3 import Web3
from web3._utils.filters import Filter
from web3.types import LogReceipt

log = get_logger(__name__)


class Watcher:
    def __init__(
        self,
        web3: Web3,
        contract_address: Address,
        contract_abi: dict[str, Any],
        queue: Queue,
    ) -> None:
        self.web3 = web3
        self.queue = queue
        self.contract = web3.eth.contract(abi=contract_abi, address=contract_address)

    def watch_forever(self):
        filter: Filter = getattr(self.contract.events, ROULETTE_TRIGGER_EVENT).createFilter(
            fromBlock=0
        )
        while True:
            entries = filter.get_new_entries()
            log.info("Querying filter", type=ROULETTE_TRIGGER_EVENT, entries=len(entries))
            if entries:
                self.handle_results(entries)
            time.sleep(3)

    def handle_results(self, reciepts: list[LogReceipt]) -> None:
        for reciept in reciepts:
            if reciept.args.survived:
                log.info("Survived", game_id=reciept.args.gameId)
                self.queue.enqueue(
                    generate_or_update_tag,
                    game_id=reciept.args.gameId,
                    token_contract_address=reciept.args.tokenContract,
                    token_id=reciept.args.tokenId,
                )
            else:
                log.info("Died", game_id=reciept.args.gameId)
                self.queue.enqueue(
                    generate_gravestone,
                    game_id=reciept.args.gameId,
                    token_contract_address=reciept.args.tokenContract,
                    token_id=reciept.args.tokenId,
                )
