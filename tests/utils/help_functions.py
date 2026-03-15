from utils.generators import (
    generate_random_email,
    generate_individual_document_number,
    generate_company_document_number,
)
from requests import request
from uuid import UUID


class HelpFunctions:
    def __init__(self):
        pass

    def create_user(self, password="securepassword123", role="admin"):
        email = generate_random_email()

        register_user_response = request(
            method="POST",
            url="http://localhost:5000/auth/register",
            json={"email": email, "password": password, "role": role},
        )

        assert register_user_response.status_code == 201

        login_response = request(
            method="POST",
            url="http://localhost:5000/auth/login",
            json={"email": email, "password": password},
        )

        assert login_response.status_code == 200
        assert "access_token" in login_response.json()

        access_token = login_response.json()["access_token"]

        get_current_user_response = request(
            method="GET",
            url="http://localhost:5000/auth",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        assert get_current_user_response.status_code == 200
        assert get_current_user_response.json()["email"] == email
        assert get_current_user_response.json()["role"] == role
        assert get_current_user_response.json()["status"] == "active"
        assert UUID(get_current_user_response.json()["user_key"])

        return {
            "email": email,
            "password": password,
            "access_token": access_token,
            "user_key": get_current_user_response.json()["user_key"],
        }

    def create_person(
        self, role="admin", admin_data=None, registration_type=None, company_key=None
    ):
        user_data = self.create_user(role=role)
        if role == "admin":
            admin_data = user_data
        document_number = generate_individual_document_number()

        person_payload = {
            "document_number": document_number,
            "name": "John Doe",
            "user_key": user_data["user_key"],
        }
        if role == "user":
            person_payload["registration_number"] = (
                generate_individual_document_number()
            )
        if registration_type:
            person_payload["registration_type"] = registration_type
        if company_key:
            person_payload["company_key"] = company_key

        post_response = request(
            method="POST",
            url="http://localhost:5000/person/",
            json=person_payload,
            headers={"Authorization": f"Bearer {admin_data['access_token']}"},
        )

        assert post_response.status_code == 201

        return user_data

    def create_company(self, admin_person, phone=None, website=None, email=None):
        document_number = generate_company_document_number()
        company_payload = {
            "document_number": document_number,
            "name": "Clínica Exemplo LTDA",
            "logo_url": "https://i.imgur.com/YMJGtCG.jpeg",
            "address": {
                "street": "123 Innovation Drive",
                "city": "Techville",
                "state": "CA",
                "postal_code": "12345612",
                "country": "USA",
                "neighborhood": "Downtown",
                "complement": "Suite 500",
                "number": "1001",
            },
        }
        if phone:
            company_payload["phone"] = phone

        if website:
            company_payload["website"] = website

        if email:
            company_payload["email"] = email

        post_response = request(
            method="POST",
            url="http://localhost:5000/company/",
            json=company_payload,
            headers={"Authorization": f"Bearer {admin_person['access_token']}"},
        )

        assert post_response.status_code == 201

        return post_response.json()
