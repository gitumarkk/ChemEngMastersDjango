# Django
from django.test import TestCase

# Project
from masters.calculations import system
from masters.calculations import constants
from masters.calculations import reactors
from masters.calculations import reactions
from masters.calculations import rates

class TestRateData(TestCase):
    def setUp(self):
        self.IRON_MR = constants.DATA[constants.IRON]["Mr"]

    def test_process_rate_data_moles_metal_reacted(self):
        rate_obj = rates.ProcessRatesData(constants.COPPER)
        moles_metal_left = rate_obj.moles_metal_left(2, -0.001)

        self.assertEqual(moles_metal_left, (2/63.546 - 0.001/2))

    def test_build_rates(self):
        rate_obj = rates.ProcessRatesData(constants.COPPER)
        output = rate_obj.run()

        calc_1 = (output["data"][1][0]["Fe3+"]["abs"] * 100 / (1000 * 0.015)) / self.IRON_MR
        self.assertEqual(output["data"][1][0]["Fe3+"]["moles"], calc_1)

        calc_2 = (output["data"][1][0]["FeTot"]["abs"] * 100 / (1000 * 0.015)) / self.IRON_MR
        self.assertEqual(output["data"][1][0]["FeTot"]["moles"], calc_2)

        self.assertGreater(output["data"][1][4]["metal"]["ion"], output["data"][1][4]["metal"]["metal"])

    def test_get_rate_constants(self):
        rate_obj = rates.RateEquation(constants.COPPER)
        output = rate_obj.run()

class TestReactors(TestCase):
    def setUp(self):
        self.volume = 10 # m3
        self.copper_conc = 2 / 63.5
        self.ferric_conc = 9 / 55.85

    def test_running_cstr_reactor_with_simplified_hansford(self):
        upstream = reactors.BaseUpStream()
        cstr = reactors.CSTR(self.volume, upstream)

        biox_rate = reactions.BioxidationRate(self.ferric_conc)

        cstr.create_components(biox_rate)
        self.assertIn(biox_rate, cstr.components)

        self.assertEqual(cstr.flow_in, upstream.flow_out)
        self.assertEqual(cstr.flow_in, cstr.flow_out)
        self.assertIsNotNone(cstr.flow_in)

        # self.assertEqual(cstr.ions[biox_rate.reactant_name], 0)

        output = cstr.run()

        self.assertIn('total_rate_ferric', output["cstr_data"])
        self.assertIn('total_rate_ferrous', output["cstr_data"])
        self.assertEqual(output["cstr_data"]['total_rate_ferrous'], -output["cstr_data"]['total_rate_ferric'])

        self.assertEqual(output["cstr_data"]['total_rate_ferrous'], output["cstr_data"]["components"][biox_rate.reactant_name]["rate_ferrous"])
        self.assertNotEqual(output["flow_out"]["components"]["ferric"], upstream.flow_out["components"]["ferric"])

        self.assertEqual(output["flow_out"]["components"]["ferric"], cstr.flow_out["components"]["ferric"])

        # Assert that the change in ferric is equal to change in rate
        self.assertAlmostEqual(output["flow_out"]["components"]["ferric"] - cstr.flow_in["components"]["ferric"],
                         output["cstr_data"]['total_rate_ferric']) # Almost equal due to floating point errors


    def test_running_cstr_reactor_with_simplified_chemical_equation(self):
        upstream = reactors.BaseUpStream()
        cstr = reactors.CSTR(self.volume, upstream)
        copper_rate = reactions.MetalDissolutionRate(constants.COPPER,
                                                     self.copper_conc,
                                                     self.ferric_conc,
                                                     system=constants.CONTINUOUS)

        cstr.create_components(copper_rate)

        self.assertIn(copper_rate, cstr.components)
        self.assertEqual(cstr.flow_in, upstream.flow_out)
        self.assertEqual(cstr.flow_in, cstr.flow_out)
        self.assertIsNotNone(cstr.flow_in)

        # self.assertEqual(cstr.ions[copper_rate.reactant_name], 0)

        output = cstr.run()

        self.assertIn('total_rate_ferric', output["cstr_data"])
        self.assertIn('total_rate_ferrous', output["cstr_data"])

        self.assertIn('Cu', output["cstr_data"]["components"])
        self.assertEqual(output["cstr_data"]['total_rate_ferrous'], -output["cstr_data"]['total_rate_ferric'])
        self.assertEqual(output["cstr_data"]["components"][copper_rate.reactant_name]['rate_ferrous'],
                         -output["cstr_data"]["components"][copper_rate.reactant_name]['rate_ferric'])

        self.assertEqual(output["cstr_data"]['total_rate_ferrous'],
                         output["cstr_data"]["components"][copper_rate.reactant_name]["rate_ferrous"])
        self.assertNotEqual(output["flow_out"]["components"]["ferric"],
                            upstream.flow_out["components"]["ferric"])

        self.assertEqual(output["flow_out"]["components"]["ferric"], cstr.flow_out["components"]["ferric"])

        # Assert that the change in ferric is equal to change in rate
        self.assertAlmostEqual(output["flow_out"]["components"]["ferric"] - cstr.flow_in["components"]["ferric"],
                         output["cstr_data"]['total_rate_ferric']) # Almost equal due to floating point errors


