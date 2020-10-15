# Ovsdb Manager
Ovsdb Manager is an OVSDB Python Client developed by the [i2CAT Foundation](https://www.i2cat.net/
) (Barcelona). It implements the basic functionalities to interact with OpenVSwitch switches (add
 port, delete port
 , add bridge, delete bridge, etc).
 
 Author: Ferran Cañellas <ferran.canellas@i2cat.net>
 
## Requirements
* Python 3.5 or grater

## Installation
```
pip install ovsdbmanager
```

## Usage
To start using Ovsdb Manager simply do
```python
from ovsdbmanager import OvsdbManager
ovs = OvsdbManager(ip="X.X.X.X", port="Y")
```
If you are running the OVSDB server locally you can ommit the IP address. The default port is 6640.

Examples of use:

```python
from ovsdbmanager import OvsdbManager
ovs = OvsdbManager(ip="X.X.X.X", port="Y")

# Create a bridge
br1 = ovs.add_bridge("br1")

# Add a port
p1 = br1.add_port("p1")

# Delete a port
br1.del_port(p1)

# Set controller
br1.set_controller("tcp:10.0.10.1:6653")

# Set fail mode as secure
br1.set_fail_mode("secure")

# Enable RSTP
br1.set_rstp(True)

# Add a patch port
br1.add_port("p2", patch_peer="p3")

# Delete a bridge
ovs.del_bridge(br1)
```