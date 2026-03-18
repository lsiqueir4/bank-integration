from marshmallow import Schema, fields
from utils.schema import EnumField


class ResponseWebhookSchema(Schema):
    webhook_key = fields.String()
    external_id = fields.String()
    webhook_type = EnumField(required=False)
    status = EnumField(required=True)
    failure_reason = fields.String()
