from django.test import TestCase
from catalog.models import Author

# Create your tests here.

class AuthoModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Mister', last_name='Djaxy')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual('last name', field_label)
    
    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = Author._meta.get_field('date_of_death').verbose_name
        self.assertEqual('died', field_label)

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(100, max_length)
    
    def test_absolute_url(self):
        author = Author.objects.get(id='1')
        self.assertEqual('/catalog/authors/1', author.get_absolute_url())

# sample tests below

# class MyTestClass(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         print("setUpTestData: Run once to set up non-modified data for all class methods.")
#         pass

#     def setUp(self):
#         print('setUp: Run once for every test method to setup clean data.')
#         pass

#     def test_false_is_false(self):
#         print('Method: test_false_is_false.')
#         self.assertFalse(False)

#     def test_false_is_true(self):
#         print('Method: test_false_is_true.')
#         self.assertTrue(False)

#     def test_one_plus_one_equals_two(self):
#         print('Method: test_one_plus_one_equals_two.')
#         self.assertEqual(1+1, 2)

