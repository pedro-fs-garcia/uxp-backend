from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import declared_attr

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True # não cria tabela
    @classmethod
    def classname(cls):
        return cls.__name__


class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
            name='created_at',
        )
    
    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
            name='updated_at',
        )