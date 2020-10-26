"""
OvsBridge class.

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
from enum import Enum
from typing import List

from ovsdbmanager import operation
from ovsdbmanager.exception import OvsdbResourceNotFoundException, OvsdbQueryException
from ovsdbmanager.utils import generate_uuid, named_uuid
from ovsdbmanager.condition import get_by_uuid
from ovsdbmanager.db.ovs import OpenVSwitch
from ovsdbmanager.db.port import OvsPort
from ovsdbmanager.db.controller import OvsController


class FailMode(Enum):
    STANDALONE = "standalone"
    SECURE = "secure"


class OvsBridge(OpenVSwitch):
    """
    Class that represents an OvS bridge. Currently it implements the
    basic operations that can be done to it.
    """

    def _update_bridge_object(self):
        self.__dict__ = self.api.get_bridge(uuid=self.uuid).__dict__

    def set_stp(self, enabled: bool):
        """
        Sets the STP parameter of the bridge.
        :param enabled: boolean that represents the stp state.
        :return:
        """
        self.api.query.update_table("Bridge",
                                    row={"stp_enable": enabled},
                                    where=[get_by_uuid(self.uuid)])
        self._update_bridge_object()

    def set_rstp(self, enabled: bool):
        """
        Sets the RSTP parameter of the bridge.
        :param enabled: boolean that represents the rstp state.
        :return:
        """
        self.api.query.update_table("Bridge",
                                    row={"rstp_enable": enabled},
                                    where=[get_by_uuid(self.uuid)])
        self._update_bridge_object()

    def set_fail_mode(self, mode: FailMode):
        """
        Sets the fail mode of the bridge
        :param mode: the mode
        :return:
        """
        self.api.query.update_table("Bridge",
                                    row={"fail_mode": mode.value},
                                    where=[get_by_uuid(self.uuid)])
        self._update_bridge_object()

    def get_controller(self) -> OvsController:
        """
        Gets the controller of the bridge
        :return: OvsController
        """
        return self.api.get_controller(getattr(self, "controller"))

    def set_controller(self, target: str) -> OvsController:
        """
        Sets the controller of the bridge
        :param target: address where the controller is
        (e.g. tcp:HOST:PORT)
        :return:OvsController
        """
        controller_id = generate_uuid()
        ops = [
            operation.insert("Controller",
                             row={"role": "other", "target": target},
                             uuid_name=controller_id),
            operation.update("Bridge",
                             where=[get_by_uuid(self.uuid)],
                             row={"controller": ["set", [named_uuid(controller_id)]]})
        ]
        self.api.query.multiple_ops(ops)
        self._update_bridge_object()
        return self.get_controller()

    def set_protocols(self, protocols: List):
        """
        Sets the supported protocols of the bridge
        :param protocols: list of supported protocols
        :return:
        """
        self.api.query.update_table("Bridge",
                                    where=[get_by_uuid(self.uuid)],
                                    row={"protocols": ["set", protocols]})
        self._update_bridge_object()

    def get_port(self, name) -> OvsPort:
        """
        Gets a port of the bridge by name
        :param name: name of the port
        :return: OvsPort
        """
        for port in self.get_ports():
            if getattr(port, "name") == name:
                return port
        raise OvsdbResourceNotFoundException("Port '{}' not found".format(name))

    def get_ports(self) -> List[OvsPort]:
        """
        Gets the whole list of ports of the bridge
        :return: List[OvsPort]
        """
        self._update_bridge_object()
        ports_raw = getattr(self, "ports")
        ports = []
        if ports_raw[0] == 'set':
            for port_uuid in ports_raw[1]:
                port = self.api.get_port(uuid=port_uuid)
                ports.append(port)
        elif ports_raw[0] == "uuid":
            port = self.api.get_port(uuid=ports_raw)
            ports.append(port)
        return ports

    def add_port(self, port: str, patch_peer: str = None):
        """
        Adds a port to the bridge
        :param port: name of the interface to attach
        :param patch_peer: if the port connects with another bridge,
        name of the patch port of the other bridge.
        :return: query response
        """
        port_id, interface_id = [generate_uuid() for _ in range(2)]
        all_ports_uuid = [p.uuid for p in self.get_ports()] + [named_uuid(port_id)]
        interface = {"name": port}
        if patch_peer:
            interface["type"] = "patch"
            interface["options"] = ["map", [["peer", patch_peer]]]
        ops = [
            operation.insert("Interface",
                             row=interface,
                             uuid_name=interface_id),
            operation.insert("Port",
                             row={"name": port,
                                  "interfaces": named_uuid(interface_id)},
                             uuid_name=port_id),
            operation.update("Bridge",
                             where=[get_by_uuid(self.uuid)],
                             row={"ports": ["set", all_ports_uuid]})
        ]
        response = self.api.query.multiple_ops(ops)
        self._update_bridge_object()
        return response

    def del_port(self, port: OvsPort):
        """
        Deletes a port
        :param port: the port to delete
        :return:
        """
        if not port:
            raise OvsdbQueryException("Please provide a port")
        new_ports = [p.uuid for p in self.get_ports() if p.uuid != port.uuid]
        self.api.query.update_table("Bridge",
                                    row={"ports": ["set", new_ports]},
                                    where=[get_by_uuid(self.uuid)])
        self._update_bridge_object()

    def del_ports(self):
        """
        Deletes all ports of a bridge
        :return:
        """
        local_port = [p.uuid for p in self.get_ports()
                      if getattr(p, "name") == getattr(self, "name")]
        self.api.query.update_table("Bridge",
                                    row={"ports": ["set", local_port]},
                                    where=[get_by_uuid(self.uuid)])
        self._update_bridge_object()

