from utils.help_functions import HelpFunctions
import requests
import json


class TestInvoice:

    def test_create_invoice(self, requests_mock):
        requests_mock.real_http = True

        with open("tests/payloads/response/post_invoice.json", "r") as f:
            mock_response = json.load(f)

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
                }
            ]
        }
        response = requests.post("http://localhost:5000/invoice", json=invoice_data)

        assert response.status_code == 201
        assert len(response.json()["invoices"]) == 1

        invoice_response = response.json()["invoices"][0]
        invoice_key = invoice_response["invoice_key"]

        assert invoice_response["amount"] == "15000.00"
        assert (
            invoice_response["payer_document_number"]
            == invoice_data["invoices"][0]["payer_document_number"]
        )
        assert invoice_response["name"] == invoice_data["invoices"][0]["name"]
        assert invoice_response["brcode"] == mock_response["invoices"][0]["brcode"]
        assert (
            invoice_response["external_id"]
            == mock_response["invoices"][0]["external_id"]
        )
        assert invoice_response["pdf_url"] == mock_response["invoices"][0]["pdf_url"]
        assert invoice_response["status"] == "created"
        assert invoice_response["brcode"] == mock_response["invoices"][0]["brcode"]

        get_response = requests.get(
            f"http://localhost:5000/invoice/invoice_key/{invoice_key}",
            json=invoice_data,
        )

        assert get_response.status_code == 200
        assert get_response.json() == invoice_response
