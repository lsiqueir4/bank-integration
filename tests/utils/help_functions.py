import json
import random


class HelpFunctions:
    def mock_external_request(
        self, mock, method, url, json_response=None, status_code=200
    ):
        getattr(mock, method.lower())(
            url, json=json_response or {}, status_code=status_code
        )

    def create_account(self, client):
        account_payload = {
            "bank_code": "20018183",
            "branch_code": "0001",
            "account_number": "6341320293482496",
            "owner_document_number": "20.018.183/0001-80",
            "owner_name": "Stark Bank S.A.",
            "account_type": "payment",
        }

        account_post_response = client.post("/account/", json=account_payload)

        assert account_post_response.status_code == 201
        return account_post_response.get_json()["account_key"]

    def create_mock_invoice_response(self, invoice_key):
        with open("tests/payloads/response/post_invoice.json", "r") as f:
            mock_response = json.load(f)
        mock_response["invoices"][0]["tags"] = [invoice_key]
        mock_response["invoices"][0]["id"] = str(random.randint(1, 500) * 50)
        return mock_response

    def test_webhook_request_payload(self, invoice_key, webhook_type: str):
        file_name = {
            "invoice_created": "post_webhook_invoice_created",
            "invoice_paid": "post_webhook_invoice_paid",
            "invoice_credited": "post_webhook_invoice_credited",
        }.get(webhook_type)

        with open(f"tests/payloads/request/{file_name}.json", "r") as f:
            payload = json.load(f)
        payload["event"]["log"]["invoice"]["tags"] = [invoice_key]
        payload["event"]["id"] = str(random.randint(1, 500) * 50)
        return payload
