import traceback

import click
from eth_utils import to_checksum_address
from nft_russian_roulette.chain_watcher.watcher import Watcher
from nft_russian_roulette.constants import Contract
from nft_russian_roulette.exceptions import NFTRRException
from nft_russian_roulette.utils import get_contract_abi
from redis import Redis
from rq import Queue
from structlog import get_logger
from web3 import Web3, WebsocketProvider

log = get_logger(__name__)


@click.command()
@click.option("--contract-address", required=True, help="Address of the deployed contract")
@click.option("--web3-ws-url", required=True, help="Web3 WS URL")
@click.option("--redis-host", default="localhost")
@click.option("--redis-port", default=6379)
@click.option("--redis-db", default=0)
@click.option("-v", "--verbose", is_flag=True)
def main(
    contract_address: str,
    web3_ws_url: str,
    redis_host: str,
    redis_port: int,
    redis_db: int,
    verbose: bool = False,
):
    redis = Redis(host=redis_host, port=redis_port, db=redis_db)
    redis.flushall()
    try:
        web3 = Web3(WebsocketProvider(web3_ws_url))
        watcher = Watcher(
            web3=web3,
            contract_address=to_checksum_address(contract_address),
            contract_abi=get_contract_abi(Contract.ROULETTE),
            queue=Queue(connection=redis),
        )
        watcher.watch_forever()
    except NFTRRException as ex:
        if verbose:
            traceback.print_exc()
        else:
            click.secho(str(ex), fg="red")
        exit(1)
