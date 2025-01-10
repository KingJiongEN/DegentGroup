from __future__ import annotations
from . import (
    collection,
    creator,
    uses,
    token_standard,
    collection_details,
)
import typing
from dataclasses import dataclass
from construct import Container, Construct
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class AssetDataJSON(typing.TypedDict):
    name: str
    symbol: str
    uri: str
    seller_fee_basis_points: int
    creators: typing.Optional[list[creator.CreatorJSON]]
    primary_sale_happened: bool
    is_mutable: bool
    token_standard: token_standard.TokenStandardJSON
    collection: typing.Optional[collection.CollectionJSON]
    uses: typing.Optional[uses.UsesJSON]
    collection_details: typing.Optional[collection_details.CollectionDetailsJSON]
    rule_set: typing.Optional[str]


@dataclass
class AssetData:
    layout: typing.ClassVar = borsh.CStruct(
        "name" / borsh.String,
        "symbol" / borsh.String,
        "uri" / borsh.String,
        "seller_fee_basis_points" / borsh.U16,
        "creators"
        / borsh.Option(borsh.Vec(typing.cast(Construct, creator.Creator.layout))),
        "primary_sale_happened" / borsh.Bool,
        "is_mutable" / borsh.Bool,
        "token_standard" / token_standard.layout,
        "collection" / borsh.Option(collection.Collection.layout),
        "uses" / borsh.Option(uses.Uses.layout),
        "collection_details" / borsh.Option(collection_details.layout),
        "rule_set" / borsh.Option(BorshPubkey),
    )
    name: str
    symbol: str
    uri: str
    seller_fee_basis_points: int
    creators: typing.Optional[list[creator.Creator]]
    primary_sale_happened: bool
    is_mutable: bool
    token_standard: token_standard.TokenStandardKind
    collection: typing.Optional[collection.Collection]
    uses: typing.Optional[uses.Uses]
    collection_details: typing.Optional[collection_details.CollectionDetailsKind]
    rule_set: typing.Optional[Pubkey]

    @classmethod
    def from_decoded(cls, obj: Container) -> "AssetData":
        return cls(
            name=obj.name,
            symbol=obj.symbol,
            uri=obj.uri,
            seller_fee_basis_points=obj.seller_fee_basis_points,
            creators=(
                None
                if obj.creators is None
                else list(
                    map(lambda item: creator.Creator.from_decoded(item), obj.creators)
                )
            ),
            primary_sale_happened=obj.primary_sale_happened,
            is_mutable=obj.is_mutable,
            token_standard=token_standard.from_decoded(obj.token_standard),
            collection=(
                None
                if obj.collection is None
                else collection.Collection.from_decoded(obj.collection)
            ),
            uses=(None if obj.uses is None else uses.Uses.from_decoded(obj.uses)),
            collection_details=(
                None
                if obj.collection_details is None
                else collection_details.from_decoded(obj.collection_details)
            ),
            rule_set=obj.rule_set,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "name": self.name,
            "symbol": self.symbol,
            "uri": self.uri,
            "seller_fee_basis_points": self.seller_fee_basis_points,
            "creators": (
                None
                if self.creators is None
                else list(map(lambda item: item.to_encodable(), self.creators))
            ),
            "primary_sale_happened": self.primary_sale_happened,
            "is_mutable": self.is_mutable,
            "token_standard": self.token_standard.to_encodable(),
            "collection": (
                None if self.collection is None else self.collection.to_encodable()
            ),
            "uses": (None if self.uses is None else self.uses.to_encodable()),
            "collection_details": (
                None
                if self.collection_details is None
                else self.collection_details.to_encodable()
            ),
            "rule_set": self.rule_set,
        }

    def to_json(self) -> AssetDataJSON:
        return {
            "name": self.name,
            "symbol": self.symbol,
            "uri": self.uri,
            "seller_fee_basis_points": self.seller_fee_basis_points,
            "creators": (
                None
                if self.creators is None
                else list(map(lambda item: item.to_json(), self.creators))
            ),
            "primary_sale_happened": self.primary_sale_happened,
            "is_mutable": self.is_mutable,
            "token_standard": self.token_standard.to_json(),
            "collection": (
                None if self.collection is None else self.collection.to_json()
            ),
            "uses": (None if self.uses is None else self.uses.to_json()),
            "collection_details": (
                None
                if self.collection_details is None
                else self.collection_details.to_json()
            ),
            "rule_set": (None if self.rule_set is None else str(self.rule_set)),
        }

    @classmethod
    def from_json(cls, obj: AssetDataJSON) -> "AssetData":
        return cls(
            name=obj["name"],
            symbol=obj["symbol"],
            uri=obj["uri"],
            seller_fee_basis_points=obj["seller_fee_basis_points"],
            creators=(
                None
                if obj["creators"] is None
                else list(
                    map(lambda item: creator.Creator.from_json(item), obj["creators"])
                )
            ),
            primary_sale_happened=obj["primary_sale_happened"],
            is_mutable=obj["is_mutable"],
            token_standard=token_standard.from_json(obj["token_standard"]),
            collection=(
                None
                if obj["collection"] is None
                else collection.Collection.from_json(obj["collection"])
            ),
            uses=(None if obj["uses"] is None else uses.Uses.from_json(obj["uses"])),
            collection_details=(
                None
                if obj["collection_details"] is None
                else collection_details.from_json(obj["collection_details"])
            ),
            rule_set=(
                None if obj["rule_set"] is None else Pubkey.from_string(obj["rule_set"])
            ),
        )
