import urllib.request
import json
import random
import uuid


def lambda_handler(event, context):
    def generate_individual_document_number():
        numbers = [random.randint(0, 9) for _ in range(9)]

        numbers_sum = sum([(10 - i) * numbers[i] for i in range(9)])
        first_digit = 11 - numbers_sum % 11
        first_digit = 0 if first_digit >= 10 else first_digit
        numbers.append(first_digit)

        numbers_sum = sum([(11 - i) * numbers[i] for i in range(10)])
        second_digit = 11 - numbers_sum % 11
        second_digit = 0 if second_digit >= 10 else second_digit
        numbers.append(second_digit)

        return "".join(map(str, numbers))

    url = "http://13.58.112.146:5000/invoice"

    invoice_list = []
    for i in range(random.randint(8, 12)):
        invoice_payload = {
            "payer_document_number": generate_individual_document_number(),
            "name": str(uuid.uuid4()),
            "amount": random.randint(1, 20) * 1000,
            "transfer_account_key": "117f2f7c-6dee-40fd-af95-3accfb05688a",
        }
        invoice_list.append(invoice_payload)

    payload = {"invoices": invoice_list}

    try:
        data = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(
            url, data=data, headers={"Content-Type": "application/json"}, method="POST"
        )

        with urllib.request.urlopen(req) as response:
            body = response.read().decode()

        return {"statusCode": response.status, "body": body}

    except Exception as e:
        return {"statusCode": 500, "error": str(e)}
