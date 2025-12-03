from django.test import TestCase
from django.urls import reverse
from .models import Product

class ProductSearchViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(
            name="Red Sneakers",
            brand="BrandA",
            product_type="GradeA",
            size="10",
            color="Red",
            year_of_manufacture=2022,
            price=100.00,
            rating=4.5,
        )
        Product.objects.create(
            name="Blue Sneakers",
            brand="BrandB",
            product_type="GradeB",
            size="9",
            color="Blue",
            year_of_manufacture=2023,
            price=120.00,
            rating=4.7,
        )
        Product.objects.create(
            name="Green Sneakers",
            brand="BrandC",
            product_type="GradeB",
            size="11",
            color="Green",
            year_of_manufacture=2021,
            price=80.00,
            rating=4.2,
        )

    def test_search_by_name(self):
        response = self.client.get(reverse('products:search'), {'q': 'Red Sneakers'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Red Sneakers")
        self.assertNotContains(response, "Blue Sneakers")
        self.assertNotContains(response, "Green Sneakers")

    def test_search_by_brand(self):
        response = self.client.get(reverse('products:search'), {'q': 'BrandB'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blue Sneakers")
        self.assertNotContains(response, "Red Sneakers")
        self.assertNotContains(response, "Green Sneakers")

    def test_search_by_product_type(self):
        response = self.client.get(reverse('products:search'), {'q': 'GradeA'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Red Sneakers")
        self.assertNotContains(response, "Blue Sneakers")
        self.assertNotContains(response, "Green Sneakers")

    def test_sort_by_price_asc(self):
        response = self.client.get(reverse('products:search'), {'q': 'Sneakers', 'sort_by': 'price', 'sort_order': 'asc'})
        results = list(response.context['results'])
        self.assertEqual(results[0].price, 80.00)
        self.assertEqual(results[1].price, 100.00)
        self.assertEqual(results[2].price, 120.00)

    def test_sort_by_rating_desc(self):
        response = self.client.get(reverse('products:search'), {'q': 'Sneakers', 'sort_by': 'rating', 'sort_order': 'desc'})
        results = list(response.context['results'])
        self.assertEqual(results[0].rating, 4.7)
        self.assertEqual(results[1].rating, 4.5)
        self.assertEqual(results[2].rating, 4.2)

    def test_sort_by_name_asc(self):
        response = self.client.get(reverse('products:search'), {'q': 'Sneakers', 'sort_by': 'name', 'sort_order': 'asc'})
        
        results = list(response.context['results'])

        self.assertEqual(len(results), 3, "Expected 3 results for query 'Sneakers'.")
        self.assertEqual(results[0].name, "Blue Sneakers")
        self.assertEqual(results[1].name, "Green Sneakers")
        self.assertEqual(results[2].name, "Red Sneakers")


    def test_empty_query(self):
        response = self.client.get(reverse('products:search'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a search query.")

    def test_no_results(self):
        response = self.client.get(reverse('products:search'), {'q': 'Yellow Sneakers'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No products found. Please refine your search.")


from django.test import TestCase
from django.urls import reverse
from .models import Product

from django.test import TestCase
from django.urls import reverse
from .models import Product


class ProductListViewTest(TestCase):
    

    @classmethod
    def setUpTestData(cls):
        
        Product.objects.create(
            name="Red Sneakers",
            brand="BrandA",
            product_type="GradeA",
            size="10",
            color="Red",
            year_of_manufacture=2022,
            price=100.00,
            rating=4.5,
        )
        Product.objects.create(
            name="Blue Sneakers",
            brand="BrandB",
            product_type="GradeB",
            size="9",
            color="Blue",
            year_of_manufacture=2023,
            price=120.00,
            rating=4.7,
        )
        Product.objects.create(
            name="Green Sneakers",
            brand="BrandC",
            product_type="GradeB",
            size="11",
            color="Green",
            year_of_manufacture=2021,
            price=80.00,
            rating=4.2,
        )

    def test_filter_by_name(self):
        
        response = self.client.get(reverse('products:product_list'), {'name': 'Red Sneakers'})
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().name, "Red Sneakers")

    def test_filter_by_brand(self):
        
        response = self.client.get(reverse('products:product_list'), {'brand': 'BrandB'})
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().brand, "BrandB")

    def test_filter_by_price(self):
        
        response = self.client.get(reverse('products:product_list'), {'price': '100.00'})
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().price, 100.00)

    def test_filter_by_year_of_manufacture(self):
        
        response = self.client.get(reverse('products:product_list'), {'year_of_manufacture': '2023'})
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().year_of_manufacture, 2023)

    def test_filter_by_combined_fields(self):
        
        response = self.client.get(reverse('products:product_list'), {
            'brand': 'BrandB',
            'color': 'Blue',
        })
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().name, "Blue Sneakers")

    def test_empty_query(self):
        
        response = self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 3)

    def test_no_results(self):
        
        response = self.client.get(reverse('products:product_list'), {'name': 'Yellow Sneakers'})
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 0)

    def test_invalid_field(self):
        
        response = self.client.get(reverse('products:product_list'), {'invalid_field': 'test'})
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 3)

    def test_filter_by_rating(self):
        
        response = self.client.get(reverse('products:product_list'), {'rating': '4.7'})
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().rating, 4.7)

    def test_case_insensitive_filter(self):
        
        response = self.client.get(reverse('products:product_list'), {'name': 'red sneakers'})
        self.assertEqual(response.status_code, 200)
        products = response.context['products']
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().name, "Red Sneakers")


class ProductAdvancedFilterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Product.objects.create(
            name="Budget Sneakers",
            brand="BrandX",
            product_type="GradeC",
            size="8",
            color="Black",
            year_of_manufacture=2024,
            price=50.00,
            rating=4.0,
        )
        Product.objects.create(
            name="Premium Sneakers",
            brand="BrandX",
            product_type="GradeC",
            size="9",
            color="White",
            year_of_manufacture=2024,
            price=200.00,
            rating=4.9,
        )
        Product.objects.create(
            name="Midrange Sneakers",
            brand="BrandY",
            product_type="GradeB",
            size="10",
            color="Blue",
            year_of_manufacture=2023,
            price=120.00,
            rating=4.5,
        )

    def test_filter_by_brand_and_price_range(self):
        """Check that filtering by brand and price range works"""
        response = self.client.get(reverse('products:product_list'), {
            'brand': 'BrandX',
            'min_price': '40',
            'max_price': '100',
        })
        products = response.context['products']
        self.assertEqual(products.count(), 1)
        self.assertEqual(products.first().name, "Budget Sneakers")