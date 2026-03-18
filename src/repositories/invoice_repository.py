import uuid
from models import Invoice, InvoiceStatus
from repositories import BaseRepository


class InvoiceRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)

    def create_invoice(self, invoice_data, invoice_key=str(uuid.uuid4())) -> Invoice:
        new_invoice = Invoice()
        new_invoice.invoice_key = invoice_key
        new_invoice.payer_document_number = invoice_data["payer_document_number"]
        new_invoice.amount = invoice_data["amount"]
        new_invoice.status = self.get_enumerator(InvoiceStatus, "created")
        new_invoice.name = invoice_data["name"]
        new_invoice.transfer_account_key = invoice_data.get("transfer_account_key")

        self.session.add(new_invoice)

        return new_invoice

    def get_invoice_by_key(self, invoice_key) -> Invoice | None:
        return self.session.query(Invoice).filter_by(invoice_key=invoice_key).first()

    def update_invoice(
        self,
        invoice: Invoice,
        fee_amount=None,
        external_id=None,
        pdf_url=None,
        brcode=None,
        status=None,
    ):
        if fee_amount is not None:
            invoice.fee_amount = fee_amount
        if external_id is not None:
            invoice.external_id = external_id
        if pdf_url is not None:
            invoice.pdf_url = pdf_url
        if brcode is not None:
            invoice.brcode = brcode
        if status is not None:
            self.update_invoice_status(invoice, status=status)
        return invoice

    def update_invoice_status(self, invoice: Invoice, status):
        invoice.status = self.get_enumerator(InvoiceStatus, status)
