"""
Example script to dump several OVS database tables
"""
from ovsdbmanager import OvsdbManager

ovs = OvsdbManager()
# print(ovs.get_table_raw("Open_vSwitch"))
# print(ovs.get_table_raw("NetFlow"))
# print(ovs.get_table_raw("IPFIX"))
# print(ovs.get_table_raw("sFlow"))
#
br = ovs.get_bridge(name="test")
x = ovs.get_openvswitch()
x.add_external_key("zamora", "rocks")
br.add_external_key()
print(x.external_ids_dict)
# print(ovs.get_table_raw("Bridge"))
# print(ovs.get_table_raw("Controller"))
# print(ovs.get_table_raw("Port"))
