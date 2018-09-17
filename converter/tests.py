from django.test import TestCase, Client


class SimpleTest(TestCase):
    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self.client = Client()

    def test_basic(self):
        response = self.client.get('/currency_converter?amount=100&input_currency=EUR&output_currency=CZK')
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['input']['amount'], 100)
        self.assertEqual(response_json['input']['currency'], 'EUR')
        self.assertIsNotNone(response_json['output']['CZK'])

    def test_input_symbol(self):
        response = self.client.get('/currency_converter?amount=0.9&input_currency=¥&output_currency=AUD')
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['input']['amount'], 0.9)
        self.assertEqual(response_json['input']['currency'], 'CNY')
        self.assertIsNotNone(response_json['output']['AUD'])

    def test_output_symbol(self):
        response = self.client.get('/currency_converter?amount=50&input_currency=CZK&output_currency=$')
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['input']['amount'], 50)
        self.assertEqual(response_json['input']['currency'], 'CZK')
        self.assertIsNotNone(response_json['output']['USD'])

    def test_missing_output(self):
        response = self.client.get('/currency_converter?amount=10.92&input_currency=£')
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['input']['amount'], 10.92)
        self.assertEqual(response_json['input']['currency'], 'GBP')
        self.assertIsNotNone(response_json['output'])

    def test_invalid_output(self):
        response = self.client.get('/currency_converter?amount=210&input_currency=CAD&output_currency=XX')
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json['input']['amount'], 210)
        self.assertEqual(response_json['input']['currency'], 'CAD')
        self.assertIsNotNone(response_json['output']['error'])

    def test_invalid_input_amount(self):
        response = self.client.get('/currency_converter?amount=money&input_currency=CAD&output_currency=CNY')
        self.assertEqual(response.status_code, 400)

        response_json = response.json()
        self.assertIsNotNone(response_json['error'])
