import decimal
from json import JSONEncoder

class DateJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(DateJSONEncoder, self).default(obj)