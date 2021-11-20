from hotspot.autoConfiguration import *

# Connection
a = autoHotspot("admin", "admin", "192.168.1.1", "8728", "192.168.1.3/24", "192.168.10.1/24", "192.168.11.1/24", "8.8.8.8,8.8.4.4", "vx6-ct.net")

# Simple Mikrotik Hotspot Automatic Configuration
a.run()
