from __future__ import annotations
from . import (
    creator,
)
import typing
from dataclasses import dataclass
from construct import Container, Construct
import borsh_construct as borsh


class DataJSON(typing.TypedDict):
    name: str
    symbol: str
    uri: str
    seller_fee_basis_points: int
    creators: typing.Optional[list[creator.CreatorJSON]]


@dataclass
class Data:
    layout: typing.ClassVar = borsh.CStruct(
        "name" / borsh.String,
        "symbol" / borsh.String,
        "uri" / borsh.String,
        "seller_fee_basis_points" / borsh.U16,
        "creators"
        / borsh.Option(borsh.Vec(typing.cast(Construct, creator.Creator.layout))),
    )
    name: str
    symbol: str
    uri: str
    seller_fee_basis_points: int
    creators: typing.Optional[list[creator.Creator]]

    @classmethod
    def from_decoded(cls, obj: Container) -> "Data":
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
        }

    def to_json(self) -> DataJSON:
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
        }

    @classmethod
    def from_json(cls, obj: DataJSON) -> "Data":
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
        )
