"""
OvsController class.

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

from ovsdbmanager.db.ovs import OpenVSwitch
from ovsdbmanager.condition import get_by_uuid


class ConnectionMode(Enum):
    OUTOFBAND = "out-of-band"
    INBAND = "in-band"


class OvsController(OpenVSwitch):
    """
    Class that represents an OvS controller.
    """
    def _update_controller_object(self):
        self.__dict__ = self.api.get_controller(uuid=self.uuid).__dict__

    def set_connection_mode(self, mode: ConnectionMode):
        """
        Sets the connection mode to the controller
        :param mode: the mode
        :return:
        """
        self.api.query.update_table("Controller",
                                    row={"connection_mode": mode.value},
                                    where=[get_by_uuid(self.uuid)])
        self._update_controller_object()



