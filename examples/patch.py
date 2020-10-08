"""
Example script that creates two bridges, builds a patch between them and
deletes all bridges
"""
from ovsdbmanager import OvsdbManager

ovs = OvsdbManager()
br1 = ovs.add_bridge("br1")
br2 = ovs.add_bridge("br2")
br1.add_port("p1", "p2")
br2.add_port("p2", "p1")
br1.del_ports()
ovs.del_bridges()
