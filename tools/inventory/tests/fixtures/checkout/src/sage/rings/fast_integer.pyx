r"""
Fast integers

A small module with the shapes that Sage's Cython sources have.
"""

from sage.libs.gmp.mpz cimport *
from cypari2.gen cimport Gen
cimport sage.structure.element


cdef inline int c_only(int a) noexcept:
    return a


cdef class FastInteger(sage.structure.element.EuclideanDomainElement):
    r"""
    An integer.

    EXAMPLES::

        sage: FastInteger(3)
        3
    """

    def xgcd(self, FastInteger n):
        r"""
        Return the extended greatest common divisor.

        EXAMPLES::

            sage: FastInteger(4).xgcd(FastInteger(6))
            (2, -1, 1)
            sage: FastInteger(5).xgcd(FastInteger(7))
            (1, 3, -2)
        """
        return None

    cpdef _add_(self, other):
        return self

    cpdef FastInteger double(self):
        return self

    cdef int _hidden(self) except -1:
        return 0


cpdef int fast_valuation(int a, int p) noexcept:
    return 0


def gcd_list(values):
    return values
