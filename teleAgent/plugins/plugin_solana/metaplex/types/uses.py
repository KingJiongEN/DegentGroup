from __future__ import annotations
from . import (
    use_method,
)
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class UsesJSON(typing.TypedDict):
    use_method: use_method.UseMethodJSON
    remaining: int
    total: int


@dataclass
class Uses:
    layout: typing.ClassVar = borsh.CStruct(
        "use_method" / use_method.layout, "remaining" / borsh.U64, "total" / borsh.U64
    )
    use_method: use_method.UseMethodKind
    remaining: int
    total: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "Uses":
        return cls(
            use_method=use_method.from_decoded(obj.use_method),
            remaining=obj.remaining,
            total=obj.total,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "use_method": self.use_method.to_encodable(),
            "remaining": self.remaining,
            "total": self.total,
        }

    def to_json(self) -> UsesJSON:
        return {
            "use_method": self.use_method.to_json(),
            "remaining": self.remaining,
            "total": self.total,
        }

    @classmethod
    def from_json(cls, obj: UsesJSON) -> "Uses":
        return cls(
            use_method=use_method.from_json(obj["use_method"]),
            remaining=obj["remaining"],
            total=obj["total"],
        )
