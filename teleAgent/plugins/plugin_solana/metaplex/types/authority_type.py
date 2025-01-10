from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class NoneJSON(typing.TypedDict):
    kind: typing.Literal["None"]


class MetadataJSON(typing.TypedDict):
    kind: typing.Literal["Metadata"]


class HolderJSON(typing.TypedDict):
    kind: typing.Literal["Holder"]


class MetadataDelegateJSON(typing.TypedDict):
    kind: typing.Literal["MetadataDelegate"]


class TokenDelegateJSON(typing.TypedDict):
    kind: typing.Literal["TokenDelegate"]


@dataclass
class None_:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "None"

    @classmethod
    def to_json(cls) -> NoneJSON:
        return NoneJSON(
            kind="None",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "None": {},
        }


@dataclass
class Metadata:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Metadata"

    @classmethod
    def to_json(cls) -> MetadataJSON:
        return MetadataJSON(
            kind="Metadata",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Metadata": {},
        }


@dataclass
class Holder:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "Holder"

    @classmethod
    def to_json(cls) -> HolderJSON:
        return HolderJSON(
            kind="Holder",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Holder": {},
        }


@dataclass
class MetadataDelegate:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "MetadataDelegate"

    @classmethod
    def to_json(cls) -> MetadataDelegateJSON:
        return MetadataDelegateJSON(
            kind="MetadataDelegate",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MetadataDelegate": {},
        }


@dataclass
class TokenDelegate:
    discriminator: typing.ClassVar = 4
    kind: typing.ClassVar = "TokenDelegate"

    @classmethod
    def to_json(cls) -> TokenDelegateJSON:
        return TokenDelegateJSON(
            kind="TokenDelegate",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "TokenDelegate": {},
        }


AuthorityTypeKind = typing.Union[
    None_, Metadata, Holder, MetadataDelegate, TokenDelegate
]
AuthorityTypeJSON = typing.Union[
    NoneJSON, MetadataJSON, HolderJSON, MetadataDelegateJSON, TokenDelegateJSON
]


def from_decoded(obj: dict) -> AuthorityTypeKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "None" in obj:
        return None_()
    if "Metadata" in obj:
        return Metadata()
    if "Holder" in obj:
        return Holder()
    if "MetadataDelegate" in obj:
        return MetadataDelegate()
    if "TokenDelegate" in obj:
        return TokenDelegate()
    raise ValueError("Invalid enum object")


def from_json(obj: AuthorityTypeJSON) -> AuthorityTypeKind:
    if obj["kind"] == "None":
        return None_()
    if obj["kind"] == "Metadata":
        return Metadata()
    if obj["kind"] == "Holder":
        return Holder()
    if obj["kind"] == "MetadataDelegate":
        return MetadataDelegate()
    if obj["kind"] == "TokenDelegate":
        return TokenDelegate()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "None" / borsh.CStruct(),
    "Metadata" / borsh.CStruct(),
    "Holder" / borsh.CStruct(),
    "MetadataDelegate" / borsh.CStruct(),
    "TokenDelegate" / borsh.CStruct(),
)
