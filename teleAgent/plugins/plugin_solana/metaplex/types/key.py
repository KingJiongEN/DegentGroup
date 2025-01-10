from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class UninitializedJSON(typing.TypedDict):
    kind: typing.Literal["Uninitialized"]


class EditionV1JSON(typing.TypedDict):
    kind: typing.Literal["EditionV1"]


class MasterEditionV1JSON(typing.TypedDict):
    kind: typing.Literal["MasterEditionV1"]


class ReservationListV1JSON(typing.TypedDict):
    kind: typing.Literal["ReservationListV1"]


class MetadataV1JSON(typing.TypedDict):
    kind: typing.Literal["MetadataV1"]


class ReservationListV2JSON(typing.TypedDict):
    kind: typing.Literal["ReservationListV2"]


class MasterEditionV2JSON(typing.TypedDict):
    kind: typing.Literal["MasterEditionV2"]


class EditionMarkerJSON(typing.TypedDict):
    kind: typing.Literal["EditionMarker"]


class UseAuthorityRecordJSON(typing.TypedDict):
    kind: typing.Literal["UseAuthorityRecord"]


class CollectionAuthorityRecordJSON(typing.TypedDict):
    kind: typing.Literal["CollectionAuthorityRecord"]


class TokenOwnedEscrowJSON(typing.TypedDict):
    kind: typing.Literal["TokenOwnedEscrow"]


class TokenRecordJSON(typing.TypedDict):
    kind: typing.Literal["TokenRecord"]


class MetadataDelegateJSON(typing.TypedDict):
    kind: typing.Literal["MetadataDelegate"]


class EditionMarkerV2JSON(typing.TypedDict):
    kind: typing.Literal["EditionMarkerV2"]


class HolderDelegateJSON(typing.TypedDict):
    kind: typing.Literal["HolderDelegate"]


@dataclass
class Uninitialized:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Uninitialized"

    @classmethod
    def to_json(cls) -> UninitializedJSON:
        return UninitializedJSON(
            kind="Uninitialized",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Uninitialized": {},
        }


@dataclass
class EditionV1:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "EditionV1"

    @classmethod
    def to_json(cls) -> EditionV1JSON:
        return EditionV1JSON(
            kind="EditionV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "EditionV1": {},
        }


@dataclass
class MasterEditionV1:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "MasterEditionV1"

    @classmethod
    def to_json(cls) -> MasterEditionV1JSON:
        return MasterEditionV1JSON(
            kind="MasterEditionV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MasterEditionV1": {},
        }


@dataclass
class ReservationListV1:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "ReservationListV1"

    @classmethod
    def to_json(cls) -> ReservationListV1JSON:
        return ReservationListV1JSON(
            kind="ReservationListV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ReservationListV1": {},
        }


@dataclass
class MetadataV1:
    discriminator: typing.ClassVar = 4
    kind: typing.ClassVar = "MetadataV1"

    @classmethod
    def to_json(cls) -> MetadataV1JSON:
        return MetadataV1JSON(
            kind="MetadataV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MetadataV1": {},
        }


@dataclass
class ReservationListV2:
    discriminator: typing.ClassVar = 5
    kind: typing.ClassVar = "ReservationListV2"

    @classmethod
    def to_json(cls) -> ReservationListV2JSON:
        return ReservationListV2JSON(
            kind="ReservationListV2",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ReservationListV2": {},
        }


@dataclass
class MasterEditionV2:
    discriminator: typing.ClassVar = 6
    kind: typing.ClassVar = "MasterEditionV2"

    @classmethod
    def to_json(cls) -> MasterEditionV2JSON:
        return MasterEditionV2JSON(
            kind="MasterEditionV2",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MasterEditionV2": {},
        }


@dataclass
class EditionMarker:
    discriminator: typing.ClassVar = 7
    kind: typing.ClassVar = "EditionMarker"

    @classmethod
    def to_json(cls) -> EditionMarkerJSON:
        return EditionMarkerJSON(
            kind="EditionMarker",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "EditionMarker": {},
        }


@dataclass
class UseAuthorityRecord:
    discriminator: typing.ClassVar = 8
    kind: typing.ClassVar = "UseAuthorityRecord"

    @classmethod
    def to_json(cls) -> UseAuthorityRecordJSON:
        return UseAuthorityRecordJSON(
            kind="UseAuthorityRecord",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "UseAuthorityRecord": {},
        }


@dataclass
class CollectionAuthorityRecord:
    discriminator: typing.ClassVar = 9
    kind: typing.ClassVar = "CollectionAuthorityRecord"

    @classmethod
    def to_json(cls) -> CollectionAuthorityRecordJSON:
        return CollectionAuthorityRecordJSON(
            kind="CollectionAuthorityRecord",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "CollectionAuthorityRecord": {},
        }


@dataclass
class TokenOwnedEscrow:
    discriminator: typing.ClassVar = 10
    kind: typing.ClassVar = "TokenOwnedEscrow"

    @classmethod
    def to_json(cls) -> TokenOwnedEscrowJSON:
        return TokenOwnedEscrowJSON(
            kind="TokenOwnedEscrow",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "TokenOwnedEscrow": {},
        }


