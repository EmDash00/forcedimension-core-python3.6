import ctypes as ct
from ctypes import POINTER, c_double, c_int, c_ubyte, c_uint, c_ushort
from typing import (
    TYPE_CHECKING, Any, Container, Sized, Tuple, TypeVar, Union
)

from typing_extensions import Literal, Protocol


_KT_contra = TypeVar("_KT_contra", contravariant=True)
_VT = TypeVar("_VT")
_VT_co = TypeVar("_VT_co", covariant=True)


ComModeStr = Literal['sync', 'async', 'virtual', 'network']


class Array(Sized, Protocol[_KT_contra, _VT_co]):
    """
    A set of values (all the same type) indexed by keys
    (all the same type).
    """

    def __getitem__(self, __k: _KT_contra) -> _VT_co:
        ...


class MutableArray(
    Array[_KT_contra, _VT], Protocol[_KT_contra, _VT]
):
    """
    A set of values (all the same type) indexed by keys
    (all the same type) that allows setting items.
    """

    def __setitem__(self, __k: _KT_contra, __v: _VT) -> None:
        ...


if not TYPE_CHECKING:
    class Pointer:
        @classmethod
        def __class_getitem__(cls, item):

            # Don't try to resolve generic types at runtime.
            # They only matter for typing anyways.
            if isinstance(item, TypeVar):
                return None

            return ct.POINTER(item)

    CType = TypeVar('CType')
else:
    #: Generic type representing a C pointer
    Pointer = ct._Pointer

    #: Generic type representing a C data type (e.g. int, float, etc.)
    CType = TypeVar('CType', bound=ct._CData)

CBoolLike = Union[bool, int]

c_double_ptr = POINTER(c_double)
c_ubyte_ptr = POINTER(c_ubyte)
c_ushort_ptr = POINTER(c_ushort)
c_int_ptr = POINTER(c_int)
c_uint_ptr = POINTER(c_uint)


class SupportsPtr(Protocol):
    @property
    def ptr(self) -> Any:
        ...


class SupportsPtrs3(Protocol):
    @property
    def ptrs(self) -> Any:
        ...

#: Represents a tuple of integers, one for each DOF.
IntDOFTuple = Tuple[int, int, int, int, int, int, int, int]

#: Represents a tuple of floats, one for each DOF.
FloatDOFTuple = Tuple[float, float, float, float, float, float, float, float]
