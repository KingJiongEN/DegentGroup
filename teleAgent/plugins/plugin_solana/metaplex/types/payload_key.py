from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class AmountJSON(typing.TypedDict):
    kind: typing.Literal["Amount"]


class AuthorityJSON(typing.TypedDict):
    kind: typing.Literal["Authority"]


class AuthoritySeedsJSON(typing.TypedDict):
    kind: typing.Literal["AuthoritySeeds"]


class DelegateJSON(typing.TypedDict):
    kind: typing.Literal["Delegate"]


class DelegateSeedsJSON(typing.TypedDict):
    kind: typing.Literal["DelegateSeeds"]


class DestinationJSON(typing.TypedDict):
    kind: typing.Literal["Destination"]


class DestinationSeedsJSON(typing.TypedDict):
    kind: typing.Literal["DestinationSeeds"]


class HolderJSON(typing.TypedDict):
    kind: typing.Literal["Holder"]


class SourceJSON(typing.TypedDict):
    kind: typing.Literal["Source"]


class SourceSeedsJSON(typing.TypedDict):
    kind: typing.Literal["SourceSeeds"]


@dataclass
class Amount:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Amount"

    @classmethod
    def to_json(cls) -> AmountJSON:
        return AmountJSON(
            kind="Amount",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Amount": {},
        }


@dataclass
class Authority:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Authority"

    @classmethod
    def to_json(cls) -> AuthorityJSON:
        return AuthorityJSON(
            kind="Authority",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Authority": {},
        }


@dataclass
class AuthoritySeeds:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "AuthoritySeeds"

    @classmethod
    def to_json(cls) -> AuthoritySeedsJSON:
        return AuthoritySeedsJSON(
            kind="AuthoritySeeds",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "AuthoritySeeds": {},
        }


@dataclass
class Delegate:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "Delegate"

    @classmethod
    def to_json(cls) -> DelegateJSON:
        return DelegateJSON(
            kind="Delegate",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Delegate": {},
        }


@dataclass
class DelegateSeeds:
    discriminator: typing.ClassVar = 4
    kind: typing.ClassVar = "DelegateSeeds"

    @classmethod
    def to_json(cls) -> DelegateSeedsJSON:
        return DelegateSeedsJSON(
            kind="DelegateSeeds",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "DelegateSeeds": {},
        }


@dataclass
class Destination:
    discriminator: typing.ClassVar = 5
    kind: typing.ClassVar = "Destination"

    @classmethod
    def to_json(cls) -> DestinationJSON:
        return DestinationJSON(
            kind="Destination",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Destination": {},
        }


@dataclass
class DestinationSeeds:
    discriminator: typing.ClassVar = 6
    kind: typing.ClassVar = "DestinationSeeds"

    @classmethod
    def to_json(cls) -> DestinationSeedsJSON:
        return DestinationSeedsJSON(
            kind="DestinationSeeds",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "DestinationSeeds": {},
        }


@dataclass
class Holder:
    discriminator: typing.ClassVar = 7
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
class Source:
    discriminator: typing.ClassVar = 8
    kind: typing.ClassVar = "Source"

    @classmethod
    def to_json(cls) -> SourceJSON:
        return SourceJSON(
            kind="Source",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Source": {},
        }


@dataclass
class SourceSeeds:
    discriminator: typing.ClassVar = 9
    kind: typing.ClassVar = "SourceSeeds"

    @classmethod
    def to_json(cls) -> SourceSeedsJSON:
        return SourceSeedsJSON(
            kind="SourceSeeds",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "SourceSeeds": {},
        }


PayloadKeyKind = typing.Union[
    Amount,
    Authority,
    AuthoritySeeds,
    Delegate,
    DelegateSeeds,
    Destination,
    DestinationSeeds,
    Holder,
    Source,
    SourceSeeds,
]
PayloadKeyJSON = typing.Union[
    AmountJSON,
    AuthorityJSON,
    AuthoritySeedsJSON,
    DelegateJSON,
    DelegateSeedsJSON,
    DestinationJSON,
    DestinationSeedsJSON,
    HolderJSON,
    SourceJSON,
    SourceSeedsJSON,
]


def from_decoded(obj: dict) -> PayloadKeyKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Amount" in obj:
        return Amount()
    if "Authority" in obj:
        return Authority()
    if "AuthoritySeeds" in obj:
        return AuthoritySeeds()
    if "Delegate" in obj:
        return Delegate()
    if "DelegateSeeds" in obj:
        return DelegateSeeds()
    if "Destination" in obj:
        return Destination()
    if "DestinationSeeds" in obj:
        return DestinationSeeds()
    if "Holder" in obj:
        return Holder()
    if "Source" in obj:
        return Source()
    if "SourceSeeds" in obj:
        return SourceSeeds()
    raise ValueError("Invalid enum object")


def from_json(obj: PayloadKeyJSON) -> PayloadKeyKind:
    if obj["kind"] == "Amount":
        return Amount()
    if obj["kind"] == "Authority":
        return Authority()
    if obj["kind"] == "AuthoritySeeds":
        return AuthoritySeeds()
    if obj["kind"] == "Delegate":
        return Delegate()
    if obj["kind"] == "DelegateSeeds":
        return DelegateSeeds()
    if obj["kind"] == "Destination":
        return Destination()
    if obj["kind"] == "DestinationSeeds":
        return DestinationSeeds()
    if obj["kind"] == "Holder":
        return Holder()
    if obj["kind"] == "Source":
        return Source()
    if obj["kind"] == "SourceSeeds":
        return SourceSeeds()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Amount" / borsh.CStruct(),
    "Authority" / borsh.CStruct(),
    "AuthoritySeeds" / borsh.CStruct(),
    "Delegate" / borsh.CStruct(),
    "DelegateSeeds" / borsh.CStruct(),
    "Destination" / borsh.CStruct(),
    "DestinationSeeds" / borsh.CStruct(),
    "Holder" / borsh.CStruct(),
    "Source" / borsh.CStruct(),
    "SourceSeeds" / borsh.CStruct(),
)
