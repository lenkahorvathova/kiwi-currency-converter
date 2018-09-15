import argparse
import json

from forex_python.converter import CurrencyRates, RatesNotAvailableError


class CurrencyConverter:
    currency_symbols = {
        "$": "USD",
        "£": "GBP",
        "€": "EUR",
        "¥": "CNY"
    }

    def convert(self, amount, input_currency, output_currency):
        if not self.is_valid(amount, input_currency, output_currency):
            return self.format_output(
                amount,
                input_currency,
                self.error_message("Invalid input. Check arguments!"))

        input_currency = self.resolve_symbol(input_currency)
        output_currency = self.resolve_symbol(output_currency)

        output = self.prepare_output(amount, input_currency, output_currency)

        result = self.format_output(amount, input_currency, output)
        return result

    def is_valid(self, amount, input_currency, output_currency):
        if amount < 0:
            return False
        if input_currency \
                and len(input_currency) == 1 \
                and input_currency not in self.currency_symbols:
            return False
        if output_currency \
                and len(output_currency) == 1 \
                and output_currency not in self.currency_symbols:
            return False
        return True

    def prepare_output(self, amount, input_currency, output_currency):
        if output_currency:
            try:
                value = CurrencyRates().convert(input_currency, output_currency, amount)
                value = "{0:.2f}".format(value)
            except RatesNotAvailableError:
                return self.error_message("Invalid input or output currency.")

            output = {output_currency: value}
        else:
            rates = CurrencyRates().get_rates(input_currency)

            for currency_code in rates:
                rates[currency_code] = "{0:.2f}".format(rates[currency_code] * amount)
            output = rates

        return output

    def resolve_symbol(self, currency):
        if currency and len(currency) == 1:
            currency = self.currency_symbols[currency]
        return currency

    def error_message(self, message):
        return {"error": message}

    def format_output(self, amount, input_currency, output):
        return {
            "input": {
                "amount": amount,
                "currency": input_currency
            },
            "output": output
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--amount', type=float, default=1,
                        help='an amount of money to convert')
    parser.add_argument('--input_currency', type=str,
                        help='a currency money are converted from')
    parser.add_argument('--output_currency', type=str, default=None,
                        help='a currency money are converted to')
    args = parser.parse_args()

    result = CurrencyConverter().convert(
        args.amount,
        args.input_currency,
        args.output_currency)

    print(json.dumps(result, indent=4))


main()
