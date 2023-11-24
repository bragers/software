from django.test import TestCase
from django.utils import timezone
from .models import Location, Language, Article
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import ArticleListView, process_payment, login_user
from .forms import ArticleFilterForm


class ArticleModelTest(TestCase):
    def setUp(self):
        # Create dummy Location and Language for testing
        self.location = Location.objects.create(name='Test Location')
        self.language = Language.objects.create(name='Test Language')

        # Create dummy Article for testing
        self.article = Article.objects.create(
            title='Test Article',
            pub_date=timezone.now(),
            for_kids=True,
            high_activity=False,
            location=self.location,
            language=self.language,
            free=True
        )

    def test_article_creation(self):
        # Test if the article was created successfully
        self.assertEqual(self.article.title, 'Test Article')
        self.assertEqual(self.article.for_kids, True)
        self.assertEqual(self.article.high_activity, False)
        self.assertEqual(self.article.location, self.location)
        self.assertEqual(self.article.language, self.language)
        self.assertEqual(self.article.free, True)

    def test_article_filter_by_location(self):
        # Test filtering articles by location
        articles_in_location = Article.objects.filter(location=self.location)
        self.assertIn(self.article, articles_in_location)

    def test_article_filter_by_language(self):
        # Test filtering articles by language
        articles_in_language = Article.objects.filter(language=self.language)
        self.assertIn(self.article, articles_in_language)

    def test_article_filter_by_for_kids(self):
        # Test filtering articles by for_kids field
        articles_for_kids = Article.objects.filter(for_kids=True)
        self.assertIn(self.article, articles_for_kids)

    def test_article_filter_by_high_activity(self):
        # Test filtering articles by high_activity field
        articles_high_activity = Article.objects.filter(high_activity=False)
        self.assertIn(self.article, articles_high_activity)

    def test_article_filter_by_free(self):
        # Test filtering articles by free field
        articles_free = Article.objects.filter(free=True)
        self.assertIn(self.article, articles_free)


class ArticleListViewTest(TestCase):
    def setUp(self):
        # Create sample Location and Language instances for testing
        self.location = Location.objects.create(name='Test Location')
        self.language = Language.objects.create(name='Test Language')

        # Create sample Article instances for testing
        for _ in range(15):
            Article.objects.create(
                title=f'Test Article {_}',
                pub_date=timezone.now(),
                for_kids=True,
                high_activity=False,
                location=self.location,
                language=self.language,
                free=True
            )

    def test_article_list_view(self):
        response = self.client.get(reverse('polls:article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/article_list.html')

    def test_filtered_article_list_view(self):
        data = {'location': self.location.id, 'language': self.language.id, 'for_kids': True}
        response = self.client.get(reverse('polls:article_list'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/article_list.html')


class LoginUserViewTest(TestCase):
    def test_successful_login(self):
        response = self.client.get(reverse('polls:login_user'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(response.json()['message'], 'Login successful')

    def test_login_error(self):
        # Simulate an error during login
        with self.settings(DEBUG=True):  # Ensure exceptions are not silenced in DEBUG mode
            # Simulate an error during login
            with self.assertRaises(Exception):
                response = self.client.get(reverse('polls:login_user'))
                self.assertEqual(response.status_code, 500)


class ProcessPaymentViewTest(TestCase):
    def test_successful_payment(self):
        response = self.client.get(reverse('polls:process_payment'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(response.json()['message'], 'Payment processed successfully')

    def test_payment_error(self):
        # Simulate an error during payment processing
        with self.settings(DEBUG=True):  # Ensure exceptions are not silenced in DEBUG mode
            # Simulate an error during payment processing
            with self.assertRaises(Exception):
                response = self.client.get(reverse('polls:process_payment'))
                self.assertEqual(response.status_code, 500)


class TestUrls(SimpleTestCase):
    def test_article_list_url_resolves(self):
        url = reverse('polls:article_list')
        self.assertEquals(resolve(url).func.view_class, ArticleListView)

    def test_article_list_for_kids_url_resolves(self):
        url = reverse('polls:article_list_for_kids')
        self.assertEquals(resolve(url).func.view_class, ArticleListView)
        self.assertTrue('for_kids' in resolve(url).kwargs)

    def test_article_list_high_activity_url_resolves(self):
        url = reverse('polls:article_list_high_activity')
        self.assertEquals(resolve(url).func.view_class, ArticleListView)
        self.assertTrue('high_activity' in resolve(url).kwargs)

    def test_root_url_resolves(self):
        url = reverse('polls:article_list')
        self.assertEquals(resolve(url).func.view_class, ArticleListView)

    def test_process_payment_url_resolves(self):
        url = reverse('polls:process_payment')
        self.assertEquals(resolve(url).func, process_payment)

    def test_login_user_url_resolves(self):
        url = reverse('polls:login_user')
        self.assertEquals(resolve(url).func, login_user)


class ArticleFilterFormTest(TestCase):
    def setUp(self):
        # Create sample Location and Language instances for testing
        self.location = Location.objects.create(name='Test Location')
        self.language = Language.objects.create(name='Test Language')

    def test_article_filter_form_valid_data(self):
        data = {
            'location': self.location.id,
            'language': self.language.id,
            'for_kids': True,
            'high_activity': False,
            'free': True,
        }
        form = ArticleFilterForm(data)
        self.assertTrue(form.is_valid())

    def test_article_filter_form_empty_data(self):
        form = ArticleFilterForm({})
        self.assertTrue(form.is_valid())

    def test_article_filter_form_invalid_data(self):
        # Invalid data, for example, location with an invalid ID
        data = {
            'location': 999,  # Non-existent ID
            'language': self.language.id,
            'for_kids': True,
            'high_activity': False,
            'free': True,
        }
        form = ArticleFilterForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('location', form.errors)

    # Add more specific tests as needed based on your form logic

    def test_article_filter_form_labels(self):
        form = ArticleFilterForm()
        self.assertEqual(form.fields['location'].label_from_instance(self.location), 'Test Location')
        self.assertEqual(form.fields['language'].label_from_instance(self.language), 'Test Language')
