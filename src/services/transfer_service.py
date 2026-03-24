from repositories import TransferRepository


class TransferService:
    def __init__(self, db_session):
        self.transfer_repository = TransferRepository(db_session)

    def handle_transfer_created(self, transfer_data):
        return

    def handle_transfer_processing(self, transfer_data):
        return

    def handle_transfer_success(self, transfer_data):
        transfer_key = transfer_data["tags"][0]
        transfer = self.transfer_repository.get_transfer_by_key(transfer_key)
        if not transfer:
            return f"Transfer not found: {transfer_key}"
        if transfer.status.enumerator != "created":
            return f"Paid Transfer in unexpected status: {transfer.status.enumerator}"

        self.transfer_repository.update_transfer(transfer, status="success")

    def handle_transfer_failed(self, transfer_data):
        transfer_key = transfer_data["tags"][0]
        transfer = self.transfer_repository.get_transfer_by_key(transfer_key)
        if not transfer:
            return f"Transfer not found: {transfer_key}"
        if transfer.status.enumerator != "created":
            return f"Paid Transfer in unexpected status: {transfer.status.enumerator}"

        self.transfer_repository.update_transfer(transfer, status="failed")

    def handle_transfer_canceled(self, transfer_data):
        transfer_key = transfer_data["tags"][0]
        transfer = self.transfer_repository.get_transfer_by_key(transfer_key)
        if not transfer:
            return f"Transfer not found: {transfer_key}"
        if transfer.status.enumerator != "created":
            return f"Paid Transfer in unexpected status: {transfer.status.enumerator}"

        self.transfer_repository.update_transfer(transfer, status="canceled")

    def process(self, payload):
        status = payload.get("log", {}).get("transfer", {}).get("status")
        handler = {
            "success": self.handle_transfer_success,
            "processing": self.handle_transfer_processing,
            "created": self.handle_transfer_created,
            "canceled": self.handle_transfer_canceled,
            "failed": self.handle_transfer_failed,
        }.get(status)

        if not handler:
            return f"Transfer status not found: {status}"

        return handler(payload["log"]["transfer"])
