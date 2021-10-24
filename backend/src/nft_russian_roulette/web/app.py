from fastapi import Depends, FastAPI, Path
from nft_russian_roulette.web.models import EthAddress
from starlette.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def index():
    return """<html><body><h1>NFT Russian Roulette</h1><p><a href="/docs">API docs</a>"""


@app.get("/tag/{address}/{token_id}")
def metadata(address: EthAddress = Depends(EthAddress.depends), token_id: str = Path(...)):
    return {"nft_contract": address.address, "token_id": token_id}
