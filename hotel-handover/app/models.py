from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, nullable=False)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    end_time = Column(TIMESTAMP(timezone=True), nullable=True)
    status = Column(String, nullable=False, server_default='open')  # open | closed

    opened_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    closed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    opener = relationship("Users", foreign_keys=[opened_by])
    closer = relationship("Users", foreign_keys=[closed_by])


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, nullable=False)
    shift_id = Column(Integer, ForeignKey("shifts.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)

    acknowledged = Column(Boolean, nullable=False, server_default='False')
    acknowledged_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    acknowledged_at = Column(TIMESTAMP(timezone=True), nullable=True)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    shift = relationship("Shift")
    author = relationship("Users", foreign_keys=[author_id])
    acknowledger = relationship("Users", foreign_keys=[acknowledged_by])
