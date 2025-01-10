import typing
from dataclasses import dataclass
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from ..program_id import PROGRAM_ID
from .. import types


class MasterEditionV2JSON(typing.TypedDict):
    key: types.key.KeyJSON
    supply: int
    max_supply: typing.Optional[int]


@dataclass
class MasterEditionV2:
    discriminator: typing.ClassVar = b"e;\xa3\xcf\xee\x10\xaa\x9f"
    layout: typing.ClassVar = borsh.CStruct(
        "key" / types.key.layout,
        "supply" / borsh.U64,
        "max_supply" / borsh.Option(borsh.U64),
    )
    key: types.key.KeyKind
    supply: int
    max_supply: typing.Optional[int]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["MasterEditionV2"]:
        resp = await conn.get_account_info(address, commitment=commitment)
        info = resp.value
        if info is None:
            return None
        if info.owner != program_id:
            raise ValueError("Account does not belong to this program")
        bytes_data = info.data
        return cls.decode(bytes_data)

    @classmethod
    async def fetch_multiple(
        cls,
        conn: AsyncClient,
        addresses: list[Pubkey],
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.List[typing.Optional["MasterEditionV2"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["MasterEditionV2"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "MasterEditionV2":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = MasterEditionV2.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            key=types.key.from_decoded(dec.key),
            supply=dec.supply,
            max_supply=dec.max_supply,
        )

    def to_json(self) -> MasterEditionV2JSON:
        return {
            "key": self.key.to_json(),
            "supply": self.supply,
            "max_supply": self.max_supply,
        }

    @classmethod
    def from_json(cls, obj: MasterEditionV2JSON) -> "MasterEditionV2":
        return cls(
            key=types.key.from_json(obj["key"]),
            supply=obj["supply"],
            max_supply=obj["max_supply"],
        )
