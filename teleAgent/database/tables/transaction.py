from sqlalchemy import Column, DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.sql import func

from ..base import Base


class Transaction(Base):
    __tablename__ = "transaction_tab"

    id = Column(String(100), primary_key=True)
    from_address = Column(String(44), ForeignKey("wallet_tab.address"), nullable=False)
    to_address = Column(String(44), ForeignKey("wallet_tab.address"), nullable=False)
    amount = Column(Numeric(precision=18, scale=9), nullable=False)
    status = Column(
        Enum("pending", "completed", "failed", name="tx_status"), nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
