import asyncio


magic_attributes = {
    '__doc__', '__name__', '__qualname__', '__module__', '__defaults__',
    '__code__', '__globals__', '__dict__', '__closure__', '__annotations__',
    '__kwdefaults', '__slots__'}

magic_methods = {
    '__new__', '__init__', '__del__', '__repr__', '__str__', '__bytes__',
    '__format__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__',
    '__hash__', '__bool__', '__getattr__', '__getattribute__', '__setattr__',
    '__delattr__', '__dir__', '__get__', '__set__', '__delete__',
    '__set_name__', '__init_subclass__', '__instancecheck__',
    '__subclasscheck__', '__call__', '__len__', '__length_hint__',
    '__getitem__', '__missing__', '__setitem__', '__delitem__', '__iter__',
    '__reversed__', '__contains__', '__add__', '__sub__', '__mul__',
    '__matmul__', '__truediv__', '__floordiv__', '__mod__', '__divmod__',
    '__pow__', '__lshift__', '__rshift__', '__and__', '__xor__', '__or__',
    '__radd__', '__rsub__', '__rmul__', '__rmatmul__', '__rtruediv__',
    '__rfloordiv__', '__rmod__', '__rdivmod__', '__rpow__', '__rlshift__',
    '__rrshift__', '__rand__', '__rxor__', '__ror__', '__iadd__', '__isub__',
    '__imul__', '__imatmul__', '__itruediv__', '__ifloordiv__', '__imod__',
    '__ipow__', '__ilshift__', '__irshift__', '__iand__', '__ixor__',
    '__ior__', '__neg__', '__pos__', '__abs__', '__invert__', '__complex__',
    '__int__', '__float__', '__round__', '__index__', '__enter__', '__exit__',
    '__await__', '__aiter__', '__anext__', '__aenter__', '__aexit__'}

required_magic_methods = {
    '__subclasshook__', '__getattribute__', '__getattr__', '__setattr__',
    '__delattr__', '__new__', '__init__', '__del__'}

replacable_m_m = magic_methods - required_magic_methods


class MagicMeta(type):
    """Forwards all magic methods of class to its __getattr__"""
    @classmethod
    def __prepare__(cls, name, bases):
        return {attr: cls.dummify_method(attr) for attr in replacable_m_m}

    @staticmethod
    def dummify_method(method_name):
        def call_class_getattr(self, *args, **kwargs):
            method = self.__getattr__(method_name)
            return method(*args, **kwargs)
        return call_class_getattr


class AsyncioOmen(metaclass=MagicMeta):
    def __init__(self, awaitable):
        self.__future = asyncio.ensure_future(awaitable)
        self.__is_done = False

    def __getattr__(self, name):
        if not self.__is_done:
            asyncio.get_event_loop().run_until_complete(self.__future)
            self.__result = self.__future.result()
            self.__is_done = True
        return object.__getattribute__(self.__result, name)
