import uuid
from models import Account, AccountType
from repositories import BaseRepository


class AccountRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)

    def create_account(self, account_data, account_type):
        new_account = Account()
        new_account.account_key = str(uuid.uuid4())
        new_account.bank_code = account_data["bank_code"]
        new_account.branch_code = account_data["branch_code"]
        new_account.account_number = account_data["account_number"]
        new_account.owner_document_number = account_data["owner_document_number"]
        new_account.owner_name = account_data["owner_name"]
        new_account.account_type = account_type

        self.session.add(new_account)

        return new_account

    def get_account_by_key(self, account_key):
        return self.session.query(Account).filter_by(account_key=account_key).first()

    def get_account_type(self, account_type):
        return (
            self.session.query(AccountType).filter_by(enumerator=account_type).first()
        )
