from django.shortcuts import render, redirect, get_object_or_404
from .models import Place # this is importing the database from models
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

# Create your views here.

@login_required
def place_list (request): # same as what is in urls.py

    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST) # creating a form from data in the request 
        place = form.save(commit=False) # creating a model object from form
        place.user = request.user
        if form.is_valid(): # validation against DB constraints
            place. save() # saves place in db
            return redirect ('place_list') # reloads home page

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name') # this will sort by name
    new_place_form = NewPlaceForm() # used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})
# this above will render and taket the wishlist, take the places, form and make it one webpage


# this is creating the funtion for the views website
@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })

@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
       # place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect('place_list') # redirect to places visited
    #return redirect('places_visited') #redirect to wishlist places

@login_required
def about(request):
    author = 'Logan'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})
# potentially block this request out if things aren't working


@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    if place.user != request.user:
        return HttpResponseForbidden()
    # Deos this place belong to the current user
    # is this a GET reequest (show + form) or a POST reequest (update Place object)
    # if POST request, validate from data and upadte
    # if GET request, show Place info and form

    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)  
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)  # temporary 

        return redirect('place_details', place_pk=place_pk)
    
    else: 
        # if GET request, show Place info and optional form
        # If place is visisted, show form, if place is not visited, no form
        if place.visited:
            review_form = TripReviewForm(instancee=place)
            render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_from': review_form })
        else:
            render(request, 'travel_wishlist/place_detail.html', {'place': place})

@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()
