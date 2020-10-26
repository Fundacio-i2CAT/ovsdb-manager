"""
Helper class used for obtaining "condition" structures.
They are described in RFC 7047 as follows:

A 3-element JSON array of the form [<column>, <function>, <value>]
that represents a test on a column value.  Except as otherwise
specified below, <value> MUST have the same type as <column>.

     Copyright (C) 2020  Fundació Privada I2CAT, Internet i Innovació digital a Catalunya

     This program is free software: you can redistribute it and/or modify
     it under the terms of the GNU Affero General Public License as published by
     the Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.

     This program is distributed in the hope that it will be useful,
     but WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
     GNU Affero General Public License for more details.

     You should have received a copy of the GNU Affero General Public License
     along with this program.  If not, see <https://www.gnu.org/licenses/>.

     Authors: Ferran Cañellas <ferran.canellas@i2cat.net>
"""

from typing import List


def get_by_uuid(uuid: List) -> List[str]:
    """
    Builds a condition to match the uuid passed as parameter.

    :param uuid: the uuid of the element to be obtained
    :return: the condition to match
    """
    return _build_condition("_uuid", "==", uuid)


def get_by_name(name: str) -> List[str]:
    """
    Builds a condition to match the name passed as parameter.

    :param name: the name of the element to be obtained
    :return: the condition to match
    """
    return _build_condition("name", "==", name)


def _build_condition(column, function: str, value) -> List[str]:
    common_functions = ["==", "!=", "includes", "excludes"]
    other_functions = ["<", "<=", ">=", ">"]

    if function not in common_functions + other_functions:
        raise TypeError("Unsupported function")

    if not isinstance(value, (int, float)) and function in other_functions:
        raise TypeError("Invalid function for value type {}".format(type(value).__name__))

    return [column, function, value]
