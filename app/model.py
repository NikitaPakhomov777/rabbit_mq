from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Model(DeclarativeBase):
    pass


class Product(Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    count: Mapped[int]

