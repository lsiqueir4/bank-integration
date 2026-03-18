from repositories import InvoiceRepository, AccountRepository, TransferRepository
from connectors import StarkConnector


class InvoiceService:
    def __init__(self, db_session):
        self.invoice_repository = InvoiceRepository(db_session)
        self.account_repository = AccountRepository(db_session)
        self.transfer_repository = TransferRepository(db_session)
        self.stark_connector = StarkConnector()

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

        fee_amount = invoice_data["fee"]
        amount_to_send = invoice.amount - fee_amount
        if invoice.transfer_account_key and amount_to_send > 0:
            account = self.account_repository.get_account_by_key(
                invoice.transfer_account_key
            )
            if not account:
                return f"Transfer account not found: {invoice.transfer_account_key}"

            transfer = self.transfer_repository.create_transfer(
                amount=amount_to_send, account=account
            )

            self.invoice_repository.session.flush()

            try:
                transfer_request_payload = self.stark_connector.create_transfer_payload(
                    amount=float(amount_to_send),
                    receiver_document_number=account.owner_document_number,
                    receiver_name=account.owner_name,
                    target_account_bank_code=account.bank_code,
                    target_account_branch_code=account.branch_code,
                    target_account_account_number=account.account_number,
                    control_key=invoice.invoice_key,
                    description=f"Transfer for credited invoice: {invoice.invoice_key}",
                )
                transfer_response = self.stark_connector.send_transfers(
                    payload={"transfers": [transfer_request_payload]}
                )
                if transfer_response["transfers"][0]["status"].lower() != "created":
                    return f"Unexpected transfer status: {transfer_response['transfers'][0]['status']}"

                self.transfer_repository.update_transfer(
                    transfer=transfer,
                    external_id=transfer_response["transfers"][0]["id"],
                )
                self.invoice_repository.update_invoice(
                    invoice=invoice, transfer_key=transfer.transfer_key
                )
            except Exception as e:
                # Alert
                return f"Error transfering credited invoice amount: {str(e)}"

        self.invoice_repository.update_invoice(
            invoice, status="credited", fee_amount=fee_amount
        )

    def process(self, payload):
        status = payload.get("log", {}).get("type")
        handler = {
            "paid": self.handle_invoice_paid,
            "credited": self.handle_invoice_credited,
            "created": self.handle_invoice_created,
        }.get(status)

        if not handler:
            return f"Invoice status not found: {status}"

        return handler(payload["log"]["invoice"])
