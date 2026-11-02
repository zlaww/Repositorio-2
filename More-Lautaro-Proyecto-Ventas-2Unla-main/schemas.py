from datetime import date, time
from pydantic import BaseModel

class ProductoCreate(BaseModel):
  nombre: str
  precio: float

  class Config:
    from_attributes = True


class ProductoResponse(BaseModel):
  id: int
  nombre: str
  precio: float

  class Config:
    from_attributes = True


class ListaProductosResponse(BaseModel):
  productos: list[ProductoResponse]


class UnProductoResponse(BaseModel):
  producto: ProductoResponse

class VentaCreate(BaseModel):
  fecha: date
  hora: time
  cantidad: int
  id_producto: int

  class Config:
    from_attributes = True


class VentaResponse(BaseModel):
  id: int
  fecha: date
  hora: time
  cantidad: int
  producto: ProductoResponse
  precio_total: float

  class Config:
    from_attributes = True



class ListaVentasResponse(BaseModel):
  ventas: list[VentaResponse]


class UnaVentaResponse(BaseModel):
  venta: VentaResponse