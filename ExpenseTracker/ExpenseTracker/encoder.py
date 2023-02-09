from flask.json import JSONEncoder
import json
import six
from ExpenseTracker.models.base_model_ import Model

from ExpenseTracker.models.User import User
from ExpenseTracker.models.Expense import Expense
from ExpenseTracker.models.Permissions import Permissions

class CustomJSONEncoder(JSONEncoder):
    include_nulls = False

    def default(self, o):
        if isinstance(o, Model):
            dikt = {}
            for attr, _ in six.iteritems(o.swagger_types):
                value = getattr(o, attr)
                if value is None and not self.include_nulls:
                    continue
                attr = o.attribute_map[attr]
                dikt[attr] = value
            return dikt
        return JSONEncoder.default(self, o)

def box_identity(user: User, persmissions: Permissions):
    token={}
    token["user"]= json.dumps(user, cls=CustomJSONEncoder)
    token["permissions"] = json.dumps(persmissions, cls=CustomJSONEncoder)
    return token

def unbox_identity(token):
    user,permissions = None, None
    if "user" in token and "permissions" in token:
        user = User.from_dict(json.loads(token["user"]))
        permissions = Permissions.from_dict(json.loads(token["permissions"]))        
    return user,permissions
