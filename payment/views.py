from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='users:login')
def payment(request):
    """
    Render the payment page for users.

    This function is responsible for displaying the `payment.html` page, which 
    allows users to review and proceed with payment options.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the `payment.html` template.
    """
    return render(request, 'payment/payment.html')

def payment_details(request):
    """
    Handle the submission of payment details provided by the user.

    This function processes payment information submitted via a POST request. 
    It retrieves the following details from the request:
        - `payment_method`: The selected payment method (e.g., credit card, PayPal).
        - `account_number`: The account or card number provided by the user.
        - `password`: The password or secure authentication token for the payment.

    If the request method is POST:
        - Logs the payment details to the console (placeholder for actual payment logic).
        - Returns a JSON response indicating the success of the operation.

    If the request method is not POST:
        - Renders the `popup.html` page, which serves as the payment form.

    Args:
        request (HttpRequest): The HTTP request object containing user-submitted 
        payment details if the method is POST.

    Returns:
        JsonResponse: A JSON object with the following keys if the request method is POST:
            - `status`: "success", indicating the operation was successful.
            - `message`: A message confirming the payment details were submitted.
        HttpResponse: Renders the `popup.html` template if the request method is not POST.
    """
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        account_number = request.POST.get('account_number')
        password = request.POST.get('password')

        # Placeholder for payment processing logic
        print(f"Payment method: {payment_method}")
        print(f"Account Number: {account_number}")
        print(f"Password: {password}")

        if payment_method and account_number and password:
            # Return a success message as a JSON response
            return JsonResponse({
                'status': 'success',
                'message': 'Payment details submitted successfully.'
            })
        else:
            # Return error response for missing or invalid details
            return JsonResponse({
                'status': 'error',
                'errors': 'Invalid or missing payment details.',
            }, status=400)

    # Render the payment form if the request is not POST
    return render(request, 'popup/popup.html')
