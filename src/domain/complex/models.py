from sqlalchemy import Integer, String, Boolean, VARCHAR, Float
from sqlalchemy.sql import expression
from sqlalchemy.orm import Mapped, mapped_column
from src.db.postgres.conn import Base
from src.db.mixins.timestamp_mixin import TimestampMixin



class Complex(Base, TimestampMixin):
    __tablename__ = "complexes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    complex_type: Mapped[str] = mapped_column(
        String(50), nullable=False, default="APT")  # e.g., "APARTMENT
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)  # 가격
    size: Mapped[float] = mapped_column(Float, nullable=False)  # 면적
    is_available: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=expression.true()  # default=True
    )