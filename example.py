from hotspot.autoConfiguration import *

# Data
username = "admin"
password = "admin"
ipGatewayRemote = "10.10.10.1"
ports = "8728"
ipClientModem = "192.168.1.3/24"
ipRemote = ipGatewayRemote+"/24"
ipHotspot = "20.20.20.1/24"
ipDNS = "8.8.8.8,8.8.4.4"
domain = "vx6ct.net"

# Connection
a = autoHotspot(username, password, ipGatewayRemote, ports, ipClientModem, ipRemote, ipHotspot, ipDNS, domain)

# Simple Mikrotik Hotspot Automatic Configuration
a.run()
