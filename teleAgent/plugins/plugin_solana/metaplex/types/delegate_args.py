from __future__ import annotations
from . import (
    authorization_data,
)
import typing
from dataclasses import dataclass
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import EnumForCodegen, BorshPubkey
import borsh_construct as borsh


class CollectionV1JSONValue(typing.TypedDict):
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class SaleV1JSONValue(typing.TypedDict):
    amount: int
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class TransferV1JSONValue(typing.TypedDict):
    amount: int
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class DataV1JSONValue(typing.TypedDict):
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class UtilityV1JSONValue(typing.TypedDict):
    amount: int
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class StakingV1JSONValue(typing.TypedDict):
    amount: int
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class StandardV1JSONValue(typing.TypedDict):
    amount: int


class LockedTransferV1JSONValue(typing.TypedDict):
    amount: int
    locked_address: str
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class ProgrammableConfigV1JSONValue(typing.TypedDict):
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class AuthorityItemV1JSONValue(typing.TypedDict):
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class DataItemV1JSONValue(typing.TypedDict):
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class CollectionItemV1JSONValue(typing.TypedDict):
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class ProgrammableConfigItemV1JSONValue(typing.TypedDict):
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class PrintDelegateV1JSONValue(typing.TypedDict):
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class CollectionV1Value(typing.TypedDict):
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class SaleV1Value(typing.TypedDict):
    amount: int
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class TransferV1Value(typing.TypedDict):
    amount: int
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class DataV1Value(typing.TypedDict):
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class UtilityV1Value(typing.TypedDict):
    amount: int
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class StakingV1Value(typing.TypedDict):
    amount: int
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class StandardV1Value(typing.TypedDict):
    amount: int


class LockedTransferV1Value(typing.TypedDict):
    amount: int
    locked_address: Pubkey
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class ProgrammableConfigV1Value(typing.TypedDict):
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class AuthorityItemV1Value(typing.TypedDict):
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class DataItemV1Value(typing.TypedDict):
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class CollectionItemV1Value(typing.TypedDict):
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class ProgrammableConfigItemV1Value(typing.TypedDict):
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class PrintDelegateV1Value(typing.TypedDict):
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class CollectionV1JSON(typing.TypedDict):
    value: CollectionV1JSONValue
    kind: typing.Literal["CollectionV1"]


class SaleV1JSON(typing.TypedDict):
    value: SaleV1JSONValue
    kind: typing.Literal["SaleV1"]


class TransferV1JSON(typing.TypedDict):
    value: TransferV1JSONValue
    kind: typing.Literal["TransferV1"]


class DataV1JSON(typing.TypedDict):
    value: DataV1JSONValue
    kind: typing.Literal["DataV1"]


class UtilityV1JSON(typing.TypedDict):
    value: UtilityV1JSONValue
    kind: typing.Literal["UtilityV1"]


class StakingV1JSON(typing.TypedDict):
    value: StakingV1JSONValue
    kind: typing.Literal["StakingV1"]


class StandardV1JSON(typing.TypedDict):
    value: StandardV1JSONValue
    kind: typing.Literal["StandardV1"]


class LockedTransferV1JSON(typing.TypedDict):
    value: LockedTransferV1JSONValue
    kind: typing.Literal["LockedTransferV1"]


class ProgrammableConfigV1JSON(typing.TypedDict):
    value: ProgrammableConfigV1JSONValue
    kind: typing.Literal["ProgrammableConfigV1"]


class AuthorityItemV1JSON(typing.TypedDict):
    value: AuthorityItemV1JSONValue
    kind: typing.Literal["AuthorityItemV1"]


class DataItemV1JSON(typing.TypedDict):
    value: DataItemV1JSONValue
    kind: typing.Literal["DataItemV1"]


class CollectionItemV1JSON(typing.TypedDict):
    value: CollectionItemV1JSONValue
    kind: typing.Literal["CollectionItemV1"]


class ProgrammableConfigItemV1JSON(typing.TypedDict):
    value: ProgrammableConfigItemV1JSONValue
    kind: typing.Literal["ProgrammableConfigItemV1"]


