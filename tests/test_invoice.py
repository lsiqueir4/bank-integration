from tests.utils.help_functions import HelpFunctions
import json
import uuid
import random


class TestInvoice:

    def test_create_invoice(self, client, requests_mock):
        requests_mock.real_http = True

        with open("tests/payloads/response/post_invoice.json", "r") as f:
            mock_response = json.load(f)
        invoice_key = str(uuid.uuid4())
        mock_response["invoices"][0]["tags"] = [invoice_key]
        mock_response["invoices"][0]["id"] = str(random.randint(1, 500) * 50)
        HelpFunctions().mock_external_request(
            requests_mock,
            method="POST",
            url="https://dev.external.com/invoice",
            json_response=mock_response,
            status_code=201,
        )

        invoice_data = {
            "invoices": [
                {
                    "payer_document_number": "95346087001",
                    "name": "Teste1",
                    "amount": 15000,
                    "invoice_key": invoice_key,
                }
            ]
        }
        post_response = client.post("/invoice/", json=invoice_data)
        print(post_response.get_json())

        assert post_response.status_code == 201
        assert len(post_response.get_json()["invoices"]) == 1

        invoice_response = post_response.get_json()["invoices"][0]

        assert invoice_key == invoice_response["invoice_key"]
        assert invoice_response["amount"] == "15000.00"
        assert (
            invoice_response["payer_document_number"]
            == invoice_data["invoices"][0]["payer_document_number"]
        )
        assert invoice_response["name"] == invoice_data["invoices"][0]["name"]
        assert invoice_response["brcode"] == mock_response["invoices"][0]["brcode"]
        assert invoice_response["external_id"] == mock_response["invoices"][0]["id"]
        assert invoice_response["pdf_url"] == mock_response["invoices"][0]["pdf"]
        assert invoice_response["status"] == "created"
        assert invoice_response["brcode"] == mock_response["invoices"][0]["brcode"]

        get_response = client.get(
            f"invoice/invoice_key/{invoice_key}",
            json=invoice_data,
        )

        assert get_response.status_code == 200
        assert get_response.get_json() == invoice_response
