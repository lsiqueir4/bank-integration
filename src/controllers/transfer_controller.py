from flask_smorest import Blueprint
from controllers import BaseController
from errors import APIError
from repositories import TransferRepository
from schemas import ResponseTransferSchema

blp = Blueprint("Transfer", __name__, url_prefix="/transfer")


class TransferController(BaseController):
    def __init__(self):
        super().__init__()
        self.transfer_bp = blp
        self.transfer_bp.add_url_rule(
            "/transfer_key/<transfer_key>",
            view_func=self.get_transfer_by_key,
            methods=["GET"],
        )
        self.transfer_repository = TransferRepository(self.db.session)

    @blp.response(200, ResponseTransferSchema)
    def get_transfer_by_key(self, transfer_key: str):
        transfer = self.transfer_repository.get_transfer_by_key(transfer_key)
        if not transfer:
            raise APIError(message="transfer not found.", status_code=404)
        return transfer
