"""
Ovsdb Manager main class.

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
import socket
from logging import Logger
from typing import Dict, List

from ovsdbmanager import operation
from ovsdbmanager.condition import get_by_uuid, get_by_name
from ovsdbmanager.exception import OvsdbQueryException, OvsdbResourceNotFoundException, \
    OvsdbSyntaxError, OvsdbUnknownDatabase
from ovsdbmanager.query import OvsdbQuery
from ovsdbmanager.db.bridge import OvsBridge
from ovsdbmanager.db.controller import OvsController
from ovsdbmanager.db.interface import OvsInterface
from ovsdbmanager.db.ovs import OpenVSwitch
from ovsdbmanager.db.port import OvsPort
from ovsdbmanager.utils import generate_uuid, named_uuid

SYNTAX_ERROR = "syntax error"


class OvsdbManager:
    def __init__(self, ip: str = "127.0.0.1", port: int = 6640, db: str = "Open_vSwitch"):
        self.query = OvsdbQuery(ip, port, db)
        self.db = db
        self.logger = None
        try:
            self.query.echo_request()
        except socket.timeout:
            raise OvsdbQueryException("Connection timed out")

    def set_logger(self, logger: Logger):
        self.logger = logger

    def get_table_raw(self, table: str) -> Dict:
        result = self.query.select_from_table(table)["result"][0]
        if result.get("error") == SYNTAX_ERROR:
            raise OvsdbSyntaxError(result["details"])
        return result["rows"]

    def get_openvswitch(self) -> OpenVSwitch:
        return OpenVSwitch(self.get_table_raw("Open_vSwitch")[0], self)

    def list_dbs(self):
        return self.query.list_dbs()["result"]

    def get_schema(self, db: str):
        response = self.query.get_schema(db)
        error = response.get("error")
        if error and error["error"] == "unknown database":
            raise OvsdbUnknownDatabase(error["details"])
        return response["result"]

    def get_bridges(self):
        bridges_raw = self.query.select_from_table("Bridge")
        return [OvsBridge(bridge, self)
                for bridge in bridges_raw["result"][0]["rows"]]

    def get_bridge(self, name: str = None, uuid: List = None):
        conds = [get_by_uuid(uuid)] if uuid else [get_by_name(name)]

        result = self.query.select_from_table("Bridge", where=conds)["result"][0]
        error = result.get("error")
        if error and error == SYNTAX_ERROR:
            raise OvsdbSyntaxError(result["details"])
        bridge_raw = result["rows"]
        if not bridge_raw:
            bridge_id = name or uuid
            raise OvsdbResourceNotFoundException(f"Bridge {bridge_id} not found")
        return OvsBridge(bridge_raw[0], self)

    def add_bridge(self, name: str):
        if type(name) != str or name == "" or len(name) > 15:
            raise OvsdbSyntaxError("Please provide a valid bridge name. It must be a non-empty "
                                   "string of up to 15 characters")
        bridge_id, interface_id, port_id = [generate_uuid() for _ in range(3)]
        bridges = [bridge.uuid for bridge in self.get_bridges()] + [named_uuid(bridge_id)]
        ops = [
            operation.insert("Interface",
                             row={"name": name,
                                  "type": "internal"},
                             uuid_name=interface_id),
            operation.insert("Port",
                             row={"name": name,
                                  "interfaces": named_uuid(interface_id)},
                             uuid_name=port_id),
            operation.insert("Bridge",
                             row={"name": name,
                                  "ports": named_uuid(port_id)},
                             uuid_name=bridge_id),
            operation.update("Open_vSwitch",
                             where=[get_by_uuid(self.get_openvswitch().uuid)],
                             row={"bridges": ["set", bridges]}),
        ]
        bridge_raw = self.query.multiple_ops(ops)
        result = bridge_raw["result"]

        return self.get_bridge(uuid=result[2]["uuid"])

    def del_bridge(self, bridge: OvsBridge):
        if type(bridge) != OvsBridge:
            raise OvsdbQueryException("Please provide a bridge")
        other_bridges = [br.uuid for br in self.get_bridges() if br.uuid != bridge.uuid]
        self.query.update_table("Open_vSwitch",
                                row={"bridges": ["set", other_bridges]},
                                where=[get_by_uuid(self.get_openvswitch().uuid)])

    def del_bridges(self):
        self.query.update_table("Open_vSwitch",
                                row={"bridges": ["set", []]},
                                where=[get_by_uuid(self.get_openvswitch().uuid)])

    def get_controllers(self):
        controllers_raw = self.query.select_from_table("Controller")
        return [OvsController(controller, self) for controller in
                controllers_raw["result"][0]["rows"]]

    def get_controller(self, uuid: List):
        controller_raw = self.query.select_from_table("Controller",
                                                      where=[get_by_uuid(uuid)])
        result = controller_raw["result"][0]
        if result.get("error") == SYNTAX_ERROR:
            raise OvsdbSyntaxError(result["details"])
        return OvsController(result["rows"][0], self)

    def get_interface(self, uuid: List):
        interface_raw = self.query.select_from_table("Interface",
                                                     where=[get_by_uuid(uuid)])
        result = interface_raw["result"][0]
        if result.get("error") == SYNTAX_ERROR:
            raise OvsdbSyntaxError(result["details"])
        return OvsInterface(result["rows"][0], self)

    def get_port(self, uuid: List = None, name: str = None):
        conds = [get_by_uuid(uuid)] if uuid else [get_by_name(name)]
        port_raw = self.query.select_from_table("Port", where=conds)["result"][0]
        if port_raw.get("error") == SYNTAX_ERROR:
            raise OvsdbSyntaxError(port_raw["details"])
        if not port_raw["rows"]:
            port_id = name or uuid
            raise OvsdbResourceNotFoundException(f"Port {port_id} not found.")
        return OvsPort(port_raw["rows"][0], self)

