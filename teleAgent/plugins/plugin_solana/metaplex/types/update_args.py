from __future__ import annotations
from . import (
    authorization_data,
    data,
    collection_toggle,
    uses_toggle,
    collection_details_toggle,
    rule_set_toggle,
    token_standard,
)
import typing
from dataclasses import dataclass
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import EnumForCodegen, BorshPubkey
import borsh_construct as borsh


class V1JSONValue(typing.TypedDict):
    new_update_authority: typing.Optional[str]
    data: typing.Optional[data.DataJSON]
    primary_sale_happened: typing.Optional[bool]
    is_mutable: typing.Optional[bool]
    collection: collection_toggle.CollectionToggleJSON
    collection_details: collection_details_toggle.CollectionDetailsToggleJSON
    uses: uses_toggle.UsesToggleJSON
    rule_set: rule_set_toggle.RuleSetToggleJSON
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class AsUpdateAuthorityV2JSONValue(typing.TypedDict):
    new_update_authority: typing.Optional[str]
    data: typing.Optional[data.DataJSON]
    primary_sale_happened: typing.Optional[bool]
    is_mutable: typing.Optional[bool]
    collection: collection_toggle.CollectionToggleJSON
    collection_details: collection_details_toggle.CollectionDetailsToggleJSON
    uses: uses_toggle.UsesToggleJSON
    rule_set: rule_set_toggle.RuleSetToggleJSON
    token_standard: typing.Optional[token_standard.TokenStandardJSON]
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class AsAuthorityItemDelegateV2JSONValue(typing.TypedDict):
    new_update_authority: typing.Optional[str]
    primary_sale_happened: typing.Optional[bool]
    is_mutable: typing.Optional[bool]
    token_standard: typing.Optional[token_standard.TokenStandardJSON]
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class AsCollectionDelegateV2JSONValue(typing.TypedDict):
    collection: collection_toggle.CollectionToggleJSON
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class AsDataDelegateV2JSONValue(typing.TypedDict):
    data: typing.Optional[data.DataJSON]
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class AsProgrammableConfigDelegateV2JSONValue(typing.TypedDict):
    rule_set: rule_set_toggle.RuleSetToggleJSON
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class AsDataItemDelegateV2JSONValue(typing.TypedDict):
    data: typing.Optional[data.DataJSON]
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class AsCollectionItemDelegateV2JSONValue(typing.TypedDict):
    collection: collection_toggle.CollectionToggleJSON
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class AsProgrammableConfigItemDelegateV2JSONValue(typing.TypedDict):
    rule_set: rule_set_toggle.RuleSetToggleJSON
    authorization_data: typing.Optional[authorization_data.AuthorizationDataJSON]


class V1Value(typing.TypedDict):
    new_update_authority: typing.Optional[Pubkey]
    data: typing.Optional[data.Data]
    primary_sale_happened: typing.Optional[bool]
    is_mutable: typing.Optional[bool]
    collection: collection_toggle.CollectionToggleKind
    collection_details: collection_details_toggle.CollectionDetailsToggleKind
    uses: uses_toggle.UsesToggleKind
    rule_set: rule_set_toggle.RuleSetToggleKind
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class AsUpdateAuthorityV2Value(typing.TypedDict):
    new_update_authority: typing.Optional[Pubkey]
    data: typing.Optional[data.Data]
    primary_sale_happened: typing.Optional[bool]
    is_mutable: typing.Optional[bool]
    collection: collection_toggle.CollectionToggleKind
    collection_details: collection_details_toggle.CollectionDetailsToggleKind
    uses: uses_toggle.UsesToggleKind
    rule_set: rule_set_toggle.RuleSetToggleKind
    token_standard: typing.Optional[token_standard.TokenStandardKind]
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class AsAuthorityItemDelegateV2Value(typing.TypedDict):
    new_update_authority: typing.Optional[Pubkey]
    primary_sale_happened: typing.Optional[bool]
    is_mutable: typing.Optional[bool]
    token_standard: typing.Optional[token_standard.TokenStandardKind]
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class AsCollectionDelegateV2Value(typing.TypedDict):
    collection: collection_toggle.CollectionToggleKind
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class AsDataDelegateV2Value(typing.TypedDict):
    data: typing.Optional[data.Data]
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class AsProgrammableConfigDelegateV2Value(typing.TypedDict):
    rule_set: rule_set_toggle.RuleSetToggleKind
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class AsDataItemDelegateV2Value(typing.TypedDict):
    data: typing.Optional[data.Data]
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class AsCollectionItemDelegateV2Value(typing.TypedDict):
    collection: collection_toggle.CollectionToggleKind
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class AsProgrammableConfigItemDelegateV2Value(typing.TypedDict):
    rule_set: rule_set_toggle.RuleSetToggleKind
    authorization_data: typing.Optional[authorization_data.AuthorizationData]


