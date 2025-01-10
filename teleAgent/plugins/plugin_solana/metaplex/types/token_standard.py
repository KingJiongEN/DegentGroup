from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class NonFungibleJSON(typing.TypedDict):
    kind: typing.Literal["NonFungible"]


class FungibleAssetJSON(typing.TypedDict):
    kind: typing.Literal["FungibleAsset"]


class FungibleJSON(typing.TypedDict):
    kind: typing.Literal["Fungible"]


class NonFungibleEditionJSON(typing.TypedDict):
    kind: typing.Literal["NonFungibleEdition"]


class ProgrammableNonFungibleJSON(typing.TypedDict):
    kind: typing.Literal["ProgrammableNonFungible"]


class ProgrammableNonFungibleEditionJSON(typing.TypedDict):
    kind: typing.Literal["ProgrammableNonFungibleEdition"]


@dataclass
class NonFungible:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "NonFungible"

    @classmethod
    def to_json(cls) -> NonFungibleJSON:
        return NonFungibleJSON(
            kind="NonFungible",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "NonFungible": {},
        }


@dataclass
class FungibleAsset:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "FungibleAsset"

    @classmethod
    def to_json(cls) -> FungibleAssetJSON:
        return FungibleAssetJSON(
            kind="FungibleAsset",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "FungibleAsset": {},
        }


@dataclass
class Fungible:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "Fungible"

    @classmethod
    def to_json(cls) -> FungibleJSON:
        return FungibleJSON(
            kind="Fungible",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Fungible": {},
        }


@dataclass
class NonFungibleEdition:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "NonFungibleEdition"

    @classmethod
    def to_json(cls) -> NonFungibleEditionJSON:
        return NonFungibleEditionJSON(
            kind="NonFungibleEdition",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "NonFungibleEdition": {},
        }


@dataclass
class ProgrammableNonFungible:
    discriminator: typing.ClassVar = 4
    kind: typing.ClassVar = "ProgrammableNonFungible"

    @classmethod
    def to_json(cls) -> ProgrammableNonFungibleJSON:
        return ProgrammableNonFungibleJSON(
            kind="ProgrammableNonFungible",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ProgrammableNonFungible": {},
        }


@dataclass
class ProgrammableNonFungibleEdition:
    discriminator: typing.ClassVar = 5
    kind: typing.ClassVar = "ProgrammableNonFungibleEdition"

    @classmethod
    def to_json(cls) -> ProgrammableNonFungibleEditionJSON:
        return ProgrammableNonFungibleEditionJSON(
            kind="ProgrammableNonFungibleEdition",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ProgrammableNonFungibleEdition": {},
        }


TokenStandardKind = typing.Union[
    NonFungible,
    FungibleAsset,
    Fungible,
    NonFungibleEdition,
    ProgrammableNonFungible,
    ProgrammableNonFungibleEdition,
]
TokenStandardJSON = typing.Union[
    NonFungibleJSON,
    FungibleAssetJSON,
    FungibleJSON,
    NonFungibleEditionJSON,
    ProgrammableNonFungibleJSON,
    ProgrammableNonFungibleEditionJSON,
]


def from_decoded(obj: dict) -> TokenStandardKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "NonFungible" in obj:
        return NonFungible()
    if "FungibleAsset" in obj:
        return FungibleAsset()
    if "Fungible" in obj:
        return Fungible()
    if "NonFungibleEdition" in obj:
        return NonFungibleEdition()
    if "ProgrammableNonFungible" in obj:
        return ProgrammableNonFungible()
    if "ProgrammableNonFungibleEdition" in obj:
        return ProgrammableNonFungibleEdition()
    raise ValueError("Invalid enum object")


def from_json(obj: TokenStandardJSON) -> TokenStandardKind:
    if obj["kind"] == "NonFungible":
        return NonFungible()
    if obj["kind"] == "FungibleAsset":
        return FungibleAsset()
    if obj["kind"] == "Fungible":
        return Fungible()
    if obj["kind"] == "NonFungibleEdition":
        return NonFungibleEdition()
    if obj["kind"] == "ProgrammableNonFungible":
        return ProgrammableNonFungible()
    if obj["kind"] == "ProgrammableNonFungibleEdition":
        return ProgrammableNonFungibleEdition()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "NonFungible" / borsh.CStruct(),
    "FungibleAsset" / borsh.CStruct(),
    "Fungible" / borsh.CStruct(),
    "NonFungibleEdition" / borsh.CStruct(),
    "ProgrammableNonFungible" / borsh.CStruct(),
    "ProgrammableNonFungibleEdition" / borsh.CStruct(),
)
