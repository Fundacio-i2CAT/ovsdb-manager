import unittest

from ovsdbmanager import OvsdbManager
from ovsdbmanager.exception import OvsdbSyntaxError, OvsdbUnknownDatabase, \
    OvsdbResourceNotFoundException, OvsdbQueryException


class OvsdbManagerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.ovs = OvsdbManager()

    def test_get_table_raw_nonexistent(self):
        with self.assertRaises(OvsdbSyntaxError):
            self.ovs.get_table_raw("blablabla")

    def test_get_schema_nonexistent(self):
        with self.assertRaises(OvsdbUnknownDatabase):
            self.ovs.get_schema("blablabla")

    def test_get_bridge_invalid_name(self):
        with self.assertRaises(OvsdbResourceNotFoundException):
            self.ovs.get_bridge(name="blablabla")

    def test_get_bridge_invalid_uuid(self):
        with self.assertRaises(OvsdbSyntaxError):
            self.ovs.get_bridge(uuid=['uuid', 'blablabla'])

    def test_add_bridge_empty(self):
        with self.assertRaises(OvsdbSyntaxError):
            self.ovs.add_bridge("")

    def test_del_bridge_invalid_type(self):
        with self.assertRaises(OvsdbQueryException):
            self.ovs.del_bridge(1)

    def test_get_controller_invalid_uuid(self):
        with self.assertRaises(OvsdbSyntaxError):
            self.ovs.get_controller(uuid=['uuid', 'blablabla'])


if __name__ == '__main__':
    unittest.main()
