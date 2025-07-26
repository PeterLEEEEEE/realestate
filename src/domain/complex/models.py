from sqlalchemy import Integer, String, Boolean, VARCHAR, Float
from sqlalchemy.sql import expression
from sqlalchemy.orm import Mapped, mapped_column
from src.db.postgres.conn import Base
from src.db.mixins.timestamp_mixin import TimestampMixin
from src.db.mixins.softdelete_mixin import SoftDeleteMixin


class Complex(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "complexes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    complex_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="APT")  # e.g., "APARTMENT
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)  # 가격
    size: Mapped[float] = mapped_column(Float, nullable=False)  # 면적

    
class ComplexComment(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "complex_comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    complex_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(VARCHAR(500), nullable=False)  # 댓글 내용
    rating: Mapped[float] = mapped_column(Float, nullable=False)  # 평점
