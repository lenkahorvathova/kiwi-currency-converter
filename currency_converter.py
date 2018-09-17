import argparse
import json

from converter.libs.currency_converter import CurrencyConverter


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
