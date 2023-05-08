import sqlalchemy.dialects.postgresql as postgres_types  # noqa: WPS301
from sqlalchemy import Column, DateTime, Sequence, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Model(Base):
    """Base model."""

    __abstract__ = True


class IdMixin(object):
    __tablename__ = ""
    id = Column(
        postgres_types.INTEGER(),
        Sequence(f"{__tablename__}_id_seq", start=0, increment=1),
        primary_key=True,
    )


class DateTimeModelMixin(object):
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class DeleteModelMixin(object):
    is_deleted = Column(postgres_types.BOOLEAN(), nullable=False, server_default="False")
