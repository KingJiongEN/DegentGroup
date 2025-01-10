from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container, Construct
import borsh_construct as borsh


class ProofInfoJSON(typing.TypedDict):
    proof: list[list[int]]


@dataclass
class ProofInfo:
    layout: typing.ClassVar = borsh.CStruct(
        "proof" / borsh.Vec(typing.cast(Construct, borsh.U8[32]))
    )
    proof: list[list[int]]

    @classmethod
    def from_decoded(cls, obj: Container) -> "ProofInfo":
        return cls(proof=obj.proof)

    def to_encodable(self) -> dict[str, typing.Any]:
        return {"proof": self.proof}

    def to_json(self) -> ProofInfoJSON:
        return {"proof": self.proof}

    @classmethod
    def from_json(cls, obj: ProofInfoJSON) -> "ProofInfo":
        return cls(proof=obj["proof"])
