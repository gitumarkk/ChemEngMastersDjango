# Python
import json

# Django
from django.core.urlresolvers import reverse
from django.test import TestCase


class TestViews(TestCase):
    def test_get_api_endpoint(self):
        url = reverse("bioleach_reactor")
        response = self.client.get(url, follow=True)

        response_json = json.loads(response.content)

    def test_get_copper_reaction_rates(self):
        url = reverse("copper_reaction_rates")

        response = self.client.get(url, follow=True)
        response_json = json.loads(response.content)
        print response_json
