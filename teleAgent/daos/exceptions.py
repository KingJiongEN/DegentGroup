class DAOError(Exception):
    """DAO层基础异常"""

    pass


class EntityNotFoundError(DAOError):
    """实体未找到异常"""

    pass


class DuplicateEntityError(DAOError):
    """实体重复异常"""

    pass
