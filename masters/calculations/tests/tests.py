# Django
from django.test import TestCase

# Project
from masters.calculations import system
from masters.calculations import constants
from masters.calculations import reactors
from masters.calculations import reactions

class TestReactors(TestCase):
    def setUp(self):
        self.volume = 10 # m3
        self.copper_conc = 2 / 63.5
        self.ferric_conc = 9 / 55.85

    def test_running_cstr_reactor_with_simplified_hansford(self):
        upstream = reactors.BaseUpStream()
        cstr = reactors.CSTR(self.volume, upstream)
        copper_rate = reactions.MetalDissolutionRate(constants.COPPER,
                                                     self.copper_conc,
                                                     self.ferric_conc,
                                                     system=constants.CONTINUOUS)

        cstr.update_component_rate(copper_rate)

        self.assertIn(copper_rate, cstr.components_rate)
        self.assertEqual(cstr.flow_in, upstream.flow_out)
        self.assertEqual(cstr.flow_in, cstr.flow_out)
        self.assertIsNotNone(cstr.flow_in)

        output = cstr.run()

        self.assertIn('total_rate_ferric', output)
        self.assertIn('total_rate_ferrous', output)
        self.assertIn('Cu', output)

        self.assertEqual(output['total_rate_ferrous'], -output['total_rate_ferric'])
        self.assertEqual(output["Cu"]['rate_ferrous'], -output["Cu"]['rate_ferric'])


class TestRunningSystem(TestCase):
    def setUp(self):
        self.volume_cstr = 10 #
        self.upstream_flow_out = {"flowrate": 1, "components": {"C_Fe2_plus": 0.1, "C_Fe3_plus": 0.2}}

    def test_system_runs_okay(self):
        sys = system.System()

        upstream = reactors.BaseUpStream(flow_out=self.upstream_flow_out)
        sys.create_reactor(reactors.CSTR, self.volume_cstr, upstream)

        # Asserts
        self.assertEqual(sys.reactor.volume, self.volume_cstr)
        self.assertEqual(sys.reactor.flow_in, self.upstream_flow_out)
        self.assertEqual(sys.reactor.flow_in, sys.reactor.flow_out)

        # Running the reactor
        output = sys.run()


class TestReactionRates(TestCase):
    def setUp(self):
        super(TestReactionRates, self).setUp()

    def test_chemical_reaction_rate(self):
        copper_conc = 2/65.3
        ferric_conc = 0.0001
        copper = reactions.MetalDissolutionRate(constants.COPPER, copper_conc, ferric_conc)
        rate_ferric = copper.copper_metal_powder_rate()

    def test_biox_reaction_rate(self):
        ferrous_conc = 0.01
        ferric_conc = 10

        biox = reactions.BioxidationRate(ferric_conc, ferrous_conc)
        biox.simplified_hansford()
