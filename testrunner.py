# Author: Annabelle Wright, 2024

import unittest
from slcsp import open_zip_codes_and_build_dictionary, open_plans_and_build_dictionary, get_slcsp_rate


class TestCases(unittest.TestCase):
    def test_open_zip_codes_and_build_dictionary(self):
        expected_output = {
            '63625': ('MO', '9'),
            '64147': ('MO', '3'),
            '34682': ('FL', '52'),
            '72365': ('AR', '2'),
            '20715': ('MD', '3'),
            '57481': ('SD', '3'),
            '79358': ('TX', '26'),
            '62957': None,
            '64132': ('MO', '3'),
        }
        zip_dict = open_zip_codes_and_build_dictionary('testData/test_zips.csv')
        self.assertEqual(expected_output, zip_dict)

    def test_open_plans_and_build_dictionary(self):
        expected_output = {
            ('WI', '12'): {'Silver': ['398.72']},
            ('MO', '7'): {'Bronze': ['216.17']},
            ('AL', '1'): {'Bronze': ['207.1']},
            ('OH', '16'): {'Bronze': ['395.92'], 'Silver': ['353.02', '359.2', '361.65']},
            ('FL', '48'): {'Silver': ['335.07', '335.25']},
        }

        plans_dict = open_plans_and_build_dictionary('testData/test_plans.csv')
        self.assertEqual(expected_output, plans_dict)

    def test_get_slcsp_rate_valid(self):
        test_input = {'Bronze': ['395.92'], 'Silver': ['290.05', '234.6', '265.82', '251.08', '351.6', '312.06', '245.2', '265.25', '253.65', '319.57', '271.64', '298.87', '341.24']}
        expected_output = (True, '245.2')
        output = get_slcsp_rate(test_input)
        self.assertEqual(expected_output, output)

    def test_get_slcp_rate_invalid(self):
        test_input = {'Bronze': ['395.92'], 'Silver': ['353.02']}
        expected_output = (False, 0)
        output = get_slcsp_rate(test_input)
        self.assertEqual(expected_output, output)


if __name__ == '__main__':
    unittest.main()
