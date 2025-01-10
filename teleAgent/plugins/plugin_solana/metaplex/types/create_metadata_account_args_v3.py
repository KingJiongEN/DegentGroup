from __future__ import annotations
from . import (
    data_v2,
    collection_details,
)
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class CreateMetadataAccountArgsV3JSON(typing.TypedDict):
    data: data_v2.DataV2JSON
    is_mutable: bool
    collection_details: typing.Optional[collection_details.CollectionDetailsJSON]


@dataclass
class CreateMetadataAccountArgsV3:
    layout: typing.ClassVar = borsh.CStruct(
        "data" / data_v2.DataV2.layout,
        "is_mutable" / borsh.Bool,
        "collection_details" / borsh.Option(collection_details.layout),
    )
    data: data_v2.DataV2
    is_mutable: bool
    collection_details: typing.Optional[collection_details.CollectionDetailsKind]

    @classmethod
    def from_decoded(cls, obj: Container) -> "CreateMetadataAccountArgsV3":
        return cls(
            data=data_v2.DataV2.from_decoded(obj.data),
            is_mutable=obj.is_mutable,
            collection_details=(
                None
                if obj.collection_details is None
                else collection_details.from_decoded(obj.collection_details)
            ),
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "data": self.data.to_encodable(),
            "is_mutable": self.is_mutable,
            "collection_details": (
                None
                if self.collection_details is None
                else self.collection_details.to_encodable()
            ),
        }

    def to_json(self) -> CreateMetadataAccountArgsV3JSON:
        return {
            "data": self.data.to_json(),
            "is_mutable": self.is_mutable,
            "collection_details": (
                None
                if self.collection_details is None
                else self.collection_details.to_json()
            ),
        }

    @classmethod
    def from_json(
        cls, obj: CreateMetadataAccountArgsV3JSON
    ) -> "CreateMetadataAccountArgsV3":
        return cls(
            data=data_v2.DataV2.from_json(obj["data"]),
            is_mutable=obj["is_mutable"],
            collection_details=(
                None
                if obj["collection_details"] is None
                else collection_details.from_json(obj["collection_details"])
            ),
        )
