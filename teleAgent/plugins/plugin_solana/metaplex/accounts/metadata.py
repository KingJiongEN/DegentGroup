import typing
from dataclasses import dataclass
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
import borsh_construct as borsh
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from anchorpy.borsh_extension import BorshPubkey
from ..program_id import PROGRAM_ID
from .. import types


class MetadataJSON(typing.TypedDict):
    key: types.key.KeyJSON
    update_authority: str
    mint: str
    data: types.data.DataJSON
    primary_sale_happened: bool
    is_mutable: bool
    edition_nonce: typing.Optional[int]
    token_standard: typing.Optional[types.token_standard.TokenStandardJSON]
    collection: typing.Optional[types.collection.CollectionJSON]
    uses: typing.Optional[types.uses.UsesJSON]
    collection_details: typing.Optional[types.collection_details.CollectionDetailsJSON]
    programmable_config: typing.Optional[
        types.programmable_config.ProgrammableConfigJSON
    ]


@dataclass
class Metadata:
    discriminator: typing.ClassVar = b"H\x0by\x1ao\xb5U]"
    layout: typing.ClassVar = borsh.CStruct(
        "key" / types.key.layout,
        "update_authority" / BorshPubkey,
        "mint" / BorshPubkey,
        "data" / types.data.Data.layout,
        "primary_sale_happened" / borsh.Bool,
        "is_mutable" / borsh.Bool,
        "edition_nonce" / borsh.Option(borsh.U8),
        "token_standard" / borsh.Option(types.token_standard.layout),
        "collection" / borsh.Option(types.collection.Collection.layout),
        "uses" / borsh.Option(types.uses.Uses.layout),
        "collection_details" / borsh.Option(types.collection_details.layout),
        "programmable_config" / borsh.Option(types.programmable_config.layout),
    )
    key: types.key.KeyKind
    update_authority: Pubkey
    mint: Pubkey
    data: types.data.Data
    primary_sale_happened: bool
    is_mutable: bool
    edition_nonce: typing.Optional[int]
    token_standard: typing.Optional[types.token_standard.TokenStandardKind]
    collection: typing.Optional[types.collection.Collection]
    uses: typing.Optional[types.uses.Uses]
    collection_details: typing.Optional[types.collection_details.CollectionDetailsKind]
    programmable_config: typing.Optional[
        types.programmable_config.ProgrammableConfigKind
    ]

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["Metadata"]:
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
    ) -> typing.List[typing.Optional["Metadata"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["Metadata"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "Metadata":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = Metadata.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            key=types.key.from_decoded(dec.key),
            update_authority=dec.update_authority,
            mint=dec.mint,
            data=types.data.Data.from_decoded(dec.data),
            primary_sale_happened=dec.primary_sale_happened,
            is_mutable=dec.is_mutable,
            edition_nonce=dec.edition_nonce,
            token_standard=(
                None
                if dec.token_standard is None
                else types.token_standard.from_decoded(dec.token_standard)
            ),
            collection=(
                None
                if dec.collection is None
                else types.collection.Collection.from_decoded(dec.collection)
            ),
            uses=(None if dec.uses is None else types.uses.Uses.from_decoded(dec.uses)),
            collection_details=(
                None
                if dec.collection_details is None
                else types.collection_details.from_decoded(dec.collection_details)
            ),
            programmable_config=(
                None
                if dec.programmable_config is None
                else types.programmable_config.from_decoded(dec.programmable_config)
            ),
        )

    def to_json(self) -> MetadataJSON:
        return {
            "key": self.key.to_json(),
            "update_authority": str(self.update_authority),
            "mint": str(self.mint),
            "data": self.data.to_json(),
            "primary_sale_happened": self.primary_sale_happened,
            "is_mutable": self.is_mutable,
            "edition_nonce": self.edition_nonce,
            "token_standard": (
                None if self.token_standard is None else self.token_standard.to_json()
            ),
            "collection": (
                None if self.collection is None else self.collection.to_json()
            ),
            "uses": (None if self.uses is None else self.uses.to_json()),
            "collection_details": (
                None
                if self.collection_details is None
                else self.collection_details.to_json()
            ),
            "programmable_config": (
                None
                if self.programmable_config is None
                else self.programmable_config.to_json()
            ),
        }

    @classmethod
    def from_json(cls, obj: MetadataJSON) -> "Metadata":
        return cls(
            key=types.key.from_json(obj["key"]),
            update_authority=Pubkey.from_string(obj["update_authority"]),
            mint=Pubkey.from_string(obj["mint"]),
            data=types.data.Data.from_json(obj["data"]),
            primary_sale_happened=obj["primary_sale_happened"],
            is_mutable=obj["is_mutable"],
            edition_nonce=obj["edition_nonce"],
            token_standard=(
                None
                if obj["token_standard"] is None
                else types.token_standard.from_json(obj["token_standard"])
            ),
            collection=(
                None
                if obj["collection"] is None
                else types.collection.Collection.from_json(obj["collection"])
            ),
            uses=(
                None if obj["uses"] is None else types.uses.Uses.from_json(obj["uses"])
            ),
            collection_details=(
                None
                if obj["collection_details"] is None
                else types.collection_details.from_json(obj["collection_details"])
            ),
            programmable_config=(
                None
                if obj["programmable_config"] is None
                else types.programmable_config.from_json(obj["programmable_config"])
            ),
        )
