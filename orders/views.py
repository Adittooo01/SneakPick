from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order


@login_required
def order_history(request):
    """
    Display a user's order history.

    Retrieves and displays a list of all orders associated with the currently
    logged-in user, sorted by the oldest order first.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object containing metadata about the request.

    Returns
    -------
    HttpResponse
        A rendered HTML page displaying the user's order history.

    Notes
    -----
    - The user must be authenticated to access this view.
    - Orders are displayed in ascending order of `order_date` (oldest first).

    Context Variables
    -----------------
    - `orders` : QuerySet
        A QuerySet of `Order` objects belonging to the logged-in user,
        ordered by `order_date` (ascending).
    """
    # Order by `order_date` in ascending order (oldest first)
    orders = Order.objects.filter(user=request.user).order_by('order_date')
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """
    Display the details of a specific order.

    Retrieves and displays information about a specific order associated with
    the currently logged-in user. Ensures that only the user who placed the order
    can view its details.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object containing metadata about the request.
    order_id : int
        The ID of the order to retrieve details for.

    Returns
    -------
    HttpResponse
        A rendered HTML page displaying the details of the specified order.

    Notes
    -----
    - The user must be authenticated to access this view.
    - If the specified `order_id` does not belong to the logged-in user or
      does not exist, a 404 error is raised.

    Context Variables
    -----------------
    - `order` : Order
        The `Order` object corresponding to the provided `order_id`.

    Exceptions
    ----------
    Http404
        Raised if the order does not exist or does not belong to the
        logged-in user.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {'order': order}
    return render(request, 'orders/order_detail.html', context)
