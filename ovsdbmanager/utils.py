"""
Helper module for handling UUIDs

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

from typing import List, Dict
from uuid import uuid4


def generate_uuid() -> str:
    """
    Generates a temporary UUID for a given transaction.
    :return:
    """
    return "id" + str(uuid4()).replace("-", "_")


def named_uuid(uuid: str) -> List:
    """
    Converts a uuid into a named-uuid
    :param uuid: the uuid
    :return: The named-uuid list
    """
    return ["named-uuid", uuid]


def parse_map(map_: List) -> Dict:
    return {elem[0]: elem[1] for elem in map_}


def add_to_map(map_: List, key: str, value: str) -> List:
    return map_[1].append([key, value])
