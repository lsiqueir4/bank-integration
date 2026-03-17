import uuid
from requests import request


class TestAccount:
    def test_create_account(self, client):
        account_payload = {
            "bank_code": "20018183",
            "branch_code": "0001",
            "account_number": "6341320293482496",
            "owner_document_number": "20.018.183/0001-80",
            "owner_name": "Stark Bank S.A.",
            "account_type": "payment",
        }

        post_response = client.post("/account/",json=account_payload)

        assert post_response.status_code == 201
        assert post_response.get_json()["bank_code"] == account_payload["bank_code"]
        assert post_response.get_json()["branch_code"] == account_payload["branch_code"]
        assert (
            post_response.get_json()["account_number"] == account_payload["account_number"]
        )
        assert (
            post_response.get_json()["owner_document_number"]
            == account_payload["owner_document_number"]
        )
        assert post_response.get_json()["owner_name"] == account_payload["owner_name"]
        assert post_response.get_json()["account_type"] == account_payload["account_type"]
        account_key = post_response.get_json()["account_key"]
        assert uuid.UUID(account_key)

        get_response = client.get(f"/account/account_key/{account_key}")
        print(get_response.get_json())
        assert get_response.status_code == 200
        assert get_response.get_json() == post_response.get_json()

    def test_invalid_account_type(self, client):
        account_payload = {
            "bank_code": "20018183",
            "branch_code": "0001",
            "account_number": "6341320293482496",
            "owner_document_number": "20.018.183/0001-80",
            "owner_name": "Stark Bank S.A.",
            "account_type": "invalid_type",
        }

        post_response = client.post("/account/",json=account_payload)

        assert post_response.status_code == 422
        assert (
            post_response.get_json()["message"]
            == '{"account_type": ["Invalid account type"]}'
        )

    def test_invalid_owner_document_number(self, client):
        account_payload = {
            "bank_code": "20018183",
            "branch_code": "0001",
            "account_number": "6341320293482496",
            "owner_document_number": "12.345.678/0001-00",
            "owner_name": "Stark Bank S.A.",
            "account_type": "payment",
        }

        post_response = client.post("/account/",json=account_payload)
        assert post_response.status_code == 422
        assert post_response.get_json()["message"] == "Invalid owner document number."

    def test_owner_document_number(self, client):
        account_payload = {
            "bank_code": "20018183",
            "branch_code": "0001",
            "account_number": "6341320293482496",
            "owner_document_number": "12.345.678/0001-00",
            "owner_name": "Stark Bank S.A.",
            "account_type": "payment",
        }

        valid_document_number = [
            "529.982.247-25",
            "168.995.350-09",
            "111.444.777-35",
            "935.411.347-80",
            "714.602.380-01",
            "04.252.011/0001-10",
            "40.688.134/0001-61",
            "33.000.167/0001-01",
            "45.723.174/0001-10",
            "12.544.992/0001-05",
        ]
        invalid_document_number = [
            "529.982.247-24",
            "168.995.350-08",
            "111.444.777-00",
            "935.411.347-81",
            "714.602.380-99",
            "04.252.011/0001-00",
            "40.688.134/0001-00",
            "33.000.167/0001-99",
            "45.723.174/0001-00",
            "12.544.992/0001-99",
        ]

        for document_number in valid_document_number:
            account_payload["owner_document_number"] = document_number
            post_response = client.post("/account/",json=account_payload)
            assert post_response.status_code == 201

        for document_number in invalid_document_number:
            account_payload["owner_document_number"] = document_number
            post_response = client.post("/account/",json=account_payload)
            assert post_response.status_code == 422
