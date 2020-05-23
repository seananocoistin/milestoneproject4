from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from listings.models import Listing

# Create your views here.

def view_cart(request):
    """ A view that renders the cart contents page """

    return render(request, 'cart/cart.html')

def add_to_cart(request, item_id):
    """ Add a quantity of the specified listing to the shopping cart """

    listing = get_object_or_404(Listing, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'listing_size' in request.POST:
        size = request.POST['listing_size']
    cart = request.session.get('cart', {})

    if size:
        if item_id in list(cart.keys()):
            if size in cart[item_id]['items_by_size'].keys():
                cart[item_id]['items_by_size'][size] += quantity
                messages.success(request, f'Updated size {size.upper()} {listing.name} quantity to {cart[item_id]["items_by_size"][size]}')
            else:
                cart[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added size {size.upper()} {listing.name} to your cart')
        else:
            cart[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()} {listing.name} to your cart')
    else:
        if item_id in list(cart.keys()):
            cart[item_id] += quantity
            messages.success(request, f'Updated {listing.name} quantity to {cart[item_id]}')
        else:
            cart[item_id] = quantity
            messages.success(request, f'Added {listing.name} to your cart')

    request.session['cart'] = cart
    return redirect(redirect_url)
    

def adjust_cart(request, item_id):
    """Adjust the quantity of the specified listing to the specified amount"""

    listing = get_object_or_404(Listing, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'listing_size' in request.POST:
        size = request.POST['listing_size']
    cart = request.session.get('cart', {})

    if size:
        if quantity > 0:
            cart[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {listing.name} quantity to {cart[item_id]["items_by_size"][size]}')
        else:
            del cart[item_id]['items_by_size'][size]
            if not cart[item_id]['items_by_size']:
                cart.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {listing.name} from your cart')
    else:
        if quantity > 0:
            cart[item_id] = quantity
            messages.success(request, f'Updated {listing.name} quantity to {cart[item_id]}')
        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {listing.name} from your cart')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))


def remove_from_cart(request, item_id):
    """Remove the item from the shopping cart"""

    try:
        listing = get_object_or_404(Listing, pk=item_id)
        size = None
        if 'listing_size' in request.POST:
            size = request.POST['listing_size']
        cart = request.session.get('cart', {})

        if size:
            del cart[item_id]['items_by_size'][size]
            if not cart[item_id]['items_by_size']:
                cart.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {listing.name} from your cart')
        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {listing.name} from your cart')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)