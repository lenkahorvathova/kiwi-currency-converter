from forex_python.converter import CurrencyRates, RatesNotAvailableError


class CurrencyConverter:
    currency_symbols = {
        "$": "USD",
        "£": "GBP",
        "€": "EUR",
        "¥": "CNY"
    }

    @staticmethod
    def convert(amount, input_currency, output_currency):
        if not CurrencyConverter.is_valid(amount, input_currency, output_currency):
            return CurrencyConverter.format_output(
                amount,
                input_currency,
                CurrencyConverter.error_message("Invalid input. Check arguments!"))

        input_currency = CurrencyConverter.resolve_symbol(input_currency)
        if output_currency:
            output_currency = CurrencyConverter.resolve_symbol(output_currency)

        output = CurrencyConverter.prepare_output(amount, input_currency, output_currency)

        result = CurrencyConverter.format_output(amount, input_currency, output)
        return result

    @staticmethod
    def is_valid(amount, input_currency, output_currency):
        if amount < 0:
            return False
        if not input_currency:
            return False
        if input_currency \
                and len(input_currency) == 1 \
                and input_currency not in CurrencyConverter.currency_symbols:
            return False
        if output_currency \
                and len(output_currency) == 1 \
                and output_currency not in CurrencyConverter.currency_symbols:
            return False
        return True

    @staticmethod
    def prepare_output(amount, input_currency, output_currency):
        if output_currency:
            try:
                value = CurrencyRates().convert(input_currency, output_currency, amount)
                value = "{0:.2f}".format(value)
            except RatesNotAvailableError:
                return CurrencyConverter.error_message("Invalid input or output currency.")

            output = {output_currency: value}
        else:
            rates = CurrencyRates().get_rates(input_currency)

            for currency_code in rates:
                rates[currency_code] = "{0:.2f}".format(rates[currency_code] * amount)
            output = rates

        return output

    @staticmethod
    def resolve_symbol(currency):
        if len(currency) == 1:
            currency = CurrencyConverter.currency_symbols[currency]
        return currency

    @staticmethod
    def error_message(message):
        return {"error": message}

    @staticmethod
    def format_output(amount, input_currency, output):
        return {
            "input": {
                "amount": amount,
                "currency": input_currency
            },
            "output": output
        }
