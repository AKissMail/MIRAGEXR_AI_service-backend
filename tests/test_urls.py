from django.test import SimpleTestCase
from django.urls import reverse, resolve
from authentication.views import authentication
from options.views import get_options
from listen.views import listen
from speak.views import speak
from document.views import document, configuration, updateOptions


class TestUrls(SimpleTestCase):
    """
    This class provides unit tests for the URLs in the application. It inherits from SimpleTestCase,
    making it compatible with Django's test framework. Each test method in this class verifies that
    the respective URL resolves to the correct view function.

    Note: This class does not need to be instantiated to run the test methods.
    """
    def test_authentication_url(self):
        url = reverse("authentication")
        resolved_func = resolve(url).func
        self.assertEqual(resolved_func, authentication)

    def test_options_url(self):
        url = reverse("options")
        self.assertEqual(resolve(url).func, get_options)

    def test_listen_url(self):
        url = reverse("listen")
        self.assertEqual(resolve(url).func, listen)

    def test_speak_url(self):
        url = reverse("speak")
        self.assertEqual(resolve(url).func, speak)

    def test_documents_url(self):
        url = reverse("document")
        self.assertEqual(resolve(url).func, document)

    def test_configuration_url(self):
        url = reverse("configuration")
        self.assertEqual(resolve(url).func, configuration)

    def test_update_options_url(self):
        url = reverse("update_options")
        self.assertEqual(resolve(url).func, updateOptions)
