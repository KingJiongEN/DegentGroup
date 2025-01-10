from __future__ import annotations
import typing
from dataclasses import dataclass
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import EnumForCodegen, BorshPubkey
import borsh_construct as borsh


class V1JSONValue(typing.TypedDict):
    rule_set: typing.Optional[str]


class V1Value(typing.TypedDict):
    rule_set: typing.Optional[Pubkey]


class V1JSON(typing.TypedDict):
    value: V1JSONValue
    kind: typing.Literal["V1"]


@dataclass
class V1:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "V1"
    value: V1Value

    def to_json(self) -> V1JSON:
        return V1JSON(
            kind="V1",
            value={
                "rule_set": (
                    None
                    if self.value["rule_set"] is None
                    else str(self.value["rule_set"])
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "V1": {
                "rule_set": self.value["rule_set"],
            },
        }


ProgrammableConfigKind = typing.Union[V1]
ProgrammableConfigJSON = typing.Union[V1JSON]


def from_decoded(obj: dict) -> ProgrammableConfigKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "V1" in obj:
        val = obj["V1"]
        return V1(
            V1Value(
                rule_set=val["rule_set"],
            )
        )
    raise ValueError("Invalid enum object")


def from_json(obj: ProgrammableConfigJSON) -> ProgrammableConfigKind:
    if obj["kind"] == "V1":
        v1json_value = typing.cast(V1JSONValue, obj["value"])
        return V1(
            V1Value(
                rule_set=(
                    None
                    if v1json_value["rule_set"] is None
                    else Pubkey.from_string(v1json_value["rule_set"])
                ),
            )
        )
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen("V1" / borsh.CStruct("rule_set" / borsh.Option(BorshPubkey)))
