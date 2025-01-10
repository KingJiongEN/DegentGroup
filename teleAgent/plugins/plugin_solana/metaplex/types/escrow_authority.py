from __future__ import annotations
import typing
from dataclasses import dataclass
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import EnumForCodegen, BorshPubkey
import borsh_construct as borsh

CreatorJSONValue = tuple[str]
CreatorValue = tuple[Pubkey]


class TokenOwnerJSON(typing.TypedDict):
    kind: typing.Literal["TokenOwner"]


class CreatorJSON(typing.TypedDict):
    value: CreatorJSONValue
    kind: typing.Literal["Creator"]


@dataclass
class TokenOwner:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "TokenOwner"

    @classmethod
    def to_json(cls) -> TokenOwnerJSON:
        return TokenOwnerJSON(
            kind="TokenOwner",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "TokenOwner": {},
        }


@dataclass
class Creator:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Creator"
    value: CreatorValue

    def to_json(self) -> CreatorJSON:
        return CreatorJSON(
            kind="Creator",
            value=(str(self.value[0]),),
        )

    def to_encodable(self) -> dict:
        return {
            "Creator": {
                "item_0": self.value[0],
            },
        }


EscrowAuthorityKind = typing.Union[TokenOwner, Creator]
EscrowAuthorityJSON = typing.Union[TokenOwnerJSON, CreatorJSON]


def from_decoded(obj: dict) -> EscrowAuthorityKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "TokenOwner" in obj:
        return TokenOwner()
    if "Creator" in obj:
        val = obj["Creator"]
        return Creator((val["item_0"],))
    raise ValueError("Invalid enum object")


def from_json(obj: EscrowAuthorityJSON) -> EscrowAuthorityKind:
    if obj["kind"] == "TokenOwner":
        return TokenOwner()
    if obj["kind"] == "Creator":
        creator_json_value = typing.cast(CreatorJSONValue, obj["value"])
        return Creator((Pubkey.from_string(creator_json_value[0]),))
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "TokenOwner" / borsh.CStruct(), "Creator" / borsh.CStruct("item_0" / BorshPubkey)
)
