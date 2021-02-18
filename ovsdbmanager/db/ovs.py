"""
OpenVSwitch class - base class for all the db.

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

from ovsdbmanager.utils import parse_map, add_to_map


class OpenVSwitch:
    def __init__(self, data, api):
        self.__dict__ = data
        self.api = api

    def __str__(self):
        tmp_json = self.__dict__.copy()
        try:
            del tmp_json["api"]
        except KeyError:
            pass
        return json.dumps(tmp_json)

    @property
    def uuid(self):
        return getattr(self, "_uuid")

    @property
    def external_ids_dict(self):
        external_ids = getattr(self, "external_ids")
        if external_ids:
            return parse_map(external_ids[1])
        return None

    def add_external_key(self, key, value):
        external_ids = getattr(self, "external_ids")
        if not external_ids:
            raise AttributeError("There is no such 'external_ids' attribute")
        add_to_map(external_ids, key, value)

