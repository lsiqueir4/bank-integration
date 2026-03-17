from marshmallow import Schema, fields, validate
from utils.schema import EnumField


class RequestInvoiceSchema(Schema):
    payer_document_number = fields.String(
        required=True,
        validate=[
            validate.Length(min=11, max=18),
            validate.Regexp(
                r"^(\d{11}|\d{14}|\d{3}\.?\d{3}\.?\d{3}-?\d{2}|\d{2}\.?\d{3}\.?\d{3}\/?\d{4}-?\d{2})$$",
                error="Invalid payer document number",
            ),
        ],
    )
    amount = fields.Decimal(
        required=True, as_string=False, validate=validate.Range(min=0.01)
    )
    name = fields.String(required=True, validate=validate.Length(min=2, max=255))
    transfer_account_key = fields.String(
        required=False,
        validate=validate.Regexp(
            r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$",
            error="Invalid transfer account key format",
        ),
    )
    invoice_key = fields.String(required=False)


class ResponseInvoiceSchema(Schema):
    invoice_key = fields.String()
    payer_document_number = fields.String()
    name = fields.String()
    amount = fields.Decimal(as_string=True)
    fee_amount = fields.Decimal(as_string=True)
    external_id = fields.String()
    pdf_url = fields.String()
    brcode = fields.String()
    transfer_account_key = fields.String()
    status = EnumField(required=True)


class RequestInvoiceListSchema(Schema):
    invoices = fields.List(fields.Nested(RequestInvoiceSchema), required=True)


class ResponseInvoiceListSchema(Schema):
    invoices = fields.List(fields.Nested(ResponseInvoiceSchema), required=True)
