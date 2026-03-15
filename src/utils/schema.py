from marshmallow import fields


class EnumField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return getattr(value, "enumerator", str(value))
