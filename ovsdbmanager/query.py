"""
OvsdbQuery - Class responsible for sending the queries

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

import json
import socket
from datetime import datetime, timedelta
from typing import Dict

from ovsdbmanager import method, operation, exception

TIMEOUT = 5
BUFSIZE = 1024


class OvsdbQuery:
    """
    Contains the set of queries that can be made to an OVSDB server
    """

    def __init__(self, ip: str, port: int, db):
        self.db = db
        self.ip = ip
        self.port = port

    def echo_request(self) -> Dict:
        return self._send(method.echo())

    def echo_reply(self, params, query_id):
        """
        Sends an echo reply message
        :param params: the params sent by the echo request
        :param query_id: the id sent by the echo request
        :return: the response to the message
        """
        return self._send(method.echo(params, query_id))

    def list_dbs(self) -> Dict:
        return self._send(method.list_dbs())

    def get_schema(self, db) -> Dict:
        return self._send(method.get_schema(db))

    def select_from_table(self, table_name, where=None) -> Dict:
        body = method.transact(self.db, [operation.select(table_name, where)])
        return _check_response(self._send(body))

    def update_table(self, table_name, row, where=None) -> Dict:
        body = method.transact(self.db, [operation.update(table_name, row, where)])
        return _check_response(self._send(body))

    def multiple_ops(self, ops) -> Dict:
        return _check_response(self._send(method.transact(self.db, ops)), len(ops))

    def _send(self, query: Dict):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5.)
        s.connect((self.ip, self.port))
        s.send(json.dumps(query).encode())

        buf = bytes()
        bufsize = BUFSIZE

        timeout = datetime.now() + timedelta(seconds=TIMEOUT)

        while datetime.now() < timeout:
            buf += s.recv(bufsize)
            try:
                query_response = json.loads(buf.decode())

                if "method" in query_response.keys() and query_response["method"] == "echo":
                    echo_reply = self.echo_reply(query_response["params"],
                                                 query_response["id"])
                    s.send(json.loads(echo_reply).encode())
                    buf = bytes()
                else:
                    s.close()
                    return query_response

            except json.JSONDecodeError:
                pass
        raise TimeoutError("Connection timed out")


def _check_response(response: Dict, num_ops: int = 1) -> Dict:
    if len(response["result"]) == num_ops:
        return response

    result_error = response["result"][num_ops]
    error_type = result_error["error"]
    error_details = result_error["details"]
    if error_type == "referential integrity violation":
        raise exception.OvsdbReferentialIntegrityViolation(error_details)
    if error_type == "constraint violation":
        raise exception.OvsdbConstraintViolation(error_details)
    if error_type == "resources exhausted":
        raise exception.OvsdbResourcesExhausted(error_details)
    if error_type == "I/O error":
        raise exception.OvsdbIOError(error_details)
    raise exception.OvsdbCommitException(error_details)
