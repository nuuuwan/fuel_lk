
import unittest

from fuel_lk import scrape


class TestCase(unittest.TestCase):
    def test_scrape(self):
        actual_fuel_info_list = scrape.scrape_page('Western', 'Colombo', 'P92')

        self.assertGreater(
            len(actual_fuel_info_list),
            0,
        )

        for k in ['name', 'stock', 'time_last_update']:
            self.assertIn(
                k,
                actual_fuel_info_list[0],
            )
