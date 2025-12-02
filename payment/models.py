from django.db import models
from django.conf import settings  # Reference for the user model
from orders.models import Order  # Import the Order model


class Payment(models.Model):
    """
    Represents a payment made by a user for an order.

    Attributes:
        user (ForeignKey): The user who made the payment.
        order (OneToOneField): The order associated with the payment.
        payment_date (DateTimeField): The date and time when the payment was made.
        amount (DecimalField): The amount paid.
        method (CharField): The payment method chosen by the user.
        status (CharField): The status of the payment (e.g., Completed, Pending).
        transaction_id (CharField): A unique identifier for the payment transaction.
    """
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('PayPal', 'PayPal'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cash on Delivery', 'Cash on Delivery'),
        ('bKash', 'bKash'),
        ('Rocket', 'Rocket'),
        ('Apple Pay', 'Apple Pay'),
        ('Google Pay', 'Google Pay'),
        ('Master Card', 'Master Card'),
        ('Nagad', 'Nagad'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        default='Credit Card'
    )
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending'
    )
    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True
    )

    def __str__(self):
        """
        Return a string representation of the payment.

        Includes the payment ID, associated order ID, and payment status.
        """
        return f"Payment {self.id} for Order {self.order.id} - Status: {self.status}"
