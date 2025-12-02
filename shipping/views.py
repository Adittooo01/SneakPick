from decimal import Decimal
from django.shortcuts import render
from .models import ShippingMethod
from payment.models import Payment
from django.contrib.auth.decorators import login_required


@login_required
def shipping_Methods(request):
    """
    Display active shipping methods and calculate the total payment 
    including the default shipping charge for the authenticated user.

    This view retrieves all active shipping methods from the database, 
    calculates the total payment for the authenticated user's last 
    completed payment, and adds the default shipping charge (charge of 
    the first active shipping method) to the total payment. If no 
    payment exists for the user, only the shipping charge is used.

    Args:
        request (HttpRequest): The HTTP request object, including user 
        and session data.

    Returns:
        HttpResponse: The rendered HTML response displaying the 
        shipping methods, total payment, and total with shipping charge.
    
    Context:
        - `methods` (QuerySet): Active shipping methods.
        - `total_payment` (Decimal): The total payment amount from the 
          user's latest completed payment or 0.00 if no payment exists.
        - `total_with_shipping` (Decimal): The total payment amount 
          including the default shipping charge.
    """
    methods = ShippingMethod.objects.filter(is_active=True)  # Fetch only active shipping methods
    total_payment = None
    default_shipping_charge = Decimal('0.00')  # Ensure it's Decimal

    if request.user.is_authenticated:
        # Fetch the user's latest payment related to an order
        payment = Payment.objects.filter(user=request.user, status='Completed').last()
        if payment:
            total_payment = Decimal(payment.amount)  # Convert to Decimal

    if methods.exists():
        default_shipping_charge = Decimal(methods[0].charge)  # Convert to Decimal

    # Safely add total payment and default shipping charge, both are now Decimal
    total_with_shipping = total_payment + default_shipping_charge if total_payment else default_shipping_charge

    context = {
            'methods': methods,
            'total_payment': total_payment or Decimal('0.00'),
            'total_with_shipping': total_with_shipping,
        }
    
    return render(request, 'shipping/shipping_methods.html', context)
