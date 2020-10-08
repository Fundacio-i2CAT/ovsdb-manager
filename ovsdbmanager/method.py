"""
Set of operations (methods) that can be done to an OVSDB database.
The functions in this file return the structure that has to be used to
make the corresponding request.

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

from typing import Dict, List

from ovsdbmanager.utils import generate_uuid


def list_dbs() -> Dict:
    """
    Builds the request payload to list the databases
    :return: the request payload
    """
    return {
        "method": "list_dbs",
        "params": [],
        "id": generate_uuid()
    }


def get_schema(db: str) -> Dict:
    """
    Builds the request payload to get the schema of a particular
    database
    :param db: the database
    :return: the request payload
    """
    return {
        "method": "get_schema",
        "params": [db],
        "id": generate_uuid()
    }


def transact(db: str, operations: List) -> Dict:
    """
    Builds the request payload for doing transactions with the database
    (create, read, update, delete)
    :param db: the database
    :param operations: the set of operations to be perfomed
    :return: the request payload
    """
    return {
        "method": "transact",
        "params": [db, *operations],
        "id": generate_uuid()
    }


def echo(params: List = None, query_id: str = None) -> Dict:
    """
    Builds the response payload to reply to an echo request. This is a
    control message between the client and the server
    :param params: the set of params sent in the echo request
    :param query_id: the id sent in the echo request
    :return: the response payload
    """
    return {
        "method": "echo",
        "params": params or ["1", "2", "3"],
        "id": query_id or generate_uuid()
    }
