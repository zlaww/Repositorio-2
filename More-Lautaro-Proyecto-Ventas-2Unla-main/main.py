from fastapi import FastAPI, status, HTTPException
from database import db_session, Producto, Venta
from schemas import ProductoCreate, VentaCreate, VentaResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "API REST de Ventas - UNLa"}


@app.get("/productos", status_code=status.HTTP_200_OK)
async def obtener_productos():
    try:
        productos = db_session.query(Producto).all()
        response = {"productos": productos}
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar obtener los productos: {e}"
        )


# --- RUTA ESTÁTICA ARRIBA (Para que no choque con {producto_id}) ---
@app.get("/productos/por-precio", status_code=status.HTTP_200_OK)
async def obtener_productos_por_precio():
    try:
        productos = db_session.query(Producto).order_by(Producto.precio.desc()).all()
        return {"productos": productos}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar obtener los productos por precio: {e}"
        )


@app.get("/productos/{producto_id}", status_code=status.HTTP_200_OK)
async def obtener_producto(producto_id: int):
    try:
        producto = db_session.query(Producto).filter_by(id=producto_id).first()

        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

        response = {"producto": producto}
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar obtener el producto con id {producto_id}: {e}"
        )


@app.post("/productos", status_code=status.HTTP_201_CREATED)
async def crear_producto(datos_producto: ProductoCreate):
    try:
        producto = db_session.query(Producto).filter_by(nombre=datos_producto.nombre).first()

        if producto:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El producto ya existe")

        producto = Producto(
            nombre=datos_producto.nombre,
            precio=datos_producto.precio
        )

        db_session.add(producto)
        db_session.commit()
        db_session.refresh(producto)

        response = {"producto": producto}
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar crear el producto: {e}"
        )


@app.put("/productos/{producto_id}", status_code=status.HTTP_200_OK)
async def actualizar_producto(producto_id: int, datos_producto: ProductoCreate):
    try:
        producto = db_session.query(Producto).filter_by(id=producto_id).first()

        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

        producto.nombre = datos_producto.nombre
        producto.precio = datos_producto.precio

        db_session.commit()
        db_session.refresh(producto)

        response = {"producto": producto}
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar actualizar el producto con id {producto_id}: {e}"
        )


@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_producto(producto_id: int):
    try:
        producto = db_session.query(Producto).filter_by(id=producto_id).first()

        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

        db_session.delete(producto)
        db_session.commit()

        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar eliminar el producto con id {producto_id}: {e}"
        )


@app.get("/ventas", status_code=status.HTTP_200_OK, response_model=list[VentaResponse])
async def obtener_ventas():
    try:
        ventas = db_session.query(Venta).all()
        return ventas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar obtener las ventas: {e}"
        )


# --- RUTA ESTÁTICA ARRIBA (Para que no choque con {venta_id}) ---
@app.get("/ventas/top5", status_code=status.HTTP_200_OK)
async def obtener_top5_ventas():
    try:
        top5_ventas = db_session.query(Venta).order_by(Venta.precio_total.desc()).limit(5).all()
        return {"top5_ventas": top5_ventas}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar obtener las top 5 ventas: {e}"
        )


@app.get("/ventas/{venta_id}", status_code=status.HTTP_200_OK, response_model=VentaResponse)
async def obtener_venta(venta_id: int):
    try:
        venta = db_session.query(Venta).filter_by(id=venta_id).first()

        if not venta:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada")

        return venta
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar obtener la venta con id {venta_id}: {e}"
        )


@app.post("/ventas", status_code=status.HTTP_201_CREATED, response_model=VentaResponse)
async def crear_venta(datos_venta: VentaCreate):
    try:
        producto = db_session.query(Producto).filter_by(id=datos_venta.id_producto).first()

        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El producto especificado no existe")

        venta = Venta(
            fecha=datos_venta.fecha,
            hora=datos_venta.hora,
            cantidad=datos_venta.cantidad,
            id_producto=datos_venta.id_producto,
            precio_total=(producto.precio * datos_venta.cantidad)
        )

        db_session.add(venta)
        db_session.commit()
        db_session.refresh(venta)

        return venta
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar crear la venta: {e}"
        )


@app.put("/ventas/{venta_id}", status_code=status.HTTP_200_OK, response_model=VentaResponse)
async def actualizar_venta(venta_id: int, datos_venta: VentaCreate):
    try:
        venta = db_session.query(Venta).filter_by(id=venta_id).first()

        if not venta:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada")

        producto = db_session.query(Producto).filter_by(id=datos_venta.id_producto).first()

        if not producto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El producto especificado no existe")

        venta.fecha = datos_venta.fecha
        venta.hora = datos_venta.hora
        venta.cantidad = datos_venta.cantidad
        venta.id_producto = datos_venta.id_producto
        venta.precio_total = producto.precio * datos_venta.cantidad

        db_session.commit()
        db_session.refresh(venta)

        return venta
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar actualizar la venta con id {venta_id}: {e}"
        )


@app.delete("/ventas/{venta_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_venta(venta_id: int):
    try:
        venta = db_session.query(Venta).filter_by(id=venta_id).first()

        if not venta:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venta no encontrada")

        db_session.delete(venta)
        db_session.commit()

        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar eliminar la venta con id {venta_id}: {e}"
        )