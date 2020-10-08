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
from typing import Dict

from ovsdbmanager import operation
from ovsdbmanager.condition import get_by_uuid, get_by_name
from ovsdbmanager.exception import OvsdbQueryException, OvsdbResourceNotFoundException
from ovsdbmanager.query import OvsdbQuery
from ovsdbmanager.tables.bridge import OvsBridge
from ovsdbmanager.tables.controller import OvsController
from ovsdbmanager.tables.interface import OvsInterface
from ovsdbmanager.tables.ovs import OpenVSwitch
from ovsdbmanager.tables.port import OvsPort
from ovsdbmanager.utils import generate_uuid, named_uuid


class OvsdbManager:
    def __init__(self, ip: str = "127.0.0.1", port: int = 6640, db: str = "Open_vSwitch"):
        self.query = OvsdbQuery(ip, port, db)
        self.db = db
        try:
            self.query.echo_request()
        except socket.timeout:
            raise OvsdbQueryException("Connection timed out")

    def get_table_raw(self, table: str) -> Dict:
        return self.query.select_from_table(table)["result"][0]["rows"]

    def get_openvswitch(self) -> OpenVSwitch:
        return OpenVSwitch(self.get_table_raw("Open_vSwitch")[0], self)

    def list_dbs(self):
        return self.query.list_dbs()["result"]

    def get_schema(self, db: str):
        return self.query.get_schema(db)["result"]

    def get_bridges(self):
        bridges_raw = self.query.select_from_table("Bridge")
        return [OvsBridge(bridge, self)
                for bridge in bridges_raw["result"][0]["rows"]]

    def get_bridge(self, name: str = None, uuid: str = None):
        conds = [get_by_uuid(uuid)] if uuid else [get_by_name(name)]

        bridge_raw = self.query.select_from_table("Bridge", where=conds)["result"][0]["rows"]
        if not bridge_raw:
            raise OvsdbResourceNotFoundException
        return OvsBridge(bridge_raw[0], self)

    def add_bridge(self, name: str):
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

        return self.get_bridge(uuid=bridge_raw["result"][2]["uuid"])

    def del_bridge(self, bridge: OvsBridge):
        if not bridge:
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

    def get_controller(self, uuid: str):
        controller_raw = self.query.select_from_table("Controller",
                                                      where=[get_by_uuid(uuid)])
        return OvsController(controller_raw["result"][0]["rows"][0], self)

    def get_interface(self, uuid: str):
        interface_raw = self.query.select_from_table("Interface",
                                                     where=[get_by_uuid(uuid)])
        return OvsInterface(interface_raw["result"][0]["rows"][0], self)

    def get_port(self, uuid: str = None, name: str = None):
        conds = [get_by_uuid(uuid)] if uuid else [get_by_name(name)]
        port_raw = self.query.select_from_table("Port", where=conds)
        return OvsPort(port_raw["result"][0]["rows"][0], self)
