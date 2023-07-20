def valores_carrito(request):
    carrito = request.session.get('carrito', [])
    cantidad_items = len(carrito)
    total = 0.00
    for item in carrito:
        total = total + item["subtotal"]
    return {"carrito_items": cantidad_items, 'carrito_total': total, 'carrito': carrito}

