import sqlalchemy as sql
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


class Publisher(Base):
    __tablename__ = "publisher"

    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.VARCHAR(length=60), unique=True)

    def __str__(self):
        return f'id: {self.id}, Publisher: {self.name}'


class Shop(Base):
    __tablename__ = "shop"

    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.VARCHAR(length=60), unique=True)

    def __str__(self):
        return f'{self.id}, Shop: {self.name}'


class Book(Base):
    __tablename__ = "book"

    id = sql.Column(sql.Integer, primary_key=True)
    title = sql.Column(sql.VARCHAR(length=80), unique=True)
    id_publisher = sql.Column(sql.Integer, sql.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="book")

    def __str__(self):
        return f'{self.id}, Book title: {self.title}, publisher: {self.publisher_id}'


class Stock(Base):
    __tablename__ = "stock"

    id = sql.Column(sql.Integer, primary_key=True)
    id_book = sql.Column(sql.Integer, sql.ForeignKey("book.id"))
    id_shop = sql.Column(sql.Integer, sql.ForeignKey("shop.id"))
    count = sql.Column(sql.Integer, nullable=False)

    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")

    def __str__(self):
        return f'{self.id}, id_book: {self.id_book}, id_shop: {self.id_shop}, count: {self.count}'


class Sale(Base):
    __tablename__ = "sale"

    id = sql.Column(sql.Integer, primary_key=True)
    price = sql.Column(sql.Float, nullable=False)
    date_sale = sql.Column(sql.DATE, nullable=False)
    id_stock = sql.Column(sql.Integer, sql.ForeignKey("stock.id"))
    count = sql.Column(sql.Integer, nullable=False)

    stock = relationship(Stock, backref="stock")

    def __str__(self):
        return f'{self.id} sale_price: {self.price},' \
               f' id_stock: {self.id_stock}, count: {self.count}, date_sale: {self.date_sale}'
