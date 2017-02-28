# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event, event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet, arp, ipv4, icmp, tcp
from ryu.lib.packet import ether_types
import pymysql
from ryu.app import my_ovs_db
import re #Import Regex

class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.initialised=False
        self.newPC = {}
        self.trustedPC = {}
        self.Intercept = False
        self.mydb = my_ovs_db.Ovsdb() # create a new instance of ovsdb class
        self.mydb.clear_Q_ZONE_TABLE()

        
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
#Add flow route non-compliance PC to this controller
    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        # The following has been commented out to stop add_flow
        # then the switch is totally not working
        datapath.send_msg(mod)
#Delete flow        
    def del_flow(self, datapath,src,table_id=0):
        #Delete a flow base on the src mac addr
        print "Datapath id is :", datapath.id 
        ofp = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch(eth_src=src)
        instructions = []
        #creating a request, req, of deleting a particular flow
        req = datapath.ofproto_parser.OFPFlowMod(datapath, 0, 0, table_id,ofp.OFPFC_DELETE,0,0,1,ofp.OFPCML_NO_BUFFER,ofp.OFPP_ANY,ofp.OFPG_ANY,0, match,instructions)
        print "Deleting flow ",src
        datapath.send_msg(req)

    def getIPHost(self,ip_src):
        # extract the Host ID from the ip_src
        # return 0 if the ip_src does not match with the S1 segment
        # return -1 if ip_src is an invalid ip address
        if ip_src == '0.0.0.0':
            return -1
        mm = re.match(r"^169.*",ip_src) 
        if mm:
            # src is invalid, still waiting for DHCPD assignment
            return -1      
        mm = re.match(r"192\.168\.163\.(\d{1,3})",ip_src)
        if mm:
            if mm.group(1):
                return int(mm.group(1))
        return 0

    def handleNewPC(self,in_port,dpid,pkt,datapath,parser,data):
        retval = False #assume no need to block
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        dst = eth.dst
        src = eth.src
        self.logger.info("Packets in dpID: %s, SRC_MAC: %s, DST_MAC: %s, IN_PORT: %s", dpid, src, dst, in_port)
        #The following protocols can be used for debugging
        arp_pkt = pkt.get_protocol(arp.arp)
        ipv4_pkt = pkt.get_protocol(ipv4.ipv4)
        icmp_pkt = pkt.get_protocol(icmp.icmp)
        tcp_pkt = pkt.get_protocol(tcp.tcp)
        if arp_pkt:
            #self.logger.info("Yes, ARP attempt detected")
            pass
        if ipv4_pkt:
            #self.logger.info("IPv4 attempt detected - dst : %s",ipv4_pkt.dst)
            #print "Source IP is found", ipv4_pkt.src
            hostID = self.getIPHost(ipv4_pkt.src)
            if hostID >=0: 
                if hostID < 170:
                    self.trustedPC[src] = ipv4_pkt.src
                    self.mydb.setTrustPC(src,ipv4_pkt.src)
                    self.del_flow(datapath,src,0)
                else:
                    if self.newPC[src] != ipv4_pkt.src:
                        self.newPC[src]= ipv4_pkt.src
                        self.mydb.updateNewPC(src,ipv4_pkt.src)
        if icmp_pkt:
            #self.logger.info("Yes, ICMP attempt detected")
            retval=False
        if tcp_pkt:
            #self.logger.info("Yes, TCP attempt detected %s",ipv4_pkt.dst)
            self.logger.info("TCP attempt detected - SRC_IP: %s, DST_IP: %s",ipv4_pkt.src,ipv4_pkt.dst)
            
            if not src in self.trustedPC:
                if not ipv4_pkt.dst in ['192.168.163.130', '192.168.163.150']: #IP of S2(HostOnly) IP of h1
    
                    retval=True
            #retval = False
            return retval

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug("packet truncated: only %s of %s bytes",
                              ev.msg.msg_len, ev.msg.total_len)
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src
        ipv4_pkt = pkt.get_protocol(ipv4.ipv4)

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})
        #self.logger.info("packet in %s %s %s %s", dpid, src, dst, in_port) 

        if dpid == 10: # dpid = 10, SW2 dpid is 10
            if not (src in self.newPC):
                self.newPC[src] = '1' 
                if  self.mydb.isUnknownPC(src):
                    self.mydb.insertNewPC(src,in_port)
                    # insert a priority 2 flow to capture all packet
                    # from this src. 
                    match = parser.OFPMatch(in_port=in_port, eth_src=src)
                    actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                        ofproto.OFPCML_NO_BUFFER)]
                    self.add_flow(datapath, 2, match, actions)
            if not (src in self.trustedPC):
                if self.mydb.isTrustedPC(src) == False:
                    print "Checking ",src
                    print ""
                    blocked = self.handleNewPC(in_port,dpid,pkt,datapath,parser,msg.data)
                    if blocked:
                        # drop the packet
                        return

        # learn a mac address to avoid FLOOD next time.
        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # install a flow to avoid packet_in next time
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
            # verify if we have a valid buffer_id, if yes avoid to send both
            # flow_mod & packet_out
            if msg.buffer_id != ofproto.OFP_NO_BUFFER:
                self.add_flow(datapath, 1, match, actions, msg.buffer_id)
                return
            else:# will try to change this datapath to my own switches
                pass
                self.add_flow(datapath, 1, match, actions)
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                  in_port=in_port, actions=actions, data=data)
        datapath.send_msg(out)