class V1JSON(typing.TypedDict):
    value: V1JSONValue
    kind: typing.Literal["V1"]


class AsUpdateAuthorityV2JSON(typing.TypedDict):
    value: AsUpdateAuthorityV2JSONValue
    kind: typing.Literal["AsUpdateAuthorityV2"]


class AsAuthorityItemDelegateV2JSON(typing.TypedDict):
    value: AsAuthorityItemDelegateV2JSONValue
    kind: typing.Literal["AsAuthorityItemDelegateV2"]


class AsCollectionDelegateV2JSON(typing.TypedDict):
    value: AsCollectionDelegateV2JSONValue
    kind: typing.Literal["AsCollectionDelegateV2"]


class AsDataDelegateV2JSON(typing.TypedDict):
    value: AsDataDelegateV2JSONValue
    kind: typing.Literal["AsDataDelegateV2"]


class AsProgrammableConfigDelegateV2JSON(typing.TypedDict):
    value: AsProgrammableConfigDelegateV2JSONValue
    kind: typing.Literal["AsProgrammableConfigDelegateV2"]


class AsDataItemDelegateV2JSON(typing.TypedDict):
    value: AsDataItemDelegateV2JSONValue
    kind: typing.Literal["AsDataItemDelegateV2"]


class AsCollectionItemDelegateV2JSON(typing.TypedDict):
    value: AsCollectionItemDelegateV2JSONValue
    kind: typing.Literal["AsCollectionItemDelegateV2"]


class AsProgrammableConfigItemDelegateV2JSON(typing.TypedDict):
    value: AsProgrammableConfigItemDelegateV2JSONValue
    kind: typing.Literal["AsProgrammableConfigItemDelegateV2"]


