from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar
from contextlib import contextmanager
from sqlalchemy.orm import Session, sessionmaker

# 用于泛型约束的类型变量
ModelType = TypeVar("ModelType")
TableType = TypeVar("TableType")


class BaseDAO(ABC, Generic[ModelType, TableType]):
    """DAO基础接口"""
    
    def __init__(self, session_factory: sessionmaker):
        self.session_factory = session_factory

    @contextmanager
    def _get_session(self) -> Session:
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @abstractmethod
    def _to_model(self, table: TableType) -> ModelType:
        """将表实体转换为领域模型"""
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[ModelType]:
        """根据ID获取实体"""
        pass

    @abstractmethod
    def create(self, model: ModelType) -> ModelType:
        """创建实体"""
        pass

    @abstractmethod
    def update(self, model: ModelType) -> Optional[ModelType]:
        """更新实体"""
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        """删除实体"""
        pass