@dataclass
class TokenRecord:
    discriminator: typing.ClassVar = 11
    kind: typing.ClassVar = "TokenRecord"

    @classmethod
    def to_json(cls) -> TokenRecordJSON:
        return TokenRecordJSON(
            kind="TokenRecord",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "TokenRecord": {},
        }


@dataclass
class MetadataDelegate:
    discriminator: typing.ClassVar = 12
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
class EditionMarkerV2:
    discriminator: typing.ClassVar = 13
    kind: typing.ClassVar = "EditionMarkerV2"

    @classmethod
    def to_json(cls) -> EditionMarkerV2JSON:
        return EditionMarkerV2JSON(
            kind="EditionMarkerV2",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "EditionMarkerV2": {},
        }


@dataclass
class HolderDelegate:
    discriminator: typing.ClassVar = 14
    kind: typing.ClassVar = "HolderDelegate"

    @classmethod
    def to_json(cls) -> HolderDelegateJSON:
        return HolderDelegateJSON(
            kind="HolderDelegate",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "HolderDelegate": {},
        }


KeyKind = typing.Union[
    Uninitialized,
    EditionV1,
    MasterEditionV1,
    ReservationListV1,
    MetadataV1,
    ReservationListV2,
    MasterEditionV2,
    EditionMarker,
    UseAuthorityRecord,
    CollectionAuthorityRecord,
    TokenOwnedEscrow,
    TokenRecord,
    MetadataDelegate,
    EditionMarkerV2,
    HolderDelegate,
]
KeyJSON = typing.Union[
    UninitializedJSON,
    EditionV1JSON,
    MasterEditionV1JSON,
    ReservationListV1JSON,
    MetadataV1JSON,
    ReservationListV2JSON,
    MasterEditionV2JSON,
    EditionMarkerJSON,
    UseAuthorityRecordJSON,
    CollectionAuthorityRecordJSON,
    TokenOwnedEscrowJSON,
    TokenRecordJSON,
    MetadataDelegateJSON,
    EditionMarkerV2JSON,
    HolderDelegateJSON,
]


def from_decoded(obj: dict) -> KeyKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Uninitialized" in obj:
        return Uninitialized()
    if "EditionV1" in obj:
        return EditionV1()
    if "MasterEditionV1" in obj:
        return MasterEditionV1()
    if "ReservationListV1" in obj:
        return ReservationListV1()
    if "MetadataV1" in obj:
        return MetadataV1()
    if "ReservationListV2" in obj:
        return ReservationListV2()
    if "MasterEditionV2" in obj:
        return MasterEditionV2()
    if "EditionMarker" in obj:
        return EditionMarker()
    if "UseAuthorityRecord" in obj:
        return UseAuthorityRecord()
    if "CollectionAuthorityRecord" in obj:
        return CollectionAuthorityRecord()
    if "TokenOwnedEscrow" in obj:
        return TokenOwnedEscrow()
    if "TokenRecord" in obj:
        return TokenRecord()
    if "MetadataDelegate" in obj:
        return MetadataDelegate()
    if "EditionMarkerV2" in obj:
        return EditionMarkerV2()
    if "HolderDelegate" in obj:
        return HolderDelegate()
    raise ValueError("Invalid enum object")


def from_json(obj: KeyJSON) -> KeyKind:
    if obj["kind"] == "Uninitialized":
        return Uninitialized()
    if obj["kind"] == "EditionV1":
        return EditionV1()
    if obj["kind"] == "MasterEditionV1":
        return MasterEditionV1()
    if obj["kind"] == "ReservationListV1":
        return ReservationListV1()
    if obj["kind"] == "MetadataV1":
        return MetadataV1()
    if obj["kind"] == "ReservationListV2":
        return ReservationListV2()
    if obj["kind"] == "MasterEditionV2":
        return MasterEditionV2()
    if obj["kind"] == "EditionMarker":
        return EditionMarker()
    if obj["kind"] == "UseAuthorityRecord":
        return UseAuthorityRecord()
    if obj["kind"] == "CollectionAuthorityRecord":
        return CollectionAuthorityRecord()
    if obj["kind"] == "TokenOwnedEscrow":
        return TokenOwnedEscrow()
    if obj["kind"] == "TokenRecord":
        return TokenRecord()
    if obj["kind"] == "MetadataDelegate":
        return MetadataDelegate()
    if obj["kind"] == "EditionMarkerV2":
        return EditionMarkerV2()
    if obj["kind"] == "HolderDelegate":
        return HolderDelegate()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Uninitialized" / borsh.CStruct(),
    "EditionV1" / borsh.CStruct(),
    "MasterEditionV1" / borsh.CStruct(),
    "ReservationListV1" / borsh.CStruct(),
    "MetadataV1" / borsh.CStruct(),
    "ReservationListV2" / borsh.CStruct(),
    "MasterEditionV2" / borsh.CStruct(),
    "EditionMarker" / borsh.CStruct(),
    "UseAuthorityRecord" / borsh.CStruct(),
    "CollectionAuthorityRecord" / borsh.CStruct(),
    "TokenOwnedEscrow" / borsh.CStruct(),
    "TokenRecord" / borsh.CStruct(),
    "MetadataDelegate" / borsh.CStruct(),
    "EditionMarkerV2" / borsh.CStruct(),
    "HolderDelegate" / borsh.CStruct(),
)
