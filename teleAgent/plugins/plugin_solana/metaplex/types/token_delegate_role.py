from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class SaleJSON(typing.TypedDict):
    kind: typing.Literal["Sale"]


class TransferJSON(typing.TypedDict):
    kind: typing.Literal["Transfer"]


class UtilityJSON(typing.TypedDict):
    kind: typing.Literal["Utility"]


class StakingJSON(typing.TypedDict):
    kind: typing.Literal["Staking"]


class StandardJSON(typing.TypedDict):
    kind: typing.Literal["Standard"]


class LockedTransferJSON(typing.TypedDict):
    kind: typing.Literal["LockedTransfer"]


class MigrationJSON(typing.TypedDict):
    kind: typing.Literal["Migration"]


@dataclass
class Sale:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Sale"

    @classmethod
    def to_json(cls) -> SaleJSON:
        return SaleJSON(
            kind="Sale",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Sale": {},
        }


@dataclass
class Transfer:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Transfer"

    @classmethod
    def to_json(cls) -> TransferJSON:
        return TransferJSON(
            kind="Transfer",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Transfer": {},
        }


@dataclass
class Utility:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "Utility"

    @classmethod
    def to_json(cls) -> UtilityJSON:
        return UtilityJSON(
            kind="Utility",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Utility": {},
        }


@dataclass
class Staking:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "Staking"

    @classmethod
    def to_json(cls) -> StakingJSON:
        return StakingJSON(
            kind="Staking",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Staking": {},
        }


@dataclass
class Standard:
    discriminator: typing.ClassVar = 4
    kind: typing.ClassVar = "Standard"

    @classmethod
    def to_json(cls) -> StandardJSON:
        return StandardJSON(
            kind="Standard",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Standard": {},
        }


@dataclass
class LockedTransfer:
    discriminator: typing.ClassVar = 5
    kind: typing.ClassVar = "LockedTransfer"

    @classmethod
    def to_json(cls) -> LockedTransferJSON:
        return LockedTransferJSON(
            kind="LockedTransfer",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "LockedTransfer": {},
        }


@dataclass
class Migration:
    discriminator: typing.ClassVar = 6
    kind: typing.ClassVar = "Migration"

    @classmethod
    def to_json(cls) -> MigrationJSON:
        return MigrationJSON(
            kind="Migration",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Migration": {},
        }


TokenDelegateRoleKind = typing.Union[
    Sale, Transfer, Utility, Staking, Standard, LockedTransfer, Migration
]
TokenDelegateRoleJSON = typing.Union[
    SaleJSON,
    TransferJSON,
    UtilityJSON,
    StakingJSON,
    StandardJSON,
    LockedTransferJSON,
    MigrationJSON,
]


def from_decoded(obj: dict) -> TokenDelegateRoleKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Sale" in obj:
        return Sale()
    if "Transfer" in obj:
        return Transfer()
    if "Utility" in obj:
        return Utility()
    if "Staking" in obj:
        return Staking()
    if "Standard" in obj:
        return Standard()
    if "LockedTransfer" in obj:
        return LockedTransfer()
    if "Migration" in obj:
        return Migration()
    raise ValueError("Invalid enum object")


def from_json(obj: TokenDelegateRoleJSON) -> TokenDelegateRoleKind:
    if obj["kind"] == "Sale":
        return Sale()
    if obj["kind"] == "Transfer":
        return Transfer()
    if obj["kind"] == "Utility":
        return Utility()
    if obj["kind"] == "Staking":
        return Staking()
    if obj["kind"] == "Standard":
        return Standard()
    if obj["kind"] == "LockedTransfer":
        return LockedTransfer()
    if obj["kind"] == "Migration":
        return Migration()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Sale" / borsh.CStruct(),
    "Transfer" / borsh.CStruct(),
    "Utility" / borsh.CStruct(),
    "Staking" / borsh.CStruct(),
    "Standard" / borsh.CStruct(),
    "LockedTransfer" / borsh.CStruct(),
    "Migration" / borsh.CStruct(),
)
