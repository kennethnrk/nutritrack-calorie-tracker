from django.shortcuts import render, redirect
from .models import Food, Consume, Goal, FashionItem
import requests
from bs4 import BeautifulSoup
# Create your views here.
from django.db import connection


def nutrition(request):
    user = request.user
    if request.method == "POST":
        food_consumed = request.POST['food_consumed']
        consume = Food.objects.get(name=food_consumed)
        consume = Consume(user=user, food_consumed=consume)
        consume.save()
        foods = Food.objects.all()

    else:
        foods = Food.objects.all()
    goal = Goal.objects.get(user=user)
    consumed_food = Consume.objects.filter(user=request.user)

    return render(request, 'myapp/nutrition.html', {'foods': foods, 'consumed_food': consumed_food, 'calories':goal.calories})

def index(request):
    return render(request, 'myapp/index.html')

def updategoal(request):
    user = request.user
    goal = Goal.objects.get(user=user)
    if request.method == "POST":
        calories = request.POST['calories']
        carbs = request.POST['carbs']
        fats = request.POST['fats']
        protein = request.POST['protein']
        goal.calories = calories
        goal.carbs = carbs
        goal.fats = fats
        goal.protein = protein
        goal.save()
        return redirect('/nutrition')
    else:
        
        
        return render(request, 'myapp/updategoal.html', { 'carbs' : goal.carbs, 'protein' : goal.protein , 'fats' : goal.fats,  'calories' : goal.calories })

def delete_consume(request, id):
    consumed_food = Consume.objects.get(id=id)
    if request.method == 'POST':
        consumed_food.delete()
        return redirect('/nutrition')
    return render(request, 'myapp/delete.html')

def fashion_endpoint(request):
    FashionItem.objects.all().delete()
    page = requests.get("https://www.vogue.in/fashion/fashion-trends")
    soup = BeautifulSoup(page.content, "html.parser")

    images = soup.find_all('img', class_='ResponsiveImageContainer-eybHBd')
    images = images[2:-1]
    captions  = soup.find_all('h2', class_='SummaryItemHedBase-hiFYpQ')
    datewritten = soup.find_all('time',class_="summary-item__publish-date")
    author = soup.find_all('span', class_="byline__name")
    vogue = list()
    for i in range(len(images)):
        a = {'caption': captions[i].getText(), 'image': images[i]['src']}
        f = FashionItem(caption = captions[i].getText(), image=images[i]['src'], datewritten= datewritten[i].getText(), author=author[i].getText())

        vogue.append(a)
        f.save()
    
    return render(request, 'myapp/fashion.html', {'fashion': vogue})

