from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class AuthorityItemJSON(typing.TypedDict):
    kind: typing.Literal["AuthorityItem"]


class CollectionJSON(typing.TypedDict):
    kind: typing.Literal["Collection"]


class UseJSON(typing.TypedDict):
    kind: typing.Literal["Use"]


class DataJSON(typing.TypedDict):
    kind: typing.Literal["Data"]


class ProgrammableConfigJSON(typing.TypedDict):
    kind: typing.Literal["ProgrammableConfig"]


class DataItemJSON(typing.TypedDict):
    kind: typing.Literal["DataItem"]


class CollectionItemJSON(typing.TypedDict):
    kind: typing.Literal["CollectionItem"]


class ProgrammableConfigItemJSON(typing.TypedDict):
    kind: typing.Literal["ProgrammableConfigItem"]


@dataclass
class AuthorityItem:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "AuthorityItem"

    @classmethod
    def to_json(cls) -> AuthorityItemJSON:
        return AuthorityItemJSON(
            kind="AuthorityItem",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "AuthorityItem": {},
        }


@dataclass
class Collection:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Collection"

    @classmethod
    def to_json(cls) -> CollectionJSON:
        return CollectionJSON(
            kind="Collection",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Collection": {},
        }


@dataclass
class Use:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "Use"

    @classmethod
    def to_json(cls) -> UseJSON:
        return UseJSON(
            kind="Use",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Use": {},
        }


@dataclass
class Data:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "Data"

    @classmethod
    def to_json(cls) -> DataJSON:
        return DataJSON(
            kind="Data",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Data": {},
        }


@dataclass
class ProgrammableConfig:
    discriminator: typing.ClassVar = 4
    kind: typing.ClassVar = "ProgrammableConfig"

    @classmethod
    def to_json(cls) -> ProgrammableConfigJSON:
        return ProgrammableConfigJSON(
            kind="ProgrammableConfig",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ProgrammableConfig": {},
        }


@dataclass
class DataItem:
    discriminator: typing.ClassVar = 5
    kind: typing.ClassVar = "DataItem"

    @classmethod
    def to_json(cls) -> DataItemJSON:
        return DataItemJSON(
            kind="DataItem",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "DataItem": {},
        }


@dataclass
class CollectionItem:
    discriminator: typing.ClassVar = 6
    kind: typing.ClassVar = "CollectionItem"

    @classmethod
    def to_json(cls) -> CollectionItemJSON:
        return CollectionItemJSON(
            kind="CollectionItem",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "CollectionItem": {},
        }


@dataclass
class ProgrammableConfigItem:
    discriminator: typing.ClassVar = 7
    kind: typing.ClassVar = "ProgrammableConfigItem"

    @classmethod
    def to_json(cls) -> ProgrammableConfigItemJSON:
        return ProgrammableConfigItemJSON(
            kind="ProgrammableConfigItem",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ProgrammableConfigItem": {},
        }


MetadataDelegateRoleKind = typing.Union[
    AuthorityItem,
    Collection,
    Use,
    Data,
    ProgrammableConfig,
    DataItem,
    CollectionItem,
    ProgrammableConfigItem,
]
MetadataDelegateRoleJSON = typing.Union[
    AuthorityItemJSON,
    CollectionJSON,
    UseJSON,
    DataJSON,
    ProgrammableConfigJSON,
    DataItemJSON,
    CollectionItemJSON,
    ProgrammableConfigItemJSON,
]


def from_decoded(obj: dict) -> MetadataDelegateRoleKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "AuthorityItem" in obj:
        return AuthorityItem()
    if "Collection" in obj:
        return Collection()
    if "Use" in obj:
        return Use()
    if "Data" in obj:
        return Data()
    if "ProgrammableConfig" in obj:
        return ProgrammableConfig()
    if "DataItem" in obj:
        return DataItem()
    if "CollectionItem" in obj:
        return CollectionItem()
    if "ProgrammableConfigItem" in obj:
        return ProgrammableConfigItem()
    raise ValueError("Invalid enum object")


def from_json(obj: MetadataDelegateRoleJSON) -> MetadataDelegateRoleKind:
    if obj["kind"] == "AuthorityItem":
        return AuthorityItem()
    if obj["kind"] == "Collection":
        return Collection()
    if obj["kind"] == "Use":
        return Use()
    if obj["kind"] == "Data":
        return Data()
    if obj["kind"] == "ProgrammableConfig":
        return ProgrammableConfig()
    if obj["kind"] == "DataItem":
        return DataItem()
    if obj["kind"] == "CollectionItem":
        return CollectionItem()
    if obj["kind"] == "ProgrammableConfigItem":
        return ProgrammableConfigItem()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "AuthorityItem" / borsh.CStruct(),
    "Collection" / borsh.CStruct(),
    "Use" / borsh.CStruct(),
    "Data" / borsh.CStruct(),
    "ProgrammableConfig" / borsh.CStruct(),
    "DataItem" / borsh.CStruct(),
    "CollectionItem" / borsh.CStruct(),
    "ProgrammableConfigItem" / borsh.CStruct(),
)
