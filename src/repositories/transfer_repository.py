import uuid
from models import Transfer, TransferStatus
from repositories import BaseRepository


class TransferRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)

    def create_transfer(self, amount, account) -> Transfer:
        new_transfer = Transfer()
        new_transfer.transfer_key = str(uuid.uuid4())
        new_transfer.amount = amount
        new_transfer.account = account
        new_transfer.status = self.get_enumerator(TransferStatus, "created")

        self.session.add(new_transfer)

        return new_transfer

    def update_transfer(self, transfer: Transfer, external_id=None, status=None):
        if external_id:
            transfer.external_id = external_id
        if status:
            transfer.status = self.get_enumerator(TransferStatus, status)

        self.session.add(transfer)

        return transfer

    def get_transfer_by_key(self, transfer_key) -> Transfer | None:
        return self.session.query(Transfer).filter_by(transfer_key=transfer_key).first()
