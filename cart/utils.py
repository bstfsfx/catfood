def calculate_cart_total(cart, foods_in_cart):
    total = 0
    for food in foods_in_cart:
        quantity = cart[str(food.id)]
        total += food.price * int(quantity)
    return total