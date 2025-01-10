from sqlalchemy import JSON, Boolean, Column, Float, String

from ..base import Base


class AgentTable(Base):
    __tablename__ = "agent_tab"

    id = Column(String(100), primary_key=True, default=Base.generate_uuid)
    name = Column(String(100), nullable=False)
    personality = Column(String(200), nullable=False)
    art_style = Column(String(200))
    profile = Column(String(500))
    avatar = Column(String(200))
    configs = Column(JSON, nullable=False, default=dict)
    stats = Column(JSON, nullable=False, default=dict)
    wallet_address = Column(String(100), unique=True)
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Agent {self.name}>"
