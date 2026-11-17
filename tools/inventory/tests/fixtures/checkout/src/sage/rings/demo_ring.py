r"""
Demonstration rings

A small module with the shapes that Sage's Python sources have.
"""

import numpy

from sage.interfaces.gap import gap
from sage.libs.pari import pari
from sage.misc.lazy_import import lazy_import
from sage.rings import unlisted
from sage.structure.parent import Parent

from .fast_integer import (
    FastInteger,
    gcd_list,
)

lazy_import("sage.version", ["version"], deprecation=1)


class DemoRing(Parent, UniqueRepresentation):
    r"""
    The ring of integers modulo `n`.

    EXAMPLES::

        sage: R = DemoRing(3)
        sage: R.order()
        3
    """

    def order(self):
        r"""
        Return the number of elements.

        ALGORITHM:

        Counting, see [Coh1993]_ and [BCP1997]_.

        EXAMPLES::

            sage: DemoRing(5).order()  # optional - database_gap
            5
        """
        return self._n

    def _repr_(self):
        return "Demonstration ring"

    class Element(RingElement):
        def inverse(self):
            def helper(value):
                return value

            return helper(self)


@overload
def demo_gcd(a: int, b: int) -> int: ...
@overload
def demo_gcd(a: list, b: None = None) -> int: ...
def demo_gcd(a, b):
    r"""
    Return the greatest common divisor.

    EXAMPLES::

        sage: demo_gcd(4, 6)  # needs sage.libs.pari
        2
    """
    return pari(a).gcd(b)


def _private(a):
    return gap(a), numpy.array(a)
