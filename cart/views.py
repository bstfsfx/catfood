from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from foods.models import Food
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required

def index(request):
    cart_total = 0
    foods_in_cart = []
    cart = request.session.get('cart', {})
    food_ids = list(cart.keys())
    if (food_ids != []):
        foods_in_cart = Food.objects.filter(id__in=food_ids)
        cart_total = calculate_cart_total(cart, foods_in_cart)

    template_data = {}
    template_data['title'] = 'Cart'
    template_data['foods_in_cart'] = foods_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html', {'template_data': template_data})

def add(request, id):
    get_object_or_404(Food, id=id)
    cart = request.session.get('cart', {})
    cart[id] = request.POST['quantity']
    request.session['cart'] = cart
    return redirect('cart.index')

def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    food_ids = list(cart.keys())

    if (food_ids == []):
        return redirect('cart.index')
    
    foods_in_cart = Food.objects.filter(id__in=food_ids)
    cart_total = calculate_cart_total(cart, foods_in_cart)

    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()

    for food in foods_in_cart:
        item = Item()
        item.food = food
        item.price = food.price
        item.order = order
        item.quantity = cart[str(food.id)]
        item.save()

    request.session['cart'] = {}
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    return render(request, 'cart/purchase.html', {'template_data': template_data})