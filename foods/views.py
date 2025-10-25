from django.shortcuts import render, redirect, get_object_or_404
from .models import Food, Review
from django.contrib.auth.decorators import login_required

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        foods = Food.objects.filter(name__icontains=search_term)
    else:
        foods = Food.objects.all()

    template_data = {}
    template_data['title'] = 'Foods'
    template_data['foods'] = foods
    return render(request, 'foods/index.html', {'template_data': template_data})

def show(request, id):
    food = Food.objects.get(id=id)
    reviews = Review.objects.filter(food=food)

    template_data = {}
    template_data['title'] = food.name
    template_data['food'] = food
    template_data['reviews'] = reviews
    return render(request, 'foods/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        food = Food.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.food = food
        review.user = request.user
        review.save()
        return redirect('foods.show', id=id)
    else:
        return redirect('foods.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('foods.show', id=id)

    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'foods/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('foods.show', id=id)
    else:
        return redirect('foods.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('foods.show', id=id)