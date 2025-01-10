from sqlalchemy import Column, DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.sql import func

from ..base import Base


class Wallet(Base):
    __tablename__ = "wallet_tab"

    address = Column(String(44), primary_key=True)
    owner_id = Column(String(100), nullable=False)
    owner_type = Column(Enum("user", "agent", name="owner_type"), nullable=False)
    balance = Column(Numeric(precision=18, scale=9), default=0)
    last_tx_at = Column(DateTime(timezone=True))
