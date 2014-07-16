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
        # self.assertEqual(item_0["flow_out"]["flowrate"], 1)

        self.assertIn('cstr_data', item_0)
        self.assertIn('total_rate_ferric', item_0['cstr_data'])
        self.assertIn('total_rate_ferrous', item_0['cstr_data'])

        self.assertEqual(item_0['cstr_data']['total_rate_ferrous'], -item_0['cstr_data']['total_rate_ferric'])

        self.assertIn('components', item_0['cstr_data'])

        self.assertIn("Cu", item_0['cstr_data']["components"])
        self.assertEqual(item_0['cstr_data']["components"]["Cu"]["rate_ferrous"],
                         -item_0['cstr_data']["components"]["Cu"]["rate_ferric"])

        # print response_json[len(response_json)-3:]

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

    def test_system_with_tanks_in_series_copper_data(self):
        url = reverse("system_run", kwargs={"system_type": "tanks_in_series"})

        response = self.client.get("%s?Cu=2" % url, follow=True)

        response_json = json.loads(response.content)
        biox_0 = response_json["bioxidation"][0]
        chem_0 = response_json["chemical"][0]

        # item_0 = response_json[0]

        self.assertIn("chemical", response_json)
        self.assertIn("bioxidation", response_json)
        self.assertIn("summary", response_json)

        self.assertIn("step", biox_0)
        self.assertIn("step", chem_0)

        self.assertIn("total_rate_ferric", biox_0["cstr_data"])

    def test_system_with_tanks_in_series_no_data(self):
        url = reverse("system_run", kwargs={"system_type": "tanks_in_series"})

        response = self.client.get(url, follow=True)

        response_json = json.loads(response.content)
        self.assertEqual(response_json["success"], False)


    def test_system_with_tanks_in_series_multiple_data(self):
        url = reverse("system_run", kwargs={"system_type": "tanks_in_series"})

        response = self.client.get("%s?Cu=2&Sn=0.5&Zn=0.5" % url, follow=True)

        response_json = json.loads(response.content)
        biox_0 = response_json["bioxidation"][0]
        chem_0 = response_json["chemical"][0]

        # item_0 = response_json[0]

        self.assertIn("chemical", response_json)
        self.assertIn("bioxidation", response_json)
        self.assertIn("summary", response_json)

        self.assertIn("step", biox_0)
        self.assertIn("step", chem_0)

        self.assertIn("total_rate_ferric", biox_0["cstr_data"])

    def test_export_as_csv(self):
        url = reverse("export_data", kwargs={"system_type": "tanks_in_series"})

        response = self.client.get("%s?Cu=2&Sn=0.5&Zn=0.5" % url, follow=True)
