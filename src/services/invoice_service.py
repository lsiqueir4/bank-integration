from repositories import InvoiceRepository


class InvoiceService:
    def __init__(self, db_session):
        self.invoice_repository = InvoiceRepository(db_session)

    def handle_invoice_created(self, invoice_data):
        return

    def handle_invoice_paid(self, invoice_data):
        invoice_key = invoice_data["tags"][0]
        invoice = self.invoice_repository.get_invoice_by_key(invoice_key)
        if not invoice:
            return f"Invoice not found: {invoice_key}"
        if invoice.status.enumerator == "paid":
            return
        if invoice.status.enumerator != "created":
            return f"Paid Invoice in unexpected status: {invoice.status.enumerator}"

        self.invoice_repository.update_invoice_status(invoice, "paid")

    def handle_invoice_credited(self, invoice_data):
        invoice_key = invoice_data["tags"][0]
        invoice = self.invoice_repository.get_invoice_by_key(invoice_key)
        if not invoice:
            return f"Invoice not found: {invoice_key}"
        if invoice.status.enumerator == "credited":
            return
        if invoice.status.enumerator != "paid":
            return f"Credited Invoice in unexpected status: {invoice.status.enumerator}"

        if invoice.transfer_account_key:
            try:
                # Simulate transfer to client account
                pass
            except Exception as e:
                # Alert
                return f"Error transfering credited invoice amount: {str(e)}"

        self.invoice_repository.update_invoice_status(invoice, "credited")

    def process(self, payload):
        status = payload.get("log", {}).get("status")
        handler = {
            "paid": self.handle_invoice_paid,
            "credited": self.handle_invoice_credited,
            "created": self.handle_invoice_created,
        }.get(status)

        if not handler:
            return f"Invoice status not found: {status}"

        handler(payload["log"]["invoice"])
