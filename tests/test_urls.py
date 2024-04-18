from django.test import SimpleTestCase
from django.urls import reverse, resolve
from authentication.views import authentication
from options.views import get_options
from listen.views import listen
from speak.views import speak
from dokument.views import dokument


class TestUrls(SimpleTestCase):
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

    def test_dokuments_url(self):
        url = reverse("dokument")
        self.assertEqual(resolve(url).func, dokument)
