import json
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class BaseModel(object):
    def to_json(self):
        if not hasattr(self, 'TAG'):
            raise NotImplementedError
        return json.dumps({self.TAG: self.to_dict()}, indent=2)

    def to_dict(self):
        return self.get_pub_vars()

    def get_pub_vars(self):
        pub_vars = {}
        for attr_name in vars(self):
            if attr_name[0] != '_':
                pub_vars[attr_name] = vars(self)[attr_name]
        return pub_vars
