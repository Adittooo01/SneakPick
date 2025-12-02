from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product
from users.models import Reviews


def searchResult(request):
    """Handles search queries and returns matching results.
    Can handle hits on multiple fields and keywords such as
    "name", "brand" and "product_type"

    Can also do sorting on the queryset. Sort by alphabetical
    order, price and rating.
    
        args: HTTP GET request

        returns queryset that satisfies the request query.
    """
    query = request.GET.get('q', '').strip()
    sort_by = request.GET.get('sort_by', 'name')  #default sort 'name'
    sort_order = request.GET.get('sort_order', 'asc') #default sort ascending

    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(brand__icontains=query) |
            Q(product_type__icontains=query)
        )
    else:
        results = Product.objects.none()

    if sort_by == 'name':
        if sort_order == 'asc':
            results = results.order_by('name')
        else:
            results = results.order_by('-name')
    elif sort_by == 'price':
        if sort_order == 'asc':
            results = results.order_by('price')
        else:
            results = results.order_by('-price')
    elif sort_by == 'rating':
        if sort_order == 'asc':
            results = results.order_by('rating')
        else:
            results = results.order_by('-rating')

    context = {
        'query': query,
        'results': results,
        'sort_by': sort_by,
        'sort_order': sort_order,
    }
    return render(request, 'products/search_results.html', context)


def product_list(request):
    """
    Display a list of products, filtered based on query parameters.

    The user can specify filters via GET parameters for fields such as 
    name, price, brand, year of manufacture, and rating.

    Parameters
    ----------
    request : HttpRequest
        The HTTP request object containing metadata about the request,
        including GET parameters.

    Returns
    -------
    HttpResponse
        A rendered HTML page displaying the list of filtered products.

    Notes
    -----
    - If no filters are provided, all products are displayed.
    - The user can filter by any valid field. Multiple filters can be applied at once.

    Valid Filter Fields
    -------------------
    - `name`
    - `brand`
    - `product_type`
    - `size`
    - `color`
    - `year_of_manufacture`
    - `price`
    - `rating`
    - `image`
    """
    filters = {
        'name': request.GET.get('name'),
        'brand': request.GET.get('brand'),
        'product_type': request.GET.get('product_type'),
        'size': request.GET.get('size'),
        'color': request.GET.get('color'),
        'year_of_manufacture': request.GET.get('year_of_manufacture'),
        'price': request.GET.get('price'),
        'rating': request.GET.get('rating'),
        'image': request.GET.get('image'),
    }

    products = Product.objects.all()

    for field, value in filters.items():
        if value:
            if field in ['price', 'year_of_manufacture', 'rating']:
                try:
                    products = products.filter(**{f'{field}__exact': float(value)})
                except ValueError:
                    continue
            else:
                products = products.filter(**{f'{field}__icontains': value})

    context = {'products': products}
    return render(request, 'products/product_list.html', context)


@login_required(login_url= 'users:login')
def rate_product(request, product_id):

    """
View function to handle product rating submission.

    This view allows users to submit a rating for a specific product. It retrieves the product 
    by its `product_id` and processes the rating value submitted via a POST request. The rating 
    value is validated and applied to the product using the `set_rating` method. If the rating 
    submission is successful, the user is redirected to the product detail page. In case of an error, 
    the user is shown a form with an error message.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        product_id (int): The ID of the product for which the rating is being submitted.
    
    Returns:
        HttpResponse: A redirect to the product detail page if the rating is successfully submitted.
        If there is an error in the submission, the function renders the rating page again with an error message.
    
    Raises:
        Http404: If no product with the given `product_id` exists, a 404 error will be raised.
    
    """
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        try:
            # Get the rating value from the form data
            rating_value = float(request.POST.get('rating'))
            product.set_rating(request.user, rating_value)  # Call the set_rating method
            return redirect('product_detail', product_id=product.id)  # Redirect to product detail page
        except ValidationError as e:
            return render(request, 'products/rate_product.html', {'product': product, 'error': str(e)})
    
    return render(request, 'products/rate_product.html', {'product': product})


def product_detail(request, product_id):
    
    """
View function to display the details of a single product along with its reviews.
    
    This view retrieves a product by its `product_id` from the database and displays its details 
    on a product detail page. It also fetches all reviews associated with the product and passes them 
    to the template for rendering.
    
    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        product_id (int): The ID of the product to retrieve from the database.
    
    Returns:
        HttpResponse: The rendered product detail page with product information and reviews.
    
    Raises:
        Http404: If no product with the given `product_id` exists, a 404 error will be raised.
    
    """
    product = get_object_or_404(Product, id=product_id)
    reviews = Reviews.objects.filter(product=product)  # Get all reviews for this product
    return render(request, 'products/product_detail.html', {'product': product, 'reviews': reviews})