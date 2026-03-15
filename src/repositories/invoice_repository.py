import uuid
from models import Invoice, InvoiceStatus
from repositories import BaseRepository


class InvoiceRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)

    def create_invoice(self, invoice_data, invoice_key=str(uuid.uuid4())):
        new_invoice = Invoice()
        new_invoice.invoice_key = invoice_key
        new_invoice.payer_document_number = invoice_data["payer_document_number"]
        new_invoice.amount = invoice_data["amount"]
        new_invoice.status = self.get_enumerator(InvoiceStatus, "created")
        new_invoice.name = invoice_data["name"]
        new_invoice.transfer_account_key = invoice_data.get("transfer_account_key")

        self.session.add(new_invoice)

        return new_invoice

    def get_invoice_by_key(self, invoice_key):
        return self.session.query(Invoice).filter_by(invoice_key=invoice_key).first()

    def update_invoice(self, invoice: Invoice, update_data):
        invoice.fee_amount = update_data["fee"]
        invoice.external_id = update_data["id"]
        invoice.pdf_url = update_data["pdf"]
        invoice.brcode = update_data["brcode"]
        invoice.status = self.get_enumerator(InvoiceStatus, update_data["status"])

        return invoice
