from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Time, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker

engine = create_engine("sqlite:///ventas.db")
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class Producto(Base):
  __tablename__ = "productos"

  id = Column(Integer, primary_key=True)
  nombre = Column(String(100), nullable=False)
  precio = Column(Float, nullable=False)

  ventas = relationship("Venta", back_populates="producto")


class Venta(Base):
  __tablename__ = "ventas"

  id = Column(Integer, primary_key=True)
  fecha = Column(Date, nullable=False)
  hora = Column(Time, nullable=False)
  cantidad = Column(Integer, nullable=False)
  id_producto = Column(Integer, ForeignKey("productos.id"), nullable=False)
  precio_total = Column(Float, nullable=False)

  producto = relationship("Producto", back_populates="ventas")


Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=True)