from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class CollectionV1JSON(typing.TypedDict):
    kind: typing.Literal["CollectionV1"]


class SaleV1JSON(typing.TypedDict):
    kind: typing.Literal["SaleV1"]


class TransferV1JSON(typing.TypedDict):
    kind: typing.Literal["TransferV1"]


class DataV1JSON(typing.TypedDict):
    kind: typing.Literal["DataV1"]


class UtilityV1JSON(typing.TypedDict):
    kind: typing.Literal["UtilityV1"]


class StakingV1JSON(typing.TypedDict):
    kind: typing.Literal["StakingV1"]


class StandardV1JSON(typing.TypedDict):
    kind: typing.Literal["StandardV1"]


class LockedTransferV1JSON(typing.TypedDict):
    kind: typing.Literal["LockedTransferV1"]


class ProgrammableConfigV1JSON(typing.TypedDict):
    kind: typing.Literal["ProgrammableConfigV1"]


class MigrationV1JSON(typing.TypedDict):
    kind: typing.Literal["MigrationV1"]


class AuthorityItemV1JSON(typing.TypedDict):
    kind: typing.Literal["AuthorityItemV1"]


class DataItemV1JSON(typing.TypedDict):
    kind: typing.Literal["DataItemV1"]


class CollectionItemV1JSON(typing.TypedDict):
    kind: typing.Literal["CollectionItemV1"]


class ProgrammableConfigItemV1JSON(typing.TypedDict):
    kind: typing.Literal["ProgrammableConfigItemV1"]


class PrintDelegateV1JSON(typing.TypedDict):
    kind: typing.Literal["PrintDelegateV1"]


@dataclass
class CollectionV1:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "CollectionV1"

    @classmethod
    def to_json(cls) -> CollectionV1JSON:
        return CollectionV1JSON(
            kind="CollectionV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "CollectionV1": {},
        }


@dataclass
class SaleV1:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "SaleV1"

    @classmethod
    def to_json(cls) -> SaleV1JSON:
        return SaleV1JSON(
            kind="SaleV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "SaleV1": {},
        }


@dataclass
class TransferV1:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "TransferV1"

    @classmethod
    def to_json(cls) -> TransferV1JSON:
        return TransferV1JSON(
            kind="TransferV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "TransferV1": {},
        }


@dataclass
class DataV1:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "DataV1"

    @classmethod
    def to_json(cls) -> DataV1JSON:
        return DataV1JSON(
            kind="DataV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "DataV1": {},
        }


@dataclass
class UtilityV1:
    discriminator: typing.ClassVar = 4
    kind: typing.ClassVar = "UtilityV1"

    @classmethod
    def to_json(cls) -> UtilityV1JSON:
        return UtilityV1JSON(
            kind="UtilityV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "UtilityV1": {},
        }


@dataclass
class StakingV1:
    discriminator: typing.ClassVar = 5
    kind: typing.ClassVar = "StakingV1"

    @classmethod
    def to_json(cls) -> StakingV1JSON:
        return StakingV1JSON(
            kind="StakingV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "StakingV1": {},
        }


@dataclass
class StandardV1:
    discriminator: typing.ClassVar = 6
    kind: typing.ClassVar = "StandardV1"

    @classmethod
    def to_json(cls) -> StandardV1JSON:
        return StandardV1JSON(
            kind="StandardV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "StandardV1": {},
        }


@dataclass
class LockedTransferV1:
    discriminator: typing.ClassVar = 7
    kind: typing.ClassVar = "LockedTransferV1"

    @classmethod
    def to_json(cls) -> LockedTransferV1JSON:
        return LockedTransferV1JSON(
            kind="LockedTransferV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "LockedTransferV1": {},
        }


@dataclass
class ProgrammableConfigV1:
    discriminator: typing.ClassVar = 8
    kind: typing.ClassVar = "ProgrammableConfigV1"

    @classmethod
    def to_json(cls) -> ProgrammableConfigV1JSON:
        return ProgrammableConfigV1JSON(
            kind="ProgrammableConfigV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ProgrammableConfigV1": {},
        }


@dataclass
class MigrationV1:
    discriminator: typing.ClassVar = 9
    kind: typing.ClassVar = "MigrationV1"

    @classmethod
    def to_json(cls) -> MigrationV1JSON:
        return MigrationV1JSON(
            kind="MigrationV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "MigrationV1": {},
        }


@dataclass
class AuthorityItemV1:
    discriminator: typing.ClassVar = 10
    kind: typing.ClassVar = "AuthorityItemV1"

    @classmethod
    def to_json(cls) -> AuthorityItemV1JSON:
        return AuthorityItemV1JSON(
            kind="AuthorityItemV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "AuthorityItemV1": {},
        }


@dataclass
class DataItemV1:
    discriminator: typing.ClassVar = 11
    kind: typing.ClassVar = "DataItemV1"

    @classmethod
    def to_json(cls) -> DataItemV1JSON:
        return DataItemV1JSON(
            kind="DataItemV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "DataItemV1": {},
        }


