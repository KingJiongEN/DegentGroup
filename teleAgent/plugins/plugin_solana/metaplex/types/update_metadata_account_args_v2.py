from __future__ import annotations
from . import (
    data_v2,
)
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class UpdateMetadataAccountArgsV2JSON(typing.TypedDict):
    data: typing.Optional[data_v2.DataV2JSON]
    update_authority: typing.Optional[str]
    primary_sale_happened: typing.Optional[bool]
    is_mutable: typing.Optional[bool]


@dataclass
class UpdateMetadataAccountArgsV2:
    layout: typing.ClassVar = borsh.CStruct(
        "data" / borsh.Option(data_v2.DataV2.layout),
        "update_authority" / borsh.Option(BorshPubkey),
        "primary_sale_happened" / borsh.Option(borsh.Bool),
        "is_mutable" / borsh.Option(borsh.Bool),
    )
    data: typing.Optional[data_v2.DataV2]
    update_authority: typing.Optional[Pubkey]
    primary_sale_happened: typing.Optional[bool]
    is_mutable: typing.Optional[bool]

    @classmethod
    def from_decoded(cls, obj: Container) -> "UpdateMetadataAccountArgsV2":
        return cls(
            data=(None if obj.data is None else data_v2.DataV2.from_decoded(obj.data)),
            update_authority=obj.update_authority,
            primary_sale_happened=obj.primary_sale_happened,
            is_mutable=obj.is_mutable,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "data": (None if self.data is None else self.data.to_encodable()),
            "update_authority": self.update_authority,
            "primary_sale_happened": self.primary_sale_happened,
            "is_mutable": self.is_mutable,
        }

    def to_json(self) -> UpdateMetadataAccountArgsV2JSON:
        return {
            "data": (None if self.data is None else self.data.to_json()),
            "update_authority": (
                None if self.update_authority is None else str(self.update_authority)
            ),
            "primary_sale_happened": self.primary_sale_happened,
            "is_mutable": self.is_mutable,
        }

    @classmethod
    def from_json(
        cls, obj: UpdateMetadataAccountArgsV2JSON
    ) -> "UpdateMetadataAccountArgsV2":
        return cls(
            data=(
                None if obj["data"] is None else data_v2.DataV2.from_json(obj["data"])
            ),
            update_authority=(
                None
                if obj["update_authority"] is None
                else Pubkey.from_string(obj["update_authority"])
            ),
            primary_sale_happened=obj["primary_sale_happened"],
            is_mutable=obj["is_mutable"],
        )
