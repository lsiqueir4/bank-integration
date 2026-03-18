import uuid
from tests.utils.help_functions import HelpFunctions


class TestWebhook:
    def setup_class(self):
        self.help_functions = HelpFunctions()

    def test_invoice_webhooks(self, client, requests_mock):
        account_key = self.help_functions.create_account(client)
        requests_mock.real_http = True
        invoice_key = str(uuid.uuid4())
        HelpFunctions().mock_external_request(
            requests_mock,
            method="POST",
            url="https://dev.external.com/invoice",
            json_response=self.help_functions.create_mock_invoice_response(invoice_key),
            status_code=201,
        )

        invoice_data = {
            "invoices": [
                {
                    "payer_document_number": "95346087001",
                    "name": "Teste1",
                    "amount": 15000,
                    "invoice_key": invoice_key,
                    "transfer_account_key": account_key,
                }
            ]
        }
        invoice_post_response = client.post("/invoice/", json=invoice_data)
        print(invoice_post_response.get_json())

        assert invoice_post_response.status_code == 201

        webhook_request_payload = self.help_functions.test_webhook_request_payload(
            invoice_key, "invoice_created"
        )

        webhook_post_response = client.post("/webhook/", json=webhook_request_payload)

        assert webhook_post_response.status_code == 201

        webhook_response = webhook_post_response.get_json()

        assert webhook_response["failure_reason"] is None
        assert uuid.UUID(webhook_response["webhook_key"])
        assert webhook_response["external_id"] is not None
        assert webhook_response["webhook_type"] == "invoice_created"
        assert webhook_response["status"] == "processed"

        webhook_request_payload = self.help_functions.test_webhook_request_payload(
            invoice_key, "invoice_paid"
        )

        webhook_post_response = client.post("/webhook/", json=webhook_request_payload)

        assert webhook_post_response.status_code == 201

        webhook_response = webhook_post_response.get_json()

        assert webhook_response["failure_reason"] is None
        assert uuid.UUID(webhook_response["webhook_key"])
        assert webhook_response["external_id"] is not None
        assert webhook_response["webhook_type"] == "invoice_paid"
        assert webhook_response["status"] == "processed"

        get_invoice_response = client.get(
            f"invoice/invoice_key/{invoice_key}",
            json=invoice_data,
        )

        assert get_invoice_response.status_code == 200
        assert get_invoice_response.get_json()["status"] == "paid"

        webhook_request_payload = self.help_functions.test_webhook_request_payload(
            invoice_key, "invoice_credited"
        )

        webhook_post_response = client.post("/webhook/", json=webhook_request_payload)

        assert webhook_post_response.status_code == 201

        webhook_response = webhook_post_response.get_json()

        assert webhook_response["failure_reason"] is None
        assert uuid.UUID(webhook_response["webhook_key"])
        assert webhook_response["external_id"] is not None
        assert webhook_response["webhook_type"] == "invoice_credited"
        assert webhook_response["status"] == "processed"

        get_invoice_response = client.get(
            f"invoice/invoice_key/{invoice_key}",
            json=invoice_data,
        )

        assert get_invoice_response.status_code == 200
        assert get_invoice_response.get_json()["status"] == "credited"
