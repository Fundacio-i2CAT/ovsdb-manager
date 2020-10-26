# Ovsdb Manager
OvSDB Manager is an OpenVSwitch Database Protocol (OVSDB) Python Client 
developed by the [i2CAT Foundation](https://www.i2cat.net/) (Barcelona). 
It implements the basic functionalities to interact with OpenVSwitch switches (addport, delete port
 , add bridge, delete bridge, etc).
 
 Author: Ferran Cañellas <ferran.canellas@i2cat.net>
 
## Requirements
* Python 3.5 or greater

## Installation
If you are using PiP:
```
pip install ovsdbmanager
```
Otherwise, you can clone this repo and install the module manually.
```
git clone https://github.com/Fundacio-i2CAT/ovsdb-manager.git
cd ovsdb-manager
python3 setup.py install
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
from ovsdbmanager.db.bridge import FailMode
from ovsdbmanager.db.controller import ConnectionMode

ovs = OvsdbManager(ip="X.X.X.X", port="Y")

# Create a bridge
br1 = ovs.add_bridge("br1")

# Add a port
p1 = br1.add_port("p1")

# Delete a port
br1.del_port(p1)

# Set controller
ctrl = br1.set_controller("tcp:10.0.10.1:6653")

# Set controller's connection mode as out of band
ctrl.set_connection_mode(ConnectionMode.OUTOFBAND)

# Set fail mode as secure
br1.set_fail_mode(FailMode.SECURE)

# Enable RSTP
br1.set_rstp(True)

# Add a patch port
br1.add_port("p2", patch_peer="p3")

# Delete a bridge
ovs.del_bridge(br1)
```