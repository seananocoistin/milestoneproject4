from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import HttpResponse

from .models import Listing, Category
from .forms import ListingForm

# Create your views here.

def all_listings(request):
    """ A view to show all listings, including sorting and search queries """

    listings = Listing.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        print(request.GET)
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                listings = listings.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            listings = listings.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            print("is it still working here?")
            listings = listings.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if 'b2c' in request.GET:
                # what to do if b2c is checked
                print('b2c is checked')
            if 'b2b' in request.GET:
                # what to do if b2b is checked
                print('b2b is checked')
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('listings'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            listings = listings.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'listings': listings,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'listings/listings.html', context)


def listing_detail(request, listing_id):
    """ A view to show individual listing details """

    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing,
    }

    return render(request, 'listings/listing_detail.html', context)

@login_required
def sign_up(request):
    """ A page to welcome people to the directory and where they can sign up and create a listing """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only directory owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save()
            messages.success(request, 'Successfully sign up and added listing!')
            return redirect(reverse('listing_detail', args=[listing.id]))
        else:
            messages.error(request, 'Failed to sign up and add a listing. Please ensure the form is valid.')
    else:
        form = ListingForm()
        
    template = 'listings/sign_up.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def add_listing(request):
    """ Add a listing to the directory """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only directory owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save()
            messages.success(request, 'Successfully added listing!')
            return redirect(reverse('listing_detail', args=[listing.id]))
        else:
            messages.error(request, 'Failed to add listing. Please ensure the form is valid.')
    else:
        form = ListingForm()
        
    template = 'listings/add_listing.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_listing(request, listing_id):
    """ Edit a listing in the directory """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only directory owners can do that.')
        return redirect(reverse('home'))

    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated the listing!')
            return redirect(reverse('listing_detail', args=[listing.id]))
        else:
            messages.error(request, 'Failed to update the listing. Please ensure the form is valid.')
    else:
        form = ListingForm(instance=listing)
        messages.info(request, f'You are editing {listing.name}')

    template = 'listings/edit_listing.html'
    context = {
        'form': form,
        'listing': listing,
    }

    return render(request, template, context)


@login_required
def delete_listing(request, listing_id):
    """ Delete a listing from the directory """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only directory owners can do that.')
        return redirect(reverse('home'))

    listing = get_object_or_404(Listing, pk=listing_id)
    listing.delete()
    messages.success(request, 'The listing was deleted!')
    return redirect(reverse('listings'))