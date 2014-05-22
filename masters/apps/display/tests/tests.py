# Python
import json

# Django
from django.core.urlresolvers import reverse
from django.test import TestCase


class TestViews(TestCase):
    def test_get_single_reactor_with_chemical(self):
        url = reverse("single_reactor", kwargs={"reactor_type": "chemical"})
        response = self.client.get(url, follow=True)

        response_json = json.loads(response.content)

        item_0 = response_json[0]

        self.assertIn('step', item_0)
        self.assertIn('flow_out', item_0)

        self.assertIn('flowrate', item_0["flow_out"])
        self.assertEqual(item_0["flow_out"]["flowrate"], 1)

        self.assertIn('cstr_data', item_0)
        self.assertIn('total_rate_ferric', item_0['cstr_data'])
        self.assertIn('total_rate_ferrous', item_0['cstr_data'])

        self.assertEqual(item_0['cstr_data']['total_rate_ferrous'], -item_0['cstr_data']['total_rate_ferric'])

        self.assertIn('component', item_0['cstr_data'])
        self.assertEqual(item_0['cstr_data']["component"]["name"], "Cu")
        self.assertEqual(item_0['cstr_data']["component"]["rate_ferrous"], -item_0['cstr_data']["component"]["rate_ferric"])

    def test_get_copper_reaction_rates(self):
        url = reverse("reaction_rates", kwargs={"rate_type": "chemical"})
        response = self.client.get(url, follow=True)
        response_json = json.loads(response.content)

        item_0 = response_json[0]
        self.assertIn("ferric", item_0)
        self.assertIn("rate_ferric", item_0)
        self.assertIn("copper", item_0)

    def test_get_bioxidation_reaction_rates(self):
        url = reverse("reaction_rates", kwargs={"rate_type": "bioxidation"})

        response = self.client.get(url, follow=True)
        response_json = json.loads(response.content)
        item_0 = response_json[0]
        self.assertIn("ferric_ferrous", item_0)
        self.assertIn("rate_ferrous", item_0)
