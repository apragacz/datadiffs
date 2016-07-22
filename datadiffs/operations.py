from .freezing import freeze_data, unfreeze_data
from .protocols import DEFAULT_PROTOCOL

__REGISTRY__ = {}


class OperationType(object):
    INSERTION = 'insert'
    DELETION = 'delete'
    REPLACEMENT = 'replace'


class OperationMetaclass(type):

    def __new__(cls, name, bases, attrs):
        super_new = super().__new__
        op_type = attrs.get('TYPE')
        new_cls = super_new(cls, name, bases, attrs)
        if op_type:
            __REGISTRY__[op_type] = new_cls
        return new_cls


class Operation(metaclass=OperationMetaclass):
    TYPE = None
    FIELDS = []

    @classmethod
    def from_serializable_data(cls, data):
        op_type = data['type']
        op_cls = __REGISTRY__[op_type]
        kwargs = {
            'context': data['context'],
        }
        for field in op_cls.FIELDS:
            kwargs[field] = data[field]
        return op_cls(**kwargs)

    def __init__(self, context):
        assert isinstance(context, (tuple, list))
        self.__context = tuple(context)

    @property
    def context(self):
        return self.__context

    @property
    def type(self):
        return self.TYPE

    def __eq__(self, obj):
        if self.__class__ != obj.__class__:
            return False

        if self.context != obj.context:
            return False

        for field in self.FIELDS:
            if getattr(self, field) != getattr(obj, field):
                return False

        return True

    def __repr__(self):
        return '{0}(context={1!r}, {2})'.format(
            self.__class__.__name__,
            self.context,
            ', '.join('{0}={1!r}'.format(f, getattr(self, f))
                      for f in self.FIELDS),
        )

    def __call__(self, value, protocol=DEFAULT_PROTOCOL):
        return self._apply_on(value, self.context, protocol=protocol)

    def to_serializable_data(self):
        if not self.TYPE:
            raise NotImplementedError()
        data = {
            'type': self.type,
            'context': self.context,
        }
        for field in self.FIELDS:
            data[field] = getattr(self, field)
        return data

    def inverted(self):
        raise NotImplementedError()

    def _apply_on(self, value, ctx, protocol):
        ctx_len = len(ctx)
        if ctx_len == 0:
            return self._apply_on_empty_context(value, protocol)
        if ctx_len == 1:
            return self._apply_on_singleton_context(value, ctx[0], protocol)
        else:
            ctx_head = ctx[0]
            ctx_tail = ctx[1:]
            sub_value = protocol.navigate(value, ctx_head)
            new_sub_value = self._apply_on(sub_value, ctx_tail, protocol)
            return protocol.update(value, ctx_head, new_sub_value)

    def _apply_on_empty_context(self, value, protocol):
        raise NotImplementedError()

    def _apply_on_singleton_context(self, value, name, protocol):
        raise NotImplementedError()


class Insertion(Operation):
    TYPE = OperationType.INSERTION
    FIELDS = ['new_value']

    def __init__(self, context, new_value):
        super().__init__(context)
        self.__new_value = freeze_data(new_value)

    @property
    def new_value(self):
        return self.__new_value

    def inverted(self):
        return Deletion(context=self.context, old_value=self.new_value)

    def _apply_on_empty_context(self, value, protocol):
        return unfreeze_data(self.new_value)

    def _apply_on_singleton_context(self, value, name, protocol):
        return protocol.insert(value, name, unfreeze_data(self.new_value),
                               obj_context=self.context[:-1])


class Deletion(Operation):
    TYPE = OperationType.DELETION
    FIELDS = ['old_value']

    def __init__(self, context, old_value):
        super().__init__(context)
        self.__old_value = freeze_data(old_value)

    @property
    def old_value(self):
        return self.__old_value

    def inverted(self):
        return Insertion(context=self.context, new_value=self.old_value)

    def _apply_on_empty_context(self, value, protocol):
        return

    def _apply_on_singleton_context(self, value, name, protocol):
        return protocol.remove(value, name, obj_context=self.context[:-1])


class Replacement(Operation):
    TYPE = OperationType.REPLACEMENT
    FIELDS = ['old_value', 'new_value']

    def __init__(self, context, old_value, new_value):
        super().__init__(context)
        self.__old_value = freeze_data(old_value)
        self.__new_value = freeze_data(new_value)

    @property
    def old_value(self):
        return self.__old_value

    @property
    def new_value(self):
        return self.__new_value

    def inverted(self):
        return Replacement(
            context=self.context,
            old_value=self.new_value,
            new_value=self.old_value,
        )

    def _apply_on_empty_context(self, value, protocol):
        return unfreeze_data(self.new_value)

    def _apply_on_singleton_context(self, value, name, protocol):
        return protocol.update(value, name, unfreeze_data(self.new_value),
                               obj_context=self.context[:-1])
