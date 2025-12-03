from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from promotions.models import DiscountCode
from datetime import timedelta


class DiscountCodeModelTest(TestCase):
    """
    Tests for the DiscountCode model.
    """

    def setUp(self):
        self.code = DiscountCode.objects.create(
            code="SAVE10",
            description="10% off on all items",
            discount_percentage=10.00,
            valid_from=timezone.now() - timedelta(days=1),
            valid_to=timezone.now() + timedelta(days=1),
            is_active=True,
        )

    def test_discount_code_creation(self):
        """Ensure the discount code was created correctly."""
        self.assertEqual(self.code.code, "SAVE10")
        self.assertEqual(self.code.discount_percentage, 10.00)
        self.assertTrue(self.code.is_active)

    def test_string_representation(self):
        """The __str__ method should return the code."""
        self.assertEqual(str(self.code), "SAVE10")

    def test_discount_code_validity_period(self):
        """Check if discount code is valid within the date range."""
        now = timezone.now()
        self.assertTrue(self.code.valid_from <= now <= self.code.valid_to)

    def test_inactive_discount_code(self):
        """Ensure inactive codes are correctly recognized."""
        self.code.is_active = False
        self.code.save()
        self.assertFalse(self.code.is_active)


class ApplyDiscountViewTest(TestCase):
    """
    Tests for the apply_discount view.
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse("promotions:apply_discount")

        # Create discount codes
        self.active_code = DiscountCode.objects.create(
            code="ACTIVE20",
            description="20% active discount",
            discount_percentage=20.00,
            valid_from=timezone.now() - timedelta(days=1),
            valid_to=timezone.now() + timedelta(days=1),
            is_active=True,
        )
        self.inactive_code = DiscountCode.objects.create(
            code="OFFLINE5",
            description="Inactive code",
            discount_percentage=5.00,
            valid_from=timezone.now() - timedelta(days=5),
            valid_to=timezone.now() - timedelta(days=1),
            is_active=False,
        )

    def test_view_status_code(self):
        """The view should return HTTP 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """The view should use promotions/apply_discount.html."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "promotions/apply_discount.html")

    def test_view_returns_all_discount_codes(self):
        """The view should return all discount codes in context."""
        response = self.client.get(self.url)
        discount_codes = response.context["discount_codes"]

        self.assertEqual(discount_codes.count(), 2)
        self.assertIn(self.active_code, discount_codes)
        self.assertIn(self.inactive_code, discount_codes)

    def test_discount_code_data_in_template(self):
        """Check that the template receives correct code info."""
        response = self.client.get(self.url)
        discount_codes = response.context["discount_codes"]

        active = discount_codes.get(code="ACTIVE20")
        self.assertEqual(active.discount_percentage, 20.00)