@dataclass
class CollectionItemV1:
    discriminator: typing.ClassVar = 12
    kind: typing.ClassVar = "CollectionItemV1"

    @classmethod
    def to_json(cls) -> CollectionItemV1JSON:
        return CollectionItemV1JSON(
            kind="CollectionItemV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "CollectionItemV1": {},
        }


@dataclass
class ProgrammableConfigItemV1:
    discriminator: typing.ClassVar = 13
    kind: typing.ClassVar = "ProgrammableConfigItemV1"

    @classmethod
    def to_json(cls) -> ProgrammableConfigItemV1JSON:
        return ProgrammableConfigItemV1JSON(
            kind="ProgrammableConfigItemV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "ProgrammableConfigItemV1": {},
        }


@dataclass
class PrintDelegateV1:
    discriminator: typing.ClassVar = 14
    kind: typing.ClassVar = "PrintDelegateV1"

    @classmethod
    def to_json(cls) -> PrintDelegateV1JSON:
        return PrintDelegateV1JSON(
            kind="PrintDelegateV1",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "PrintDelegateV1": {},
        }


RevokeArgsKind = typing.Union[
    CollectionV1,
    SaleV1,
    TransferV1,
    DataV1,
    UtilityV1,
    StakingV1,
    StandardV1,
    LockedTransferV1,
    ProgrammableConfigV1,
    MigrationV1,
    AuthorityItemV1,
    DataItemV1,
    CollectionItemV1,
    ProgrammableConfigItemV1,
    PrintDelegateV1,
]
RevokeArgsJSON = typing.Union[
    CollectionV1JSON,
    SaleV1JSON,
    TransferV1JSON,
    DataV1JSON,
    UtilityV1JSON,
    StakingV1JSON,
    StandardV1JSON,
    LockedTransferV1JSON,
    ProgrammableConfigV1JSON,
    MigrationV1JSON,
    AuthorityItemV1JSON,
    DataItemV1JSON,
    CollectionItemV1JSON,
    ProgrammableConfigItemV1JSON,
    PrintDelegateV1JSON,
]


def from_decoded(obj: dict) -> RevokeArgsKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "CollectionV1" in obj:
        return CollectionV1()
    if "SaleV1" in obj:
        return SaleV1()
    if "TransferV1" in obj:
        return TransferV1()
    if "DataV1" in obj:
        return DataV1()
    if "UtilityV1" in obj:
        return UtilityV1()
    if "StakingV1" in obj:
        return StakingV1()
    if "StandardV1" in obj:
        return StandardV1()
    if "LockedTransferV1" in obj:
        return LockedTransferV1()
    if "ProgrammableConfigV1" in obj:
        return ProgrammableConfigV1()
    if "MigrationV1" in obj:
        return MigrationV1()
    if "AuthorityItemV1" in obj:
        return AuthorityItemV1()
    if "DataItemV1" in obj:
        return DataItemV1()
    if "CollectionItemV1" in obj:
        return CollectionItemV1()
    if "ProgrammableConfigItemV1" in obj:
        return ProgrammableConfigItemV1()
    if "PrintDelegateV1" in obj:
        return PrintDelegateV1()
    raise ValueError("Invalid enum object")


def from_json(obj: RevokeArgsJSON) -> RevokeArgsKind:
    if obj["kind"] == "CollectionV1":
        return CollectionV1()
    if obj["kind"] == "SaleV1":
        return SaleV1()
    if obj["kind"] == "TransferV1":
        return TransferV1()
    if obj["kind"] == "DataV1":
        return DataV1()
    if obj["kind"] == "UtilityV1":
        return UtilityV1()
    if obj["kind"] == "StakingV1":
        return StakingV1()
    if obj["kind"] == "StandardV1":
        return StandardV1()
    if obj["kind"] == "LockedTransferV1":
        return LockedTransferV1()
    if obj["kind"] == "ProgrammableConfigV1":
        return ProgrammableConfigV1()
    if obj["kind"] == "MigrationV1":
        return MigrationV1()
    if obj["kind"] == "AuthorityItemV1":
        return AuthorityItemV1()
    if obj["kind"] == "DataItemV1":
        return DataItemV1()
    if obj["kind"] == "CollectionItemV1":
        return CollectionItemV1()
    if obj["kind"] == "ProgrammableConfigItemV1":
        return ProgrammableConfigItemV1()
    if obj["kind"] == "PrintDelegateV1":
        return PrintDelegateV1()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "CollectionV1" / borsh.CStruct(),
    "SaleV1" / borsh.CStruct(),
    "TransferV1" / borsh.CStruct(),
    "DataV1" / borsh.CStruct(),
    "UtilityV1" / borsh.CStruct(),
    "StakingV1" / borsh.CStruct(),
    "StandardV1" / borsh.CStruct(),
    "LockedTransferV1" / borsh.CStruct(),
    "ProgrammableConfigV1" / borsh.CStruct(),
    "MigrationV1" / borsh.CStruct(),
    "AuthorityItemV1" / borsh.CStruct(),
    "DataItemV1" / borsh.CStruct(),
    "CollectionItemV1" / borsh.CStruct(),
    "ProgrammableConfigItemV1" / borsh.CStruct(),
    "PrintDelegateV1" / borsh.CStruct(),
)
