from eth_utils import is_checksum_address
from fastapi import HTTPException, Path
from pydantic import BaseModel, ValidationError, validator

_address_type = Path(
    "0x0000000000000000000000000000000000000000",
    min_length=42,
    max_length=42,
    regex=r"0x[a-fA-F0-9]{40}",
)


class EthAddress(BaseModel):
    address: str = _address_type

    @validator("address")
    def _validate_address(cls, address):
        if not is_checksum_address(address):
            raise ValueError("Address isn't valid EIP-55")
        return address

    @classmethod
    async def depends(cls, address: str = _address_type):
        try:
            return cls(address=address)
        except ValidationError as e:
            for error in e.errors():
                error["loc"] = ["path"] + list(error["loc"])
            raise HTTPException(422, detail=e.errors())
