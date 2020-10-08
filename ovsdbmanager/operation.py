"""
Set of operations that can be done in a transact method.
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


def insert(table: str, row: Dict, uuid_name: str = "") -> Dict:
    """
    Builds an insert operation (create)
    :param table: table where the new element
    :param row: data of the new element to be inserted
    :param uuid_name: the uuid of the element. If not present, a random
    one is assigned
    :return: The operation payload
    """
    insert_dict = {
        "op": "insert",
        "table": table,
        "row": row
    }
    if uuid_name:
        insert_dict["uuid-name"] = uuid_name
    return insert_dict


def select(table: str, where: List = None, columns: List = None) -> Dict:
    """
    Builds a select operation (get)
    :param table: The table were the element(s) are
    :param where: The condition to filter the database. To obtain a
    specific element, its uuid is typically used. If not present all the
    elements of the table are returned
    :param columns: The specific fields that have to be retrieved. If not
    present all are returned.
    :return: The operation table
    """
    if where is None:
        where = []
    select_dict = {
        "op": "select",
        "table": table,
        "where": where
    }
    if columns:
        select_dict["columns"] = columns
    return select_dict


def update(table: str, row: Dict, where: List = None) -> Dict:
    """
    Builds an update operation (update)
    :param table: The table where the element(s) are
    :param row: the new data to be put
    :param where: the conditions to filter the table. If not present,
    all the elements of the database will be updated with 'row'.
    :return: the operation payload
    """
    if where is None:
        where = []
    return {
        "op": "update",
        "table": table,
        "where": where,
        "row": row
    }


def delete(table: str, where: List = None) -> Dict:
    """
    Builds a delete operation (delete)
    :param table: The table where the element(s) to delete are
    :param where: The condition to filter the table
    :return: the operation payload
    """
    if where is None:
        where = []
    return {
        "op": "delete",
        "table": table,
        "where": where
    }
