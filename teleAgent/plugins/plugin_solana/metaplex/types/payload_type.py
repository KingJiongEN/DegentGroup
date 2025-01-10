from __future__ import annotations
from . import (
    seeds_vec,
    proof_info,
)
import typing
from dataclasses import dataclass
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import EnumForCodegen, BorshPubkey
import borsh_construct as borsh

PubkeyJSONValue = tuple[str]
SeedsJSONValue = tuple[seeds_vec.SeedsVecJSON]
MerkleProofJSONValue = tuple[proof_info.ProofInfoJSON]
NumberJSONValue = tuple[int]
PubkeyValue = tuple[Pubkey]
SeedsValue = tuple[seeds_vec.SeedsVec]
MerkleProofValue = tuple[proof_info.ProofInfo]
NumberValue = tuple[int]


class PubkeyJSON(typing.TypedDict):
    value: PubkeyJSONValue
    kind: typing.Literal["Pubkey"]


class SeedsJSON(typing.TypedDict):
    value: SeedsJSONValue
    kind: typing.Literal["Seeds"]


class MerkleProofJSON(typing.TypedDict):
    value: MerkleProofJSONValue
    kind: typing.Literal["MerkleProof"]


class NumberJSON(typing.TypedDict):
    value: NumberJSONValue
    kind: typing.Literal["Number"]


@dataclass
class Pubkey:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Pubkey"
    value: PubkeyValue

    def to_json(self) -> PubkeyJSON:
        return PubkeyJSON(
            kind="Pubkey",
            value=(str(self.value[0]),),
        )

    def to_encodable(self) -> dict:
        return {
            "Pubkey": {
                "item_0": self.value[0],
            },
        }


@dataclass
class Seeds:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Seeds"
    value: SeedsValue

    def to_json(self) -> SeedsJSON:
        return SeedsJSON(
            kind="Seeds",
            value=(self.value[0].to_json(),),
        )

    def to_encodable(self) -> dict:
        return {
            "Seeds": {
                "item_0": self.value[0].to_encodable(),
            },
        }


@dataclass
class MerkleProof:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "MerkleProof"
    value: MerkleProofValue

    def to_json(self) -> MerkleProofJSON:
        return MerkleProofJSON(
            kind="MerkleProof",
            value=(self.value[0].to_json(),),
        )

    def to_encodable(self) -> dict:
        return {
            "MerkleProof": {
                "item_0": self.value[0].to_encodable(),
            },
        }


@dataclass
class Number:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "Number"
    value: NumberValue

    def to_json(self) -> NumberJSON:
        return NumberJSON(
            kind="Number",
            value=(self.value[0],),
        )

    def to_encodable(self) -> dict:
        return {
            "Number": {
                "item_0": self.value[0],
            },
        }


PayloadTypeKind = typing.Union[Pubkey, Seeds, MerkleProof, Number]
PayloadTypeJSON = typing.Union[PubkeyJSON, SeedsJSON, MerkleProofJSON, NumberJSON]


def from_decoded(obj: dict) -> PayloadTypeKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Pubkey" in obj:
        val = obj["Pubkey"]
        return Pubkey((val["item_0"],))
    if "Seeds" in obj:
        val = obj["Seeds"]
        return Seeds((seeds_vec.SeedsVec.from_decoded(val["item_0"]),))
    if "MerkleProof" in obj:
        val = obj["MerkleProof"]
        return MerkleProof((proof_info.ProofInfo.from_decoded(val["item_0"]),))
    if "Number" in obj:
        val = obj["Number"]
        return Number((val["item_0"],))
    raise ValueError("Invalid enum object")


def from_json(obj: PayloadTypeJSON) -> PayloadTypeKind:
    if obj["kind"] == "Pubkey":
        pubkey_json_value = typing.cast(PubkeyJSONValue, obj["value"])
        return Pubkey((Pubkey.from_string(pubkey_json_value[0]),))
    if obj["kind"] == "Seeds":
        seeds_json_value = typing.cast(SeedsJSONValue, obj["value"])
        return Seeds((seeds_vec.SeedsVec.from_json(seeds_json_value[0]),))
    if obj["kind"] == "MerkleProof":
        merkle_proof_json_value = typing.cast(MerkleProofJSONValue, obj["value"])
        return MerkleProof(
            (proof_info.ProofInfo.from_json(merkle_proof_json_value[0]),)
        )
    if obj["kind"] == "Number":
        number_json_value = typing.cast(NumberJSONValue, obj["value"])
        return Number((number_json_value[0],))
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Pubkey" / borsh.CStruct("item_0" / BorshPubkey),
    "Seeds" / borsh.CStruct("item_0" / seeds_vec.SeedsVec.layout),
    "MerkleProof" / borsh.CStruct("item_0" / proof_info.ProofInfo.layout),
    "Number" / borsh.CStruct("item_0" / borsh.U64),
)