class PrintDelegateV1JSON(typing.TypedDict):
    value: PrintDelegateV1JSONValue
    kind: typing.Literal["PrintDelegateV1"]


@dataclass
class CollectionV1:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "CollectionV1"
    value: CollectionV1Value

    def to_json(self) -> CollectionV1JSON:
        return CollectionV1JSON(
            kind="CollectionV1",
            value={
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "CollectionV1": {
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class SaleV1:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "SaleV1"
    value: SaleV1Value

    def to_json(self) -> SaleV1JSON:
        return SaleV1JSON(
            kind="SaleV1",
            value={
                "amount": self.value["amount"],
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "SaleV1": {
                "amount": self.value["amount"],
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class TransferV1:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "TransferV1"
    value: TransferV1Value

    def to_json(self) -> TransferV1JSON:
        return TransferV1JSON(
            kind="TransferV1",
            value={
                "amount": self.value["amount"],
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "TransferV1": {
                "amount": self.value["amount"],
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class DataV1:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "DataV1"
    value: DataV1Value

    def to_json(self) -> DataV1JSON:
        return DataV1JSON(
            kind="DataV1",
            value={
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "DataV1": {
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class UtilityV1:
    discriminator: typing.ClassVar = 4
    kind: typing.ClassVar = "UtilityV1"
    value: UtilityV1Value

    def to_json(self) -> UtilityV1JSON:
        return UtilityV1JSON(
            kind="UtilityV1",
            value={
                "amount": self.value["amount"],
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "UtilityV1": {
                "amount": self.value["amount"],
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class StakingV1:
    discriminator: typing.ClassVar = 5
    kind: typing.ClassVar = "StakingV1"
    value: StakingV1Value

    def to_json(self) -> StakingV1JSON:
        return StakingV1JSON(
            kind="StakingV1",
            value={
                "amount": self.value["amount"],
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "StakingV1": {
                "amount": self.value["amount"],
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class StandardV1:
    discriminator: typing.ClassVar = 6
    kind: typing.ClassVar = "StandardV1"
    value: StandardV1Value

    def to_json(self) -> StandardV1JSON:
        return StandardV1JSON(
            kind="StandardV1",
            value={
                "amount": self.value["amount"],
            },
        )

    def to_encodable(self) -> dict:
        return {
            "StandardV1": {
                "amount": self.value["amount"],
            },
        }


@dataclass
class LockedTransferV1:
    discriminator: typing.ClassVar = 7
    kind: typing.ClassVar = "LockedTransferV1"
    value: LockedTransferV1Value

    def to_json(self) -> LockedTransferV1JSON:
        return LockedTransferV1JSON(
            kind="LockedTransferV1",
            value={
                "amount": self.value["amount"],
                "locked_address": str(self.value["locked_address"]),
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "LockedTransferV1": {
                "amount": self.value["amount"],
                "locked_address": self.value["locked_address"],
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class ProgrammableConfigV1:
    discriminator: typing.ClassVar = 8
    kind: typing.ClassVar = "ProgrammableConfigV1"
    value: ProgrammableConfigV1Value

    def to_json(self) -> ProgrammableConfigV1JSON:
        return ProgrammableConfigV1JSON(
            kind="ProgrammableConfigV1",
            value={
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "ProgrammableConfigV1": {
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class AuthorityItemV1:
    discriminator: typing.ClassVar = 9
    kind: typing.ClassVar = "AuthorityItemV1"
    value: AuthorityItemV1Value

    def to_json(self) -> AuthorityItemV1JSON:
        return AuthorityItemV1JSON(
            kind="AuthorityItemV1",
            value={
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "AuthorityItemV1": {
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class DataItemV1:
    discriminator: typing.ClassVar = 10
    kind: typing.ClassVar = "DataItemV1"
    value: DataItemV1Value

    def to_json(self) -> DataItemV1JSON:
        return DataItemV1JSON(
            kind="DataItemV1",
            value={
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "DataItemV1": {
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class CollectionItemV1:
    discriminator: typing.ClassVar = 11
    kind: typing.ClassVar = "CollectionItemV1"
    value: CollectionItemV1Value

    def to_json(self) -> CollectionItemV1JSON:
        return CollectionItemV1JSON(
            kind="CollectionItemV1",
            value={
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "CollectionItemV1": {
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class ProgrammableConfigItemV1:
    discriminator: typing.ClassVar = 12
    kind: typing.ClassVar = "ProgrammableConfigItemV1"
    value: ProgrammableConfigItemV1Value

    def to_json(self) -> ProgrammableConfigItemV1JSON:
        return ProgrammableConfigItemV1JSON(
            kind="ProgrammableConfigItemV1",
            value={
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "ProgrammableConfigItemV1": {
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class PrintDelegateV1:
    discriminator: typing.ClassVar = 13
    kind: typing.ClassVar = "PrintDelegateV1"
    value: PrintDelegateV1Value

    def to_json(self) -> PrintDelegateV1JSON:
        return PrintDelegateV1JSON(
            kind="PrintDelegateV1",
            value={
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "PrintDelegateV1": {
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


DelegateArgsKind = typing.Union[
    CollectionV1,
    SaleV1,
    TransferV1,
    DataV1,
    UtilityV1,
    StakingV1,
    StandardV1,
    LockedTransferV1,
    ProgrammableConfigV1,
    AuthorityItemV1,
    DataItemV1,
    CollectionItemV1,
    ProgrammableConfigItemV1,
    PrintDelegateV1,
]
DelegateArgsJSON = typing.Union[
    CollectionV1JSON,
    SaleV1JSON,
    TransferV1JSON,
    DataV1JSON,
    UtilityV1JSON,
    StakingV1JSON,
    StandardV1JSON,
    LockedTransferV1JSON,
    ProgrammableConfigV1JSON,
    AuthorityItemV1JSON,
    DataItemV1JSON,
    CollectionItemV1JSON,
    ProgrammableConfigItemV1JSON,
    PrintDelegateV1JSON,
]


def from_decoded(obj: dict) -> DelegateArgsKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "CollectionV1" in obj:
        val = obj["CollectionV1"]
        return CollectionV1(
            CollectionV1Value(
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "SaleV1" in obj:
        val = obj["SaleV1"]
        return SaleV1(
            SaleV1Value(
                amount=val["amount"],
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "TransferV1" in obj:
        val = obj["TransferV1"]
        return TransferV1(
            TransferV1Value(
                amount=val["amount"],
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "DataV1" in obj:
        val = obj["DataV1"]
        return DataV1(
            DataV1Value(
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "UtilityV1" in obj:
        val = obj["UtilityV1"]
        return UtilityV1(
            UtilityV1Value(
                amount=val["amount"],
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "StakingV1" in obj:
        val = obj["StakingV1"]
        return StakingV1(
            StakingV1Value(
                amount=val["amount"],
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "StandardV1" in obj:
        val = obj["StandardV1"]
        return StandardV1(
            StandardV1Value(
                amount=val["amount"],
            )
        )
    if "LockedTransferV1" in obj:
        val = obj["LockedTransferV1"]
        return LockedTransferV1(
            LockedTransferV1Value(
                amount=val["amount"],
                locked_address=val["locked_address"],
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "ProgrammableConfigV1" in obj:
        val = obj["ProgrammableConfigV1"]
        return ProgrammableConfigV1(
            ProgrammableConfigV1Value(
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "AuthorityItemV1" in obj:
        val = obj["AuthorityItemV1"]
        return AuthorityItemV1(
            AuthorityItemV1Value(
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "DataItemV1" in obj:
        val = obj["DataItemV1"]
        return DataItemV1(
            DataItemV1Value(
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "CollectionItemV1" in obj:
        val = obj["CollectionItemV1"]
        return CollectionItemV1(
            CollectionItemV1Value(
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "ProgrammableConfigItemV1" in obj:
        val = obj["ProgrammableConfigItemV1"]
        return ProgrammableConfigItemV1(
            ProgrammableConfigItemV1Value(
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "PrintDelegateV1" in obj:
        val = obj["PrintDelegateV1"]
        return PrintDelegateV1(
            PrintDelegateV1Value(
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    raise ValueError("Invalid enum object")


def from_json(obj: DelegateArgsJSON) -> DelegateArgsKind:
    if obj["kind"] == "CollectionV1":
        collection_v1json_value = typing.cast(CollectionV1JSONValue, obj["value"])
        return CollectionV1(
            CollectionV1Value(
                authorization_data=(
                    None
                    if collection_v1json_value["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_json(
                        collection_v1json_value["authorization_data"]
                    )
                ),
            )
        )
    if obj["kind"] == "SaleV1":
        sale_v1json_value = typing.cast(SaleV1JSONValue, obj["value"])
        return SaleV1(
            SaleV1Value(
                amount=sale_v1json_value["amount"],
                authorization_data=(
                    None
                    if sale_v1json_value["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_json(
                        sale_v1json_value["authorization_data"]
                    )
                ),
            )
        )
    if obj["kind"] == "TransferV1":
        transfer_v1json_value = typing.cast(TransferV1JSONValue, obj["value"])
        return TransferV1(
            TransferV1Value(
                amount=transfer_v1json_value["amount"],
                authorization_data=(
                    None
                    if transfer_v1json_value["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_json(
                        transfer_v1json_value["authorization_data"]
                    )
                ),
            )
        )
    if obj["kind"] == "DataV1":
        data_v1json_value = typing.cast(DataV1JSONValue, obj["value"])
        return DataV1(
            DataV1Value(
                authorization_data=(
                    None
                    if data_v1json_value["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_json(
                        data_v1json_value["authorization_data"]
                    )
                ),
            )
        )
    if obj["kind"] == "UtilityV1":
        utility_v1json_value = typing.cast(UtilityV1JSONValue, obj["value"])
        return UtilityV1(
            UtilityV1Value(
                amount=utility_v1json_value["amount"],
                authorization_data=(
                    None
                    if utility_v1json_value["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_json(
                        utility_v1json_value["authorization_data"]
                    )
                ),
            )
        )
    if obj["kind"] == "StakingV1":
        staking_v1json_value = typing.cast(StakingV1JSONValue, obj["value"])
        return StakingV1(
            StakingV1Value(
                amount=staking_v1json_value["amount"],
                authorization_data=(
                    None
                    if staking_v1json_value["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_json(
                        staking_v1json_value["authorization_data"]
                    )
                ),
            )
        )
    if obj["kind"] == "StandardV1":
        standard_v1json_value = typing.cast(StandardV1JSONValue, obj["value"])
        return StandardV1(
            StandardV1Value(
                amount=standard_v1json_value["amount"],
            )
        )
    if obj["kind"] == "LockedTransferV1":
        locked_transfer_v1json_value = typing.cast(
            LockedTransferV1JSONValue, obj["value"]
        )
        return LockedTransferV1(
            LockedTransferV1Value(
                amount=locked_transfer_v1json_value["amount"],
                locked_address=Pubkey.from_string(
                    locked_transfer_v1json_value["locked_address"]
                ),
                authorization_data=(
                    None
                    if locked_transfer_v1json_value["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_json(
                        locked_transfer_v1json_value["authorization_data"]
                    )
                ),
            )
        )
    if obj["kind"] == "ProgrammableConfigV1":
        programmable_config_v1json_value = typing.cast(
            ProgrammableConfigV1JSONValue, obj["value"]
        )
        return ProgrammableConfigV1(
            ProgrammableConfigV1Value(
                authorization_data=(
                    None
                    if programmable_config_v1json_value["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_json(
                        programmable_config_v1json_value["authorization_data"]
                    )
                ),
            )
        )
    if obj["kind"] == "AuthorityItemV1":
        authority_item_v1json_value = typing.cast(
            AuthorityItemV1JSONValue, obj["value"]
        )
        return AuthorityItemV1(
            AuthorityItemV1Value(
                authorization_data=(
                    None
                    if authority_item_v1json_value["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_json(
                        authority_item_v1json_value["authorization_data"]
                    )
                ),
            )
        )
    if obj["kind"] == "DataItemV1":
        data_item_v1json_value = typing.cast(DataItemV1JSONValue, obj["value"])
        return DataItemV1(
            DataItemV1Value(
                authorization_data=(
                    None
                    if data_item_v1json_value["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_json(
                        data_item_v1json_value["authorization_data"]
                    )
                ),
            )
        )
    if obj["kind"] == "CollectionItemV1":
        collection_item_v1json_value = typing.cast(
            CollectionItemV1JSONValue, obj["value"]
        )
        return CollectionItemV1(
            CollectionItemV1Value(
                authorization_data=(
                    None
                    if collection_item_v1json_value["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_json(
                        collection_item_v1json_value["authorization_data"]
                    )
                ),
            )
        )
    if obj["kind"] == "ProgrammableConfigItemV1":
        programmable_config_item_v1json_value = typing.cast(
            ProgrammableConfigItemV1JSONValue, obj["value"]
        )
        return ProgrammableConfigItemV1(
            ProgrammableConfigItemV1Value(
                authorization_data=(
                    None
                    if programmable_config_item_v1json_value["authorization_data"]
                    is None
                    else authorization_data.AuthorizationData.from_json(
                        programmable_config_item_v1json_value["authorization_data"]
                    )
                ),
            )
        )
    if obj["kind"] == "PrintDelegateV1":
        print_delegate_v1json_value = typing.cast(
            PrintDelegateV1JSONValue, obj["value"]
        )
        return PrintDelegateV1(
            PrintDelegateV1Value(
                authorization_data=(
                    None
                    if print_delegate_v1json_value["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_json(
                        print_delegate_v1json_value["authorization_data"]
                    )
                ),
            )
        )
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "CollectionV1"
    / borsh.CStruct(
        "authorization_data" / borsh.Option(authorization_data.AuthorizationData.layout)
    ),
    "SaleV1"
    / borsh.CStruct(
        "amount" / borsh.U64,
        "authorization_data"
        / borsh.Option(authorization_data.AuthorizationData.layout),
    ),
    "TransferV1"
    / borsh.CStruct(
        "amount" / borsh.U64,
        "authorization_data"
        / borsh.Option(authorization_data.AuthorizationData.layout),
    ),
    "DataV1"
    / borsh.CStruct(
        "authorization_data" / borsh.Option(authorization_data.AuthorizationData.layout)
    ),
    "UtilityV1"
    / borsh.CStruct(
        "amount" / borsh.U64,
        "authorization_data"
        / borsh.Option(authorization_data.AuthorizationData.layout),
    ),
    "StakingV1"
    / borsh.CStruct(
        "amount" / borsh.U64,
        "authorization_data"
        / borsh.Option(authorization_data.AuthorizationData.layout),
    ),
    "StandardV1" / borsh.CStruct("amount" / borsh.U64),
    "LockedTransferV1"
    / borsh.CStruct(
        "amount" / borsh.U64,
        "locked_address" / BorshPubkey,
        "authorization_data"
        / borsh.Option(authorization_data.AuthorizationData.layout),
    ),
    "ProgrammableConfigV1"
    / borsh.CStruct(
        "authorization_data" / borsh.Option(authorization_data.AuthorizationData.layout)
    ),
    "AuthorityItemV1"
    / borsh.CStruct(
        "authorization_data" / borsh.Option(authorization_data.AuthorizationData.layout)
    ),
    "DataItemV1"
    / borsh.CStruct(
        "authorization_data" / borsh.Option(authorization_data.AuthorizationData.layout)
    ),
    "CollectionItemV1"
    / borsh.CStruct(
        "authorization_data" / borsh.Option(authorization_data.AuthorizationData.layout)
    ),
    "ProgrammableConfigItemV1"
    / borsh.CStruct(
        "authorization_data" / borsh.Option(authorization_data.AuthorizationData.layout)
    ),
    "PrintDelegateV1"
    / borsh.CStruct(
        "authorization_data" / borsh.Option(authorization_data.AuthorizationData.layout)
    ),
)
