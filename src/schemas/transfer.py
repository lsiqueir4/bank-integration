from marshmallow import Schema, fields
from utils.schema import EnumField


class ResponseTransferSchema(Schema):
    transfer_key = fields.String()
    external_id = fields.String()
    amount = fields.Float()
    status = EnumField(required=True)
