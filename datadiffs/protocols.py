from .exceptions import InvalidValueState


class ValueProtocol(object):

    def is_index(self, name, obj_context=None):
        raise NotImplementedError()

    def navigate(self, obj, name, obj_context=None):
        raise NotImplementedError()

    def insert(self, obj, name, value, obj_context=None):
        fun = (self.insert_index
               if self.is_index(name, obj_context=obj_context)
               else self.insert_key)
        return fun(obj, name, value, obj_context=obj_context)

    def remove(self, obj, name, obj_context=None):
        fun = (self.remove_index
               if self.is_index(name, obj_context=obj_context)
               else self.remove_key)
        return fun(obj, name, obj_context=obj_context)

    def update(self, obj, name, value, obj_context=None):
        fun = (self.update_index
               if self.is_index(name, obj_context=obj_context)
               else self.update_key)
        return fun(obj, name, value, obj_context=obj_context)


class ImmutableDictListProtocol(ValueProtocol):

    def is_index(self, name, obj_context=None):
        return isinstance(name, int)

    def navigate(self, obj, name, obj_context=None):
        return obj[name]

    def insert_key(self, obj, key, value, obj_context=None):
        if key in obj:
            raise InvalidValueState("key {0} already exists".format(key))
        obj_copy = obj.copy()
        obj_copy[key] = value
        return obj_copy

    def update_key(self, obj, key, value, obj_context=None):
        try:
            if obj[key] is value:
                return obj
        except KeyError:
            raise InvalidValueState("key {0} does not exist".format(key))
        obj_copy = obj.copy()
        obj_copy[key] = value
        return obj_copy

    def remove_key(self, obj, key, obj_context=None):
        if key not in obj:
            raise InvalidValueState("key {0} does not exist".format(key))
        obj_copy = obj.copy()
        del obj_copy[key]
        return obj_copy

    def insert_index(self, obj, index, value, obj_context=None):
        objtype = type(obj)
        return obj[0:index] + objtype([value]) + obj[index:]

    def update_index(self, obj, index, value, obj_context=None):
        try:
            if obj[index] is value:
                return obj
        except IndexError:
            raise InvalidValueState("index {0} does not exist".format(index))

        objtype = type(obj)
        return obj[0:index] + objtype([value]) + obj[index + 1:]

    def remove_index(self, obj, index, obj_context=None):
        if index >= len(obj):
            raise InvalidValueState("index {0} does not exist".format(index))
        return obj[0:index] + obj[index + 1:]


DEFAULT_PROTOCOL = ImmutableDictListProtocol()
