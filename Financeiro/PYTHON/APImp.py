import mercadopago

sdk = mercadopago.SDK("TEST-7361780537087791-100218-568b4809c6dd0a58d6668ae409d83756-777050022")

request_options = mercadopago.config.RequestOptions()
request_options.custom_headers = {
    'x-idempotency-key': '<SOME_UNIQUE_VALUE>'
}

payment_data = {
    "itens": [
        {"id": "1", "title": "Mensalidade", "quantity": 1, "Currency_id": "BRL", "unit_price": 259.99},
    ],
    "back_urls": {
        
    }
}
result = sdk.payment().create(payment_data, request_options)
payment = result["response"]

print(payment)