# Konfigurasi Mikrotik Hotspot Server
# by MbingSDK
# Leave me here...

from librouteros import connect

class autoHotspot:
    def __init__(self, user, password, ipModem, port, ipClient, ipRemote, ipHotspot, ipDNS, domain):
        self.user = user
        self.password = password
        self.ipModem = ipModem
        self.ipClient = ipClient
        self.port = port
        self.ipRemote = ipRemote
        self.ipHotspot = ipHotspot
        self.ipDNS = ipDNS
        self.domain = domain
        self.ether = []
        self.etherLenght = 0
        self.api = None
        self.bridge = "hotspot"
        self.defaultUsername = "admin"
        self.defaultPassword = "mbingsdk"

    def auth(self):
        try:
            self.api = connect(username = self.user, password = self.password, host = self.ipModem, port = self.port)
            return self.api
        except Exception as asu:
            print(asu)
            exit()

    def checkEther(self):
        ethernet = self.api.path('interface')
        a = tuple(ethernet)
        for i in a:
            self.ether.append(i['name'])

    def addBridge(self):
        br = self.api.path('interface', 'bridge')
        tuple(br)
        br.add(name = self.bridge)

    def extendPort(self):
        brport = self.api.path('interface', 'bridge', 'port')
        tuple(brport)
        for i in range(len(self.ether)):
            if i not in [0,1]:
                brport.add(
                    interface = self.ether[i],
                    bridge = self.bridge
                )

    def ipSetting(self):
        ipnya = self.api.path('ip', 'address')
        tuple(ipnya)
        ipnya.add(
            address = self.ipClient,
            network = self.ipClient.replace(self.ipClient.split(".")[3], "0"),
            interface = self.ether[0]
        )
        ipnya.add(
            address = self.ipHotspot,
            network = self.ipHotspot.replace(self.ipHotspot.split(".")[3], "0"),
            interface = self.bridge
        )

    def defaultRoute(self):
        rout = self.api.path('ip', 'route')
        tuple(rout)
        rout.add(
            gateway = self.ipClient.replace(self.ipClient.split(".")[3], "1")
        )

    def dnsSetting(self):
        dns = self.api.path('ip','dns')
        tuple(dns)
        dns.update(**{
            'servers':self.ipDNS,
            'allow-remote-requests':True
        })

    def ipPool(self):
        pool = self.api.path('ip','pool')
        tuple(pool)
        pool.add(
            name = "Remote",
            ranges = self.ipRemote.replace(self.ipRemote.split(".")[3], "2")+"-"+self.ipRemote.replace(self.ipRemote.split(".")[3], "254")
        )
        pool.add(
            name = "Hotspot",
            ranges = self.ipHotspot.replace(self.ipHotspot.split(".")[3], "2")+"-"+self.ipHotspot.replace(self.ipHotspot.split(".")[3], "254")
        )

    def dhcpServer(self):
        dhcp = self.api.path('ip','dhcp-server')
        tuple(dhcp)
        dhcpID = dhcp.add(
            name="Dhcp-Hotspot",
            interface=self.bridge
        )
        dhcp.update(**{
            '.id':dhcpID,
            'lease-time':'1d',
            'address-pool':'Hotspot',
            'add-arp':True,
            'disabled':False
        })
        dhcpNetwork = self.api.path('ip','dhcp-server','network')
        tuple(dhcpNetwork)
        dhcpNetwork.add(
            address = self.ipHotspot.replace(self.ipHotspot.split(".")[3], "0/24"),
            gateway = self.ipHotspot.replace(self.ipHotspot.split(".")[3], "1")
        )

    def natFirewall(self):
        nat = self.api.path('ip','firewall','nat')
        n1 = nat.add(
            chain = "srcnat"
        )
        nat.update(**{
            '.id':n1,
            'action':'masquerade',
            'src-address':self.ipHotspot.replace(self.ipHotspot.split(".")[3], "0/24"),
            'comment':'masquerade hotspot network'
        })
        n2 = nat.add(
            chain = "srcnat",
            action = "masquerade"
        )
        nat.update(**{
            '.id':n2,
            'out-interface':self.ether[0]
        })

    def mangleFirewall(self):
        mangle = self.api.path('ip','firewall','mangle')
        tuple(mangle)
        m1 = mangle.add(
            chain = 'postrouting'
        )
        mangle.update(**{
            '.id':m1,
            'action':'change-ttl',
            'new-ttl':'set:1',
            'passthrough':False,
            'out-interface':self.bridge
        })

    def hotspotProfile(self):
        hsProfile = self.api.path('ip','hotspot','profile')
        tuple(hsProfile)
        hspf = hsProfile.add(
            name = "hsprof1"
        )
        hsProfile.update(**{
            '.id':hspf,
            'hotspot-address':self.ipHotspot.split("/")[0],
            'dns-name':self.domain,
            'html-directory':'flash/hotspot',
            'login-by':'http-chap,https,http-pap,trial,mac-cookie',
            'https-redirect':True,
            'trial-uptime-limit':'1m',
            'trial-uptime-reset':'1d'
        })

    def hotspotServer(self):
        hsServer = self.api.path('ip','hotspot')
        tuple(hsServer)
        hss = hsServer.add(
            name = "hotspotVx6",
            interface = self.bridge,
            profile = "hsprof1"
        )
        hsServer.update(**{
            '.id':hss,
            'address-pool':'Hotspot',
            'idle-timeout':'5m',
            'disabled':False
        })

    def hotspotDefautlUsers(self):
        users = self.api.path('ip','hotspot','user')
        tuple(users)
        users.add(
            name = self.defaultUsername,
            password = self.defaultPassword
        )

        dhcpID = dhcp.add(
            name = "Dhcp-Remote",
            interface = self.ether[1]
        )
        dhcp.update(**{
            '.id':dhcpID,
            'lease-time':'1d',
            'address-pool':'Remote',
            'add-arp':True,
            'disabled':False
        })

    def hotspotDhcpServer(self):
        dhcpNetwork = self.api.path('ip','dhcp-server','network')
        dhcpNetwork.add(
            address = ipRemote.replace(ipRemote.split(".")[3], "0/24"),
            gateway = ipRemote.replace(ipRemote.split(".")[3], "1")
        )
        
    def run(self):
        pa = input("Masukkan kode: ")
        if str(pa) == "mbing":
            self.auth()
            self.checkEther()
            self.addBridge()
            self.extendPort()
            self.ipSetting()
            self.defaultRoute()
            self.dnsSetting()
            self.ipPool()
            self.dhcpServer()
            self.natFirewall()
            self.mangleFirewall()
            self.hotspotProfile()
            self.hotspotServer()
            self.hotspotDefautlUsers()
            self.hotspotDhcpServer()
            print("\n\nHotspot Berhasil Dibuat,...! :v\n\nUser Default : admin\nPassword: mbingsdk\n\n")
            time.sleep(3)
        else:
            print("\n\nFailed,...! :v\n\n")
