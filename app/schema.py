from marshmallow import Schema, fields


class TransactionSchema(Schema):
    id = fields.Integer()
    amount = fields.Decimal()
    name = fields.Str()
    timestamp = fields.DateTime()
    stock_id = fields.Integer()


class StockSchema(Schema):
    id = fields.Integer()
    company_name = fields.Str()
    current_value = fields.Decimal()