@dataclass
class V1:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "V1"
    value: V1Value

    def to_json(self) -> V1JSON:
        return V1JSON(
            kind="V1",
            value={
                "new_update_authority": (
                    None
                    if self.value["new_update_authority"] is None
                    else str(self.value["new_update_authority"])
                ),
                "data": (
                    None if self.value["data"] is None else self.value["data"].to_json()
                ),
                "primary_sale_happened": self.value["primary_sale_happened"],
                "is_mutable": self.value["is_mutable"],
                "collection": self.value["collection"].to_json(),
                "collection_details": self.value["collection_details"].to_json(),
                "uses": self.value["uses"].to_json(),
                "rule_set": self.value["rule_set"].to_json(),
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "V1": {
                "new_update_authority": self.value["new_update_authority"],
                "data": (
                    None
                    if self.value["data"] is None
                    else self.value["data"].to_encodable()
                ),
                "primary_sale_happened": self.value["primary_sale_happened"],
                "is_mutable": self.value["is_mutable"],
                "collection": self.value["collection"].to_encodable(),
                "collection_details": self.value["collection_details"].to_encodable(),
                "uses": self.value["uses"].to_encodable(),
                "rule_set": self.value["rule_set"].to_encodable(),
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class AsUpdateAuthorityV2:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "AsUpdateAuthorityV2"
    value: AsUpdateAuthorityV2Value

    def to_json(self) -> AsUpdateAuthorityV2JSON:
        return AsUpdateAuthorityV2JSON(
            kind="AsUpdateAuthorityV2",
            value={
                "new_update_authority": (
                    None
                    if self.value["new_update_authority"] is None
                    else str(self.value["new_update_authority"])
                ),
                "data": (
                    None if self.value["data"] is None else self.value["data"].to_json()
                ),
                "primary_sale_happened": self.value["primary_sale_happened"],
                "is_mutable": self.value["is_mutable"],
                "collection": self.value["collection"].to_json(),
                "collection_details": self.value["collection_details"].to_json(),
                "uses": self.value["uses"].to_json(),
                "rule_set": self.value["rule_set"].to_json(),
                "token_standard": (
                    None
                    if self.value["token_standard"] is None
                    else self.value["token_standard"].to_json()
                ),
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "AsUpdateAuthorityV2": {
                "new_update_authority": self.value["new_update_authority"],
                "data": (
                    None
                    if self.value["data"] is None
                    else self.value["data"].to_encodable()
                ),
                "primary_sale_happened": self.value["primary_sale_happened"],
                "is_mutable": self.value["is_mutable"],
                "collection": self.value["collection"].to_encodable(),
                "collection_details": self.value["collection_details"].to_encodable(),
                "uses": self.value["uses"].to_encodable(),
                "rule_set": self.value["rule_set"].to_encodable(),
                "token_standard": (
                    None
                    if self.value["token_standard"] is None
                    else self.value["token_standard"].to_encodable()
                ),
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class AsAuthorityItemDelegateV2:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "AsAuthorityItemDelegateV2"
    value: AsAuthorityItemDelegateV2Value

    def to_json(self) -> AsAuthorityItemDelegateV2JSON:
        return AsAuthorityItemDelegateV2JSON(
            kind="AsAuthorityItemDelegateV2",
            value={
                "new_update_authority": (
                    None
                    if self.value["new_update_authority"] is None
                    else str(self.value["new_update_authority"])
                ),
                "primary_sale_happened": self.value["primary_sale_happened"],
                "is_mutable": self.value["is_mutable"],
                "token_standard": (
                    None
                    if self.value["token_standard"] is None
                    else self.value["token_standard"].to_json()
                ),
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "AsAuthorityItemDelegateV2": {
                "new_update_authority": self.value["new_update_authority"],
                "primary_sale_happened": self.value["primary_sale_happened"],
                "is_mutable": self.value["is_mutable"],
                "token_standard": (
                    None
                    if self.value["token_standard"] is None
                    else self.value["token_standard"].to_encodable()
                ),
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class AsCollectionDelegateV2:
    discriminator: typing.ClassVar = 3
    kind: typing.ClassVar = "AsCollectionDelegateV2"
    value: AsCollectionDelegateV2Value

    def to_json(self) -> AsCollectionDelegateV2JSON:
        return AsCollectionDelegateV2JSON(
            kind="AsCollectionDelegateV2",
            value={
                "collection": self.value["collection"].to_json(),
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "AsCollectionDelegateV2": {
                "collection": self.value["collection"].to_encodable(),
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class AsDataDelegateV2:
    discriminator: typing.ClassVar = 4
    kind: typing.ClassVar = "AsDataDelegateV2"
    value: AsDataDelegateV2Value

    def to_json(self) -> AsDataDelegateV2JSON:
        return AsDataDelegateV2JSON(
            kind="AsDataDelegateV2",
            value={
                "data": (
                    None if self.value["data"] is None else self.value["data"].to_json()
                ),
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "AsDataDelegateV2": {
                "data": (
                    None
                    if self.value["data"] is None
                    else self.value["data"].to_encodable()
                ),
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class AsProgrammableConfigDelegateV2:
    discriminator: typing.ClassVar = 5
    kind: typing.ClassVar = "AsProgrammableConfigDelegateV2"
    value: AsProgrammableConfigDelegateV2Value

    def to_json(self) -> AsProgrammableConfigDelegateV2JSON:
        return AsProgrammableConfigDelegateV2JSON(
            kind="AsProgrammableConfigDelegateV2",
            value={
                "rule_set": self.value["rule_set"].to_json(),
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "AsProgrammableConfigDelegateV2": {
                "rule_set": self.value["rule_set"].to_encodable(),
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class AsDataItemDelegateV2:
    discriminator: typing.ClassVar = 6
    kind: typing.ClassVar = "AsDataItemDelegateV2"
    value: AsDataItemDelegateV2Value

    def to_json(self) -> AsDataItemDelegateV2JSON:
        return AsDataItemDelegateV2JSON(
            kind="AsDataItemDelegateV2",
            value={
                "data": (
                    None if self.value["data"] is None else self.value["data"].to_json()
                ),
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "AsDataItemDelegateV2": {
                "data": (
                    None
                    if self.value["data"] is None
                    else self.value["data"].to_encodable()
                ),
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class AsCollectionItemDelegateV2:
    discriminator: typing.ClassVar = 7
    kind: typing.ClassVar = "AsCollectionItemDelegateV2"
    value: AsCollectionItemDelegateV2Value

    def to_json(self) -> AsCollectionItemDelegateV2JSON:
        return AsCollectionItemDelegateV2JSON(
            kind="AsCollectionItemDelegateV2",
            value={
                "collection": self.value["collection"].to_json(),
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "AsCollectionItemDelegateV2": {
                "collection": self.value["collection"].to_encodable(),
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


@dataclass
class AsProgrammableConfigItemDelegateV2:
    discriminator: typing.ClassVar = 8
    kind: typing.ClassVar = "AsProgrammableConfigItemDelegateV2"
    value: AsProgrammableConfigItemDelegateV2Value

    def to_json(self) -> AsProgrammableConfigItemDelegateV2JSON:
        return AsProgrammableConfigItemDelegateV2JSON(
            kind="AsProgrammableConfigItemDelegateV2",
            value={
                "rule_set": self.value["rule_set"].to_json(),
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_json()
                ),
            },
        )

    def to_encodable(self) -> dict:
        return {
            "AsProgrammableConfigItemDelegateV2": {
                "rule_set": self.value["rule_set"].to_encodable(),
                "authorization_data": (
                    None
                    if self.value["authorization_data"] is None
                    else self.value["authorization_data"].to_encodable()
                ),
            },
        }


UpdateArgsKind = typing.Union[
    V1,
    AsUpdateAuthorityV2,
    AsAuthorityItemDelegateV2,
    AsCollectionDelegateV2,
    AsDataDelegateV2,
    AsProgrammableConfigDelegateV2,
    AsDataItemDelegateV2,
    AsCollectionItemDelegateV2,
    AsProgrammableConfigItemDelegateV2,
]
UpdateArgsJSON = typing.Union[
    V1JSON,
    AsUpdateAuthorityV2JSON,
    AsAuthorityItemDelegateV2JSON,
    AsCollectionDelegateV2JSON,
    AsDataDelegateV2JSON,
    AsProgrammableConfigDelegateV2JSON,
    AsDataItemDelegateV2JSON,
    AsCollectionItemDelegateV2JSON,
    AsProgrammableConfigItemDelegateV2JSON,
]


def from_decoded(obj: dict) -> UpdateArgsKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "V1" in obj:
        val = obj["V1"]
        return V1(
            V1Value(
                new_update_authority=val["new_update_authority"],
                data=(
                    None if val["data"] is None else data.Data.from_decoded(val["data"])
                ),
                primary_sale_happened=val["primary_sale_happened"],
                is_mutable=val["is_mutable"],
                collection=collection_toggle.from_decoded(val["collection"]),
                collection_details=collection_details_toggle.from_decoded(
                    val["collection_details"]
                ),
                uses=uses_toggle.from_decoded(val["uses"]),
                rule_set=rule_set_toggle.from_decoded(val["rule_set"]),
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "AsUpdateAuthorityV2" in obj:
        val = obj["AsUpdateAuthorityV2"]
        return AsUpdateAuthorityV2(
            AsUpdateAuthorityV2Value(
                new_update_authority=val["new_update_authority"],
                data=(
                    None if val["data"] is None else data.Data.from_decoded(val["data"])
                ),
                primary_sale_happened=val["primary_sale_happened"],
                is_mutable=val["is_mutable"],
                collection=collection_toggle.from_decoded(val["collection"]),
                collection_details=collection_details_toggle.from_decoded(
                    val["collection_details"]
                ),
                uses=uses_toggle.from_decoded(val["uses"]),
                rule_set=rule_set_toggle.from_decoded(val["rule_set"]),
                token_standard=(
                    None
                    if val["token_standard"] is None
                    else token_standard.from_decoded(val["token_standard"])
                ),
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "AsAuthorityItemDelegateV2" in obj:
        val = obj["AsAuthorityItemDelegateV2"]
        return AsAuthorityItemDelegateV2(
            AsAuthorityItemDelegateV2Value(
                new_update_authority=val["new_update_authority"],
                primary_sale_happened=val["primary_sale_happened"],
                is_mutable=val["is_mutable"],
                token_standard=(
                    None
                    if val["token_standard"] is None
                    else token_standard.from_decoded(val["token_standard"])
                ),
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "AsCollectionDelegateV2" in obj:
        val = obj["AsCollectionDelegateV2"]
        return AsCollectionDelegateV2(
            AsCollectionDelegateV2Value(
                collection=collection_toggle.from_decoded(val["collection"]),
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "AsDataDelegateV2" in obj:
        val = obj["AsDataDelegateV2"]
        return AsDataDelegateV2(
            AsDataDelegateV2Value(
                data=(
                    None if val["data"] is None else data.Data.from_decoded(val["data"])
                ),
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "AsProgrammableConfigDelegateV2" in obj:
        val = obj["AsProgrammableConfigDelegateV2"]
        return AsProgrammableConfigDelegateV2(
            AsProgrammableConfigDelegateV2Value(
                rule_set=rule_set_toggle.from_decoded(val["rule_set"]),
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "AsDataItemDelegateV2" in obj:
        val = obj["AsDataItemDelegateV2"]
        return AsDataItemDelegateV2(
            AsDataItemDelegateV2Value(
                data=(
                    None if val["data"] is None else data.Data.from_decoded(val["data"])
                ),
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "AsCollectionItemDelegateV2" in obj:
        val = obj["AsCollectionItemDelegateV2"]
        return AsCollectionItemDelegateV2(
            AsCollectionItemDelegateV2Value(
                collection=collection_toggle.from_decoded(val["collection"]),
                authorization_data=(
                    None
                    if val["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_decoded(
                        val["authorization_data"]
                    )
                ),
            )
        )
    if "AsProgrammableConfigItemDelegateV2" in obj:
        val = obj["AsProgrammableConfigItemDelegateV2"]
        return AsProgrammableConfigItemDelegateV2(
            AsProgrammableConfigItemDelegateV2Value(
                rule_set=rule_set_toggle.from_decoded(val["rule_set"]),
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


def from_json(obj: UpdateArgsJSON) -> UpdateArgsKind:
    if obj["kind"] == "V1":
        v1json_value = typing.cast(V1JSONValue, obj["value"])
        return V1(
            V1Value(
                new_update_authority=(
                    None
                    if v1json_value["new_update_authority"] is None
                    else Pubkey.from_string(v1json_value["new_update_authority"])
                ),
                data=(
                    None
                    if v1json_value["data"] is None
                    else data.Data.from_json(v1json_value["data"])
                ),
                primary_sale_happened=v1json_value["primary_sale_happened"],
                is_mutable=v1json_value["is_mutable"],
                collection=collection_toggle.from_json(v1json_value["collection"]),
                collection_details=collection_details_toggle.from_json(
                    v1json_value["collection_details"]
                ),
                uses=uses_toggle.from_json(v1json_value["uses"]),
                rule_set=rule_set_toggle.from_json(v1json_value["rule_set"]),
                authorization_data=(
                    None
                    if v1json_value["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_json(
                        v1json_value["authorization_data"]
                    )
                ),
            )
        )
    if obj["kind"] == "AsUpdateAuthorityV2":
        as_update_authority_v2json_value = typing.cast(
            AsUpdateAuthorityV2JSONValue, obj["value"]
        )
        return AsUpdateAuthorityV2(
            AsUpdateAuthorityV2Value(
                new_update_authority=(
                    None
                    if as_update_authority_v2json_value["new_update_authority"] is None
                    else Pubkey.from_string(
                        as_update_authority_v2json_value["new_update_authority"]
                    )
                ),
                data=(
                    None
                    if as_update_authority_v2json_value["data"] is None
                    else data.Data.from_json(as_update_authority_v2json_value["data"])
                ),
                primary_sale_happened=as_update_authority_v2json_value[
                    "primary_sale_happened"
                ],
                is_mutable=as_update_authority_v2json_value["is_mutable"],
                collection=collection_toggle.from_json(
                    as_update_authority_v2json_value["collection"]
                ),
                collection_details=collection_details_toggle.from_json(
                    as_update_authority_v2json_value["collection_details"]
                ),
                uses=uses_toggle.from_json(as_update_authority_v2json_value["uses"]),
                rule_set=rule_set_toggle.from_json(
                    as_update_authority_v2json_value["rule_set"]
                ),
                token_standard=(
                    None
                    if as_update_authority_v2json_value["token_standard"] is None
                    else token_standard.from_json(
                        as_update_authority_v2json_value["token_standard"]
                    )
                ),
                authorization_data=(
                    None
                    if as_update_authority_v2json_value["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_json(
                        as_update_authority_v2json_value["authorization_data"]
                    )
                ),
            )
        )
    if obj["kind"] == "AsAuthorityItemDelegateV2":
        as_authority_item_delegate_v2json_value = typing.cast(
            AsAuthorityItemDelegateV2JSONValue, obj["value"]
        )
        return AsAuthorityItemDelegateV2(
            AsAuthorityItemDelegateV2Value(
                new_update_authority=(
                    None
                    if as_authority_item_delegate_v2json_value["new_update_authority"]
                    is None
                    else Pubkey.from_string(
                        as_authority_item_delegate_v2json_value["new_update_authority"]
                    )
                ),
                primary_sale_happened=as_authority_item_delegate_v2json_value[
                    "primary_sale_happened"
                ],
                is_mutable=as_authority_item_delegate_v2json_value["is_mutable"],
                token_standard=(
                    None
                    if as_authority_item_delegate_v2json_value["token_standard"] is None
                    else token_standard.from_json(
                        as_authority_item_delegate_v2json_value["token_standard"]
                    )
                ),
                authorization_data=(
                    None
                    if as_authority_item_delegate_v2json_value["authorization_data"]
                    is None
                    else authorization_data.AuthorizationData.from_json(
                        as_authority_item_delegate_v2json_value["authorization_data"]
                    )
                ),
            )
        )
    if obj["kind"] == "AsCollectionDelegateV2":
        as_collection_delegate_v2json_value = typing.cast(
            AsCollectionDelegateV2JSONValue, obj["value"]
        )
        return AsCollectionDelegateV2(
            AsCollectionDelegateV2Value(
                collection=collection_toggle.from_json(
                    as_collection_delegate_v2json_value["collection"]
                ),
                authorization_data=(
                    None
                    if as_collection_delegate_v2json_value["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_json(
                        as_collection_delegate_v2json_value["authorization_data"]
                    )
                ),
            )
        )
    if obj["kind"] == "AsDataDelegateV2":
        as_data_delegate_v2json_value = typing.cast(
            AsDataDelegateV2JSONValue, obj["value"]
        )
        return AsDataDelegateV2(
            AsDataDelegateV2Value(
                data=(
                    None
                    if as_data_delegate_v2json_value["data"] is None
                    else data.Data.from_json(as_data_delegate_v2json_value["data"])
                ),
                authorization_data=(
                    None
                    if as_data_delegate_v2json_value["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_json(
                        as_data_delegate_v2json_value["authorization_data"]
                    )
                ),
            )
        )
    if obj["kind"] == "AsProgrammableConfigDelegateV2":
        as_programmable_config_delegate_v2json_value = typing.cast(
            AsProgrammableConfigDelegateV2JSONValue, obj["value"]
        )
        return AsProgrammableConfigDelegateV2(
            AsProgrammableConfigDelegateV2Value(
                rule_set=rule_set_toggle.from_json(
                    as_programmable_config_delegate_v2json_value["rule_set"]
                ),
                authorization_data=(
                    None
                    if as_programmable_config_delegate_v2json_value[
                        "authorization_data"
                    ]
                    is None
                    else authorization_data.AuthorizationData.from_json(
                        as_programmable_config_delegate_v2json_value[
                            "authorization_data"
                        ]
                    )
                ),
            )
        )
    if obj["kind"] == "AsDataItemDelegateV2":
        as_data_item_delegate_v2json_value = typing.cast(
            AsDataItemDelegateV2JSONValue, obj["value"]
        )
        return AsDataItemDelegateV2(
            AsDataItemDelegateV2Value(
                data=(
                    None
                    if as_data_item_delegate_v2json_value["data"] is None
                    else data.Data.from_json(as_data_item_delegate_v2json_value["data"])
                ),
                authorization_data=(
                    None
                    if as_data_item_delegate_v2json_value["authorization_data"] is None
                    else authorization_data.AuthorizationData.from_json(
                        as_data_item_delegate_v2json_value["authorization_data"]
                    )
                ),
            )
        )
    if obj["kind"] == "AsCollectionItemDelegateV2":
        as_collection_item_delegate_v2json_value = typing.cast(
            AsCollectionItemDelegateV2JSONValue, obj["value"]
        )
        return AsCollectionItemDelegateV2(
            AsCollectionItemDelegateV2Value(
                collection=collection_toggle.from_json(
                    as_collection_item_delegate_v2json_value["collection"]
                ),
                authorization_data=(
                    None
                    if as_collection_item_delegate_v2json_value["authorization_data"]
                    is None
                    else authorization_data.AuthorizationData.from_json(
                        as_collection_item_delegate_v2json_value["authorization_data"]
                    )
                ),
            )
        )
    if obj["kind"] == "AsProgrammableConfigItemDelegateV2":
        as_programmable_config_item_delegate_v2json_value = typing.cast(
            AsProgrammableConfigItemDelegateV2JSONValue, obj["value"]
        )
        return AsProgrammableConfigItemDelegateV2(
            AsProgrammableConfigItemDelegateV2Value(
                rule_set=rule_set_toggle.from_json(
                    as_programmable_config_item_delegate_v2json_value["rule_set"]
                ),
                authorization_data=(
                    None
                    if as_programmable_config_item_delegate_v2json_value[
                        "authorization_data"
                    ]
                    is None
                    else authorization_data.AuthorizationData.from_json(
                        as_programmable_config_item_delegate_v2json_value[
                            "authorization_data"
                        ]
                    )
                ),
            )
        )
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "V1"
    / borsh.CStruct(
        "new_update_authority" / borsh.Option(BorshPubkey),
        "data" / borsh.Option(data.Data.layout),
        "primary_sale_happened" / borsh.Option(borsh.Bool),
        "is_mutable" / borsh.Option(borsh.Bool),
        "collection" / collection_toggle.layout,
        "collection_details" / collection_details_toggle.layout,
        "uses" / uses_toggle.layout,
        "rule_set" / rule_set_toggle.layout,
        "authorization_data"
        / borsh.Option(authorization_data.AuthorizationData.layout),
    ),
    "AsUpdateAuthorityV2"
    / borsh.CStruct(
        "new_update_authority" / borsh.Option(BorshPubkey),
        "data" / borsh.Option(data.Data.layout),
        "primary_sale_happened" / borsh.Option(borsh.Bool),
        "is_mutable" / borsh.Option(borsh.Bool),
        "collection" / collection_toggle.layout,
        "collection_details" / collection_details_toggle.layout,
        "uses" / uses_toggle.layout,
        "rule_set" / rule_set_toggle.layout,
        "token_standard" / borsh.Option(token_standard.layout),
        "authorization_data"
        / borsh.Option(authorization_data.AuthorizationData.layout),
    ),
    "AsAuthorityItemDelegateV2"
    / borsh.CStruct(
        "new_update_authority" / borsh.Option(BorshPubkey),
        "primary_sale_happened" / borsh.Option(borsh.Bool),
        "is_mutable" / borsh.Option(borsh.Bool),
        "token_standard" / borsh.Option(token_standard.layout),
        "authorization_data"
        / borsh.Option(authorization_data.AuthorizationData.layout),
    ),
    "AsCollectionDelegateV2"
    / borsh.CStruct(
        "collection" / collection_toggle.layout,
        "authorization_data"
        / borsh.Option(authorization_data.AuthorizationData.layout),
    ),
    "AsDataDelegateV2"
    / borsh.CStruct(
        "data" / borsh.Option(data.Data.layout),
        "authorization_data"
        / borsh.Option(authorization_data.AuthorizationData.layout),
    ),
    "AsProgrammableConfigDelegateV2"
    / borsh.CStruct(
        "rule_set" / rule_set_toggle.layout,
        "authorization_data"
        / borsh.Option(authorization_data.AuthorizationData.layout),
    ),
    "AsDataItemDelegateV2"
    / borsh.CStruct(
        "data" / borsh.Option(data.Data.layout),
        "authorization_data"
        / borsh.Option(authorization_data.AuthorizationData.layout),
    ),
    "AsCollectionItemDelegateV2"
    / borsh.CStruct(
        "collection" / collection_toggle.layout,
        "authorization_data"
        / borsh.Option(authorization_data.AuthorizationData.layout),
    ),
    "AsProgrammableConfigItemDelegateV2"
    / borsh.CStruct(
        "rule_set" / rule_set_toggle.layout,
        "authorization_data"
        / borsh.Option(authorization_data.AuthorizationData.layout),
    ),
)
