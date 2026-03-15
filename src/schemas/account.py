from marshmallow import Schema, fields, validate
from utils.schema import EnumField


class RequestAccountSchema(Schema):
    bank_code = fields.String(
        required=True, validate=validate.Regexp(r"^\d{3,8}$", error="Invalid bank code")
    )
    branch_code = fields.String(
        required=True,
        validate=[
            validate.Length(min=4, max=10),
            validate.Regexp(r"^[0-9-]+$", error="Invalid branch code"),
        ],
    )
    account_number = fields.String(
        required=True,
        validate=[
            validate.Length(min=4, max=40),
            validate.Regexp(r"^[0-9-]+$", error="Invalid account number"),
        ],
    )
    owner_document_number = fields.String(
        required=True,
        validate=[
            validate.Length(min=11, max=18),
            validate.Regexp(
                r"^(\d{11}|\d{14}|\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2})$$",
                error="Invalid owner document number",
            ),
        ],
    )
    owner_name = fields.String(required=True, validate=validate.Length(min=2, max=255))
    account_type = fields.String(
        required=True,
        validate=validate.OneOf(
            choices=["payment", "savings", "checking", "salary"],
            error="Invalid account type",
        ),
    )


class ResponseAccountSchema(Schema):
    account_key = fields.String()
    bank_code = fields.String()
    branch_code = fields.String()
    account_number = fields.String()
    owner_document_number = fields.String()
    owner_name = fields.String()
    account_type = EnumField(required=True)
