from __future__ import annotations
from . import (
    collection,
    creator,
    uses,
)
import typing
from dataclasses import dataclass
from construct import Container, Construct
import borsh_construct as borsh


class DataV2JSON(typing.TypedDict):
    name: str
    symbol: str
    uri: str
    seller_fee_basis_points: int
    creators: typing.Optional[list[creator.CreatorJSON]]
    collection: typing.Optional[collection.CollectionJSON]
    uses: typing.Optional[uses.UsesJSON]


@dataclass
class DataV2:
    layout: typing.ClassVar = borsh.CStruct(
        "name" / borsh.String,
        "symbol" / borsh.String,
        "uri" / borsh.String,
        "seller_fee_basis_points" / borsh.U16,
        "creators"
        / borsh.Option(borsh.Vec(typing.cast(Construct, creator.Creator.layout))),
        "collection" / borsh.Option(collection.Collection.layout),
        "uses" / borsh.Option(uses.Uses.layout),
    )
    name: str
    symbol: str
    uri: str
    seller_fee_basis_points: int
    creators: typing.Optional[list[creator.Creator]]
    collection: typing.Optional[collection.Collection]
    uses: typing.Optional[uses.Uses]

    @classmethod
    def from_decoded(cls, obj: Container) -> "DataV2":
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
            collection=(
                None
                if obj.collection is None
                else collection.Collection.from_decoded(obj.collection)
            ),
            uses=(None if obj.uses is None else uses.Uses.from_decoded(obj.uses)),
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
            "collection": (
                None if self.collection is None else self.collection.to_encodable()
            ),
            "uses": (None if self.uses is None else self.uses.to_encodable()),
        }

    def to_json(self) -> DataV2JSON:
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
            "collection": (
                None if self.collection is None else self.collection.to_json()
            ),
            "uses": (None if self.uses is None else self.uses.to_json()),
        }

    @classmethod
    def from_json(cls, obj: DataV2JSON) -> "DataV2":
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
            collection=(
                None
                if obj["collection"] is None
                else collection.Collection.from_json(obj["collection"])
            ),
            uses=(None if obj["uses"] is None else uses.Uses.from_json(obj["uses"])),
        )