class TestRunningSystem(TestCase):
    def setUp(self):
        self.volume_cstr = 1 # m^3
        self.copper_conc = 2 #mol.m^-3
        self.ferric_ferrous = 1000
        self.total_iron = 9

    def test_system_runs_okay_with_cyclic_tanks_model(self):
        initial_metals = {constants.COPPER: self.copper_conc}

        sys = system.System(self.volume_cstr,
                            self.volume_cstr,
                            self.ferric_ferrous,
                            self.total_iron,
                            initial_metals=initial_metals)
        sys.build_cyclic_tanks()

        self.assertEqual(sys.biox_cstr.upstream, sys.chem_cstr)
        self.assertEqual(sys.chem_cstr.upstream, sys.biox_cstr)

        sys.step()
        # As the biox reatcor is only updated in the next step
        chem_old = sys.chem_cstr.flow_out

        # That Chem Flow in = Biox Flow out
        self.assertEqual(sys.biox_cstr.flow_out, sys.chem_cstr.flow_in)

        sys.step()
        # That Biox Flow in = Chem Flow Out (t - 1)
        self.assertEqual(chem_old, sys.biox_cstr.flow_in)
        self.assertEqual(sys.biox_cstr.flow_out, sys.chem_cstr.flow_in)

        chem_old = sys.chem_cstr.flow_out

        sys.step()
        self.assertEqual(chem_old, sys.biox_cstr.flow_in)
        # import ipdb; ipdb.set_trace()
        # pass

    def test_system_runs_okay_with_tanks_in_series_model(self):
        initial_metals = {constants.COPPER: self.copper_conc}

        # BaseUpstream -> Bioxidation -> CSTR ->
        sys = system.System(self.volume_cstr,
                            self.volume_cstr,
                            self.ferric_ferrous,
                            self.total_iron,
                            initial_metals=initial_metals)

        # upstream = reactors.BaseUpStream()
        sys.build_tanks_in_series()

        # Create Bioxidation Reactor
        # biox_cstr = sys.create_reactor(reactors.CSTR, self.volume_cstr, upstream)

        # biox_rate = reactions.BioxidationRate()

        # biox_cstr.update_component_rate(biox_rate)
        # self.assertEqual(biox_rate, biox_cstr.components_rate[0])

        # # Update component stream
        # # Asserts
        # self.assertEqual(biox_cstr.volume, self.volume_cstr)
        # self.assertEqual(biox_cstr.flow_in, upstream.flow_out)
        # self.assertEqual(biox_cstr.flow_in, biox_cstr.flow_out)

        self.assertEqual(len(sys.units), 2)
        # self.assertEqual(sys.units[0], biox_cstr)

        # Create Chemical Reactor
        # chem_cstr = sys.create_reactor(reactors.CSTR, self.volume_cstr, biox_cstr)

        # # Update component stream
        # copper_rate = reactions.MetalDissolutionRate(constants.COPPER,
        #                                              self.copper_conc,
        #                                              system=constants.CONTINUOUS)
        # chem_cstr.update_component_rate(copper_rate)
        # self.assertEqual(copper_rate.ferric, chem_cstr.ferric)
        # self.assertEqual(copper_rate, chem_cstr.components_rate[0])

        # Assetrs
        # self.assertEqual(len(sys.units), 2)
        # self.assertEqual(sys.units[1], chem_cstr)

        # self.assertEqual(chem_cstr.upstream, biox_cstr)
        # self.assertEqual(chem_cstr.flow_in, biox_cstr.flow_out)

        # Running the reactor
        output_1 = sys.step()
        self.assertEqual(len(output_1), 2)
        # print output_1

        output_2 = sys.step()
        self.assertEqual(len(output_2), 2)
        # print output_2


class TestReactionRates(TestCase):
    def setUp(self):
        super(TestReactionRates, self).setUp()

    def test_chemical_reaction_rate(self):
        copper_conc = 2/65.3
        ferric_conc = 0.0001
        copper = reactions.MetalDissolutionRate(constants.COPPER, copper_conc, ferric_conc)
        rate_ferric = copper.metal_powder_rate()

    def test_biox_reaction_rate(self):
        ferrous_conc = 0.01
        ferric_conc = 10

        biox = reactions.BioxidationRate(ferric_conc, ferrous_conc)
        biox.simplified_hansford()
