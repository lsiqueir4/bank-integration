from flask_smorest import Blueprint
from controllers import BaseController
from connectors import StarkConnector
from errors import APIError
from repositories import InvoiceRepository, AccountRepository
from schemas import (
    RequestInvoiceListSchema,
    ResponseInvoiceListSchema,
    ResponseInvoiceSchema,
)
from utils.validations import validate_document_number
from uuid import uuid4

blp = Blueprint("Invoice", __name__, url_prefix="/invoice")


class InvoiceController(BaseController):
    def __init__(self):
        super().__init__()
        self.invoice_bp = blp
        self.invoice_bp.add_url_rule(
            "/invoice_key/<invoice_key>",
            view_func=self.get_invoice_by_key,
            methods=["GET"],
        )
        self.invoice_bp.add_url_rule(
            "", view_func=self.create_invoice, methods=["POST"]
        )
        self.invoice_repository = InvoiceRepository(self.db.session)
        self.account_repository = AccountRepository(self.db.session)
        self.stark_connector = StarkConnector()

    @blp.arguments(RequestInvoiceListSchema)
    @blp.response(201, ResponseInvoiceListSchema)
    def create_invoice(self, invoice_list):
        invoices_to_send = []
        invoice_dict = {}
        invoice_list = invoice_list["invoices"]
        for invoice_data in invoice_list:
            if not validate_document_number(invoice_data["payer_document_number"]):
                raise APIError(
                    message=f"Invalid payer document number: {invoice_data['payer_document_number']}.",
                    status_code=422,
                )

            if invoice_data.get("transfer_account_key"):
                transfer_account = self.account_repository.get_account_by_key(
                    invoice_data["transfer_account_key"]
                )
                if not transfer_account:
                    raise APIError(
                        message=f"Transfer account not found: {invoice_data['transfer_account_key']}.",
                        status_code=404,
                    )
            invoice_key = invoice_data.get("invoice_key", str(uuid4()))
            invoice = self.invoice_repository.create_invoice(
                invoice_data=invoice_data, invoice_key=invoice_key
            )
            invoices_to_send.append(
                self.prepare_invoice_payload(invoice_data, invoice_key)
            )
            invoice_dict.update({invoice_key: invoice})

        self.invoice_repository.session.flush()

        invoices_response = self.stark_connector.send_invoices(
            {"invoices": invoices_to_send}
        )

        for invoice_response in invoices_response["invoices"]:
            invoice_key = invoice_response["tags"][0]
            invoice = invoice_dict[invoice_key]
            invoice = self.invoice_repository.update_invoice(
                invoice,
                fee_amount=invoice_response["fee"],
                external_id=invoice_response["id"],
                pdf_url=invoice_response["pdf"],
                brcode=invoice_response["brcode"],
                status=invoice_response["status"].lower(),
            )

        self.invoice_repository.session.commit()

        return {"invoices": list(invoice_dict.values())}

    @blp.response(200, ResponseInvoiceSchema)
    def get_invoice_by_key(self, invoice_key: str):
        invoice = self.invoice_repository.get_invoice_by_key(invoice_key)
        if not invoice:
            raise APIError(message="invoice not found.", status_code=404)
        return invoice

    def prepare_invoice_payload(self, payload, invoice_key):
        return {
            "taxId": payload["payer_document_number"],
            "name": payload["name"],
            "amount": int(payload["amount"]),
            "tags": [invoice_key],
        }
