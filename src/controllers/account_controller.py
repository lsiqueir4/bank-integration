from flask_smorest import Blueprint
from controllers import BaseController
from errors import APIError
from repositories import AccountRepository
from schemas import RequestAccountSchema, ResponseAccountSchema
from utils.validations import validate_document_number

blp = Blueprint("Account", __name__, url_prefix="/account")


class AccountController(BaseController):
    def __init__(self):
        super().__init__()
        self.account_bp = blp
        self.account_bp.add_url_rule(
            "/account_key/<account_key>",
            view_func=self.get_account_by_key,
            methods=["GET"],
        )
        self.account_bp.add_url_rule(
            "/", view_func=self.create_account, methods=["POST"]
        )
        self.account_repository = AccountRepository(self.db.session)

    @blp.arguments(RequestAccountSchema)
    @blp.response(201, ResponseAccountSchema)
    def create_account(self, account_data):
        account_type = self.account_repository.get_account_type(
            account_data["account_type"]
        )
        if not account_type:
            raise APIError(message="Invalid account type.", status_code=400)
        if not validate_document_number(account_data["owner_document_number"]):
            raise APIError(message="Invalid owner document number.", status_code=422)

        account = self.account_repository.create_account(
            account_data=account_data, account_type=account_type
        )
        self.account_repository.session.commit()

        return account

    @blp.response(200, ResponseAccountSchema)
    def get_account_by_key(self, account_key: str):
        account = self.account_repository.get_account_by_key(account_key)
        if not account:
            raise APIError(message="account not found.", status_code=404)
        return account
