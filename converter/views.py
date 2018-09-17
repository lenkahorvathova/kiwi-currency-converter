from django.http import JsonResponse
from converter.libs.currency_converter import CurrencyConverter


def index(request):
    if request.method == 'GET':
        amount = request.GET.get('amount', None)
        input_currency = request.GET.get('input_currency', None)
        output_currency = request.GET.get('output_currency', None)

        if amount:
            try:
                amount = float(amount)
            except ValueError:
                return JsonResponse(
                    CurrencyConverter.error_message('Amount "%s" is an invalid float value.' % amount),
                    status=400)

        result = CurrencyConverter.convert(amount, input_currency, output_currency)

        return JsonResponse(result, status=200)
