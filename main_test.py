import unittest
from unittest.mock import patch

import main


class MainTestCase(unittest.TestCase):

    def setUp(self):
        main.app.testing = True
        self.app = main.app.test_client()

    def test_convert_handler_success(self):
        with patch('main.convert_all_and_sum') as mock_convert:
            mock_convert.return_value = 100
            response = self.app.post('/convert', json={
                'amounts': [10, 20],
                'from_currency': 'USD',
                'to_currency': 'EUR'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn("Der totale Betrag nach der Umrechnung von USD zu EUR ist", str(response.data))

    def test_convert_handler_error(self):
        response = self.app.post('/convert', json={
            'amounts': [10, 20],
            'from_currency': 'XXX',
            'to_currency': 'EUR'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", str(response.data))


if __name__ == '__main__':
    unittest.main()
