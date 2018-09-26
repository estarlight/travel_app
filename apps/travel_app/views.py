from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt
import json
from django.db.models import Count
# Create your views here.

def index(request):

    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
    else: 
        user = None 
    
    context = {
        'user' : user
    }
    return render (request, 'travel_app/index.html', context)

def login_reg(request):

    return render(request, 'travel_app/login_reg.html')

def register_process(request, methods='POST'):
    
    request.session['errors'] = False

    valid = User.objects.user_validation(request.POST)
    if 'errors' in valid:
        for e in valid['errors']:
            messages.error(request, e, extra_tags='register')
        return redirect('/login_reg')
    
    if len(request.POST['password']) < 8:
        request.session['errors'] = True
        messages.error(request, 'Password must be at least 8 characters.')
    if not request.POST['password'] == request.POST['password_confirmation']:
        request.session['errors'] = True
        messages.error(request, 'Password and password confirmation do not match')

    if request.session['errors']:
        return redirect('/login_reg')

    try:
        user = User.objects.get(email=request.POST['email'])
        messages.error(request, 'Account with this email exists. Please login.')
        return redirect('/login_reg')

    except User.DoesNotExist:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        correct_hashed_pw = hashed_pw.decode('utf-8')

        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=correct_hashed_pw)
        request.session['user_id'] = user.id

    return redirect('/')    


def login_process(request, methods='POST'):

    try: 
        user = User.objects.get(email=request.POST['email'])
    except User.DoesNotExist:
        messages.error(request, 'There is no account with this email. Please register', extra_tags='login')
        return redirect('/login_reg')
    
    password_correct = bcrypt.checkpw(request.POST['password'].encode(), user.password.encode())

    if not password_correct:
        messages.error(request, 'Email/password does not match.', extra_tags='login')
        return redirect('/login_reg')

    else:

        request.session['user_id'] = user.id 

        return redirect('/')


    return redirect('/')


def logout(request):
    request.session.clear()

    return redirect('/')

def add_process(request, methods='POST'):

    if not 'user_id' in request.session:
        messages.error(request, 'You must login first.')
        return redirect('/login_reg')
    
    request.session['errors'] = False

    if len(request.POST['title']) < 1:
        request.session['errors'] = True
        messages.error(request, 'Title is required')
    if len(request.POST['city_name']) < 1:
        request.session['errors'] = True
        messages.error(request, 'City is required')
    if len(request.POST['country_name']) < 1:
        request.session['errors'] = True
        messages.error(request, 'Country is required')
    if len(request.POST['description']) < 5:
        request.session['errors'] = True
        messages.error(request, 'Description must be longer than 5 characters')
    
    if request.session['errors']:
        return redirect('/')

        
    added_user = User.objects.get(id=request.session['user_id'])
    title = request.POST["title"]
    city = request.POST['city_name']
    country = request.POST['country_name']
    description = request.POST['description']

    Itinerary.objects.create(title=title, city=city, country=country, description=description, added_user=added_user)

    return redirect('/my_trips')

def my_trips(request):

    if not 'user_id' in request.session:
        messages.error(request, 'You must login first.', extra_tags='login')
        return redirect('/login_reg')

    user = User.objects.get(id=request.session['user_id'])
    my_trips = Itinerary.objects.filter(added_user=user)

    context = {
        "my_trips": my_trips,
    }
  
    return render (request, 'travel_app/my_trips.html', context)

def edit_trip(request, t_id):

    try:
        trip = Itinerary.objects.get(id=t_id)
    except Itinerary.DoesNotExist:
        messages.error(request, 'This trip does not exist')
        return redirect ('my_trips')

    user = User.objects.get(id=request.session['user_id'])

    context = {
        "trip": trip
    }
    return render (request, 'travel_app/edit_trip.html', context)

def edit_process(request, methods='POST'):

    trip = Itinerary.objects.get(id=request.POST['trip_id'])

    trip.title = request.POST['title']
    trip.city = request.POST['city_name']
    trip.country = request.POST['country_name']
    trip.description = request.POST['description']
    trip.save()

    return redirect('/my_trips')

def view_trip(request, t_id):
    try:
        trip = Itinerary.objects.get(id=t_id)
    except Itinerary.DoesNotExist:
        messages.error(request, 'This trip does not exist')
        return redirect ('my_trips')

    user = User.objects.get(id=request.session['user_id'])

    context = {
        "trip": trip
    }

    print (trip.added_user.first_name)

    return render (request, 'travel_app/view.html', context)

def delete(request, t_id):
    try:
        trip = Itinerary.objects.get(id=t_id)
    except Itinerary.DoesNotExist:
        messages.error(request, 'This trip does not exist')
        return redirect ('my_trips')

    user = User.objects.get(id=request.session['user_id'])

    if trip.added_user == user:
        trip.delete()

    return redirect ('/my_trips')

def saved_itineraries(request):
    if not 'user_id' in request.session:
        messages.error(request, 'You must login first.', extra_tags='login')
        return redirect('/login_reg')

    user = User.objects.get(id=request.session['user_id'])
    saved_trips = Itinerary.objects.filter(saved_user=user)

    context = {
        "trips": saved_trips,
    }
    return render (request, 'travel_app/saved_itineraries.html', context)

def remove (request, t_id):
    user = User.objects.get(id=request.session['user_id'])
    trip = Itinerary.objects.get(id=t_id)
    user.saved_trip.remove(trip)
    user.save()

    return redirect ('/saved_itineraries')

def results(request, city, country):
    
    if 'user_id' in request.session:
        user = User.objects.get(id=request.session['user_id'])
    else: 
        user = None 


    place = Itinerary.objects.filter(city=city)
    excluded_places = place.exclude(added_user=user)
    print (place)
    print (excluded_places)

    for dict in place.values():
        # for key, val in dict.items():
        #     print(key)
        print(dict)
        
 

    context = {
        'place' : place,
        # 'result_for' : place,
        'city' : dict['city'],
        'country' : dict['country']
    }
    return render(request, 'travel_app/results.html', context)

def find_places(request, methods='POST'):
    # if request.is_ajax():
    #     q = request.POST['search']
    #     places = Itinerary.objects.filter(city__icontains=q)
    #     results = []

    #     for pl in places:
    #         place_json = {}
    #         place_json = pl.city + ', ' + pl.country
    #         results.append(place_json)
    #     data =json.dumps(results)
    # else: 
    #     data = 'fail'
    # mimetype = 'application/json'
    # return HttpResponse(data, mimetype)
   
    places= Itinerary.objects.filter(city__icontains=request.POST['search']).values('city', 'country').distinct() or Itinerary.objects.filter(country__icontains=request.POST['search']).values('city', 'country').distinct()
    print(places)
    return render (request, 'travel_app/insert.html', {'places': places})

def save_process(request, t_id):

    if not 'user_id' in request.session:
        messages.error(request, 'You must login first.', extra_tags='login')
        return redirect('/login_reg')
        
    logged_user = User.objects.get(id=request.session['user_id'])

    trip = Itinerary.objects.get(id=t_id)
    trip.saved_user.add(logged_user)
    trip.save()

    context = {
        'logged_user' : logged_user,
    }

    return redirect ('/saved_itineraries')
