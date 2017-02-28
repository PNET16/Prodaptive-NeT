
import pymysql
import imp
my_db = imp.load_source('my_db', '/home/faucet/ryu/ryu/app/my_db.py') #directory to our own folder
 
# Ovsdb
# provide application specific support to the adaptive security network project
class Ovsdb(my_db.PnetMacDB):
    def __init__(self,dbhost='localhost',dbuser='root',
                 schema='ovsDB',pwd='root'):
        super(Ovsdb, self).__init__(dbhost,dbuser,schema,pwd)

    def isUnknownPC(self,mac):
        # input a mac addr.
        # check if there is any machine match at the T_Q_ZONE_PC
        # return True if not found
        if self.conn == None:
            self.dbOpen()
        query="select count(*) FROM T_Q_ZONE_PC WHERE  "
        query=query+" MAC_ADDR = %s "

        try:
            cursor = self.conn.cursor() 
            cursor.execute(query,mac)
            row = cursor.fetchone()
            if row:
                c = row[0]
            else:
                c = 0
            cursor.close()
            #print "count is ",c
            if c == 0:
                return True
            else:
                return False
        except pymysql.Error, e:
            print "ERROR %d IN SELECT: %s" % (e.args[0], e.args[1])   

    def isNewPC(self,mac):
        # input a mac addr.
        # check if there is any machine match at the T_Q_ZONE_PC
        # return True if not found
        if self.conn == None:
            self.dbOpen()
        query="select count(*) FROM T_Q_ZONE_PC WHERE  CHK_STATUS = 'F' AND "
        query=query+" MAC_ADDR = %s "
             
        try:
            cursor = self.conn.cursor() 
            cursor.execute(query,mac)
            row = cursor.fetchone()
            if row:
                c = row[0]
            else:
                c = 0
            cursor.close()
            #print "count is ",c
            if c == 0:
                return True
            else:
                return False
        except pymysql.Error, e:
            print "ERROR %d IN SELECT: %s" % (e.args[0], e.args[1])

    def setTrustPCByIP(self,ip_addr):
        # update an entry of  T_Q_ZONE_PC to trusted
        if self.conn == None:
            self.dbOpen()
        query="UPDATE T_Q_ZONE_PC SET CHK_STATUS = 'T', LAST_MOD_TM = now() WHERE "
        query=query+" IP_ADDR = %s "
        #print query
        try:
            cursor = self.conn.cursor() 
            retval = cursor.execute(query,ip_addr)
            #print "retval is ",retval
            cursor.close()
            if retval > 0:
                self.conn.commit()
                return True
            else:
                return False
        except pymysql.Error, e:
            print "ERROR %d IN setTrustPCByIP: %s" % (e.args[0], e.args[1])

    def setTrustPC(self,mac,ip_addr):
        # update an entry of  T_Q_ZONE_PC to trusted
        if self.conn == None:
            self.dbOpen()
        query="UPDATE T_Q_ZONE_PC SET CHK_STATUS = 'T', LAST_MOD_TM = now() , IP_ADDR = %s WHERE "
        query=query+" MAC_ADDR = %s "
  
        try:
            cursor = self.conn.cursor() 
            retval = cursor.execute(query,(ip_addr, mac))
       
            cursor.close()
            if retval > 0:
                self.conn.commit()
                return True
            else:
                return False
        except pymysql.Error, e:
            print "ERROR %d IN setTrustPC: %s" % (e.args[0], e.args[1])
    def getMacByIP(self,ip_addr):
        # input a mac addr.
        # check if there is any machine match at the T_Q_ZONE_PC
        # return True if not found
        
        if self.conn == None:
            self.dbOpen()
        query="select MAC_ADDR FROM T_Q_ZONE_PC WHERE  "
        query=query+" IP_ADDR = %s "
        print query
        print ip_addr   
        try:
            cursor = self.conn.cursor() 
            cursor.execute(query,ip_addr)

            row = cursor.fetchone()
            if row:
                mac = row[0]
            else:
                mac = None
            cursor.close()
            return mac
        except pymysql.Error, e:
            print "ERROR %d IN SELECT: %s" % (e.args[0], e.args[1])

    def isTrustedPCbyIP(self,ip_addr):
        # input a mac addr.
        # check if there is any machine match at the T_Q_ZONE_PC
        # return True if not found
        if ip_addr:
            #print "enter isTrustedPCbyIP with ",ip_addr

            if self.conn == None:
                self.dbOpen()
            query="select count(*) FROM T_Q_ZONE_PC WHERE CHK_STATUS = 'T' and "
            query=query+" IP_ADDR = %s " 
            try:
                cursor = self.conn.cursor() 
                cursor.execute(query,ip_addr)
                row = cursor.fetchone()
                if row:
                    c = row[0]
                else:
                    c = 0
                cursor.close()
                #print "count is ",c
                if c == 0:
                    return False
                else:
                    return True
            except pymysql.Error, e:
                print "ERROR %d IN SELECT: %s" % (e.args[0], e.args[1])
        else:
            print "Invalid IP"
            return False

    def isTrustedPC(self,mac):
        # input a mac addr.
        # check if there is any machine match at the T_Q_ZONE_PC
        # return True if not found
        if self.conn == None:
            self.dbOpen()
        query="select count(*) FROM T_Q_ZONE_PC WHERE CHK_STATUS = 'T' and "
        query=query+" MAC_ADDR = %s "
             
        try:
            cursor = self.conn.cursor() 
            cursor.execute(query,mac)
            row = cursor.fetchone()
            if row:
                c = row[0]
            else:
                c = 0
            cursor.close()
            #print "count is ",c
            if c == 0:
                return False
            else:
                return True
        except pymysql.Error, e:
            print "ERROR %d IN SELECT: %s" % (e.args[0], e.args[1])
        
    def insertNewPC(self,mac,in_port):
        # insert a new entry to T_Q_ZONE_PC with minimum information.
        if self.conn == None:
            self.dbOpen()
        query="INSERT INTO T_Q_ZONE_PC (MAC_ADDR, CHK_STATUS, IN_PORT, CREAT_TM, LAST_MOD_TM) "
        query=query+" VALUES ( %s, 'F', %s, now(), now())"
        #print query
        try:
            cursor = self.conn.cursor() 
            retval = cursor.execute(query,(mac,in_port))
            #print "retval is ",retval
            cursor.close()
            if retval > 0:
                self.conn.commit()
                return True
            else:
                return False
        except pymysql.Error, e:
            print "ERROR %d IN insertNewPC: %s" % (e.args[0], e.args[1])

    def clear_Q_ZONE_TABLE(self,):
        # need to clear all Q Zone Records
        if self.conn == None:
            self.dbOpen()
        query= "DELETE FROM T_Q_ZONE_PC "
        try:
            cursor = self.conn.cursor() 
            retval = cursor.execute(query)
            #print "retval is ",retval
            cursor.close()
            if retval > 0:
                self.conn.commit()
        except pymysql.Error, e:
            print "ERROR %d IN setTrustPC: %s" % (e.args[0], e.args[1])

    def updateNewPC(self,mac,ip_addr):
        # update the ip_addr col of an entry of  T_Q_ZONE_PC  
        if self.conn == None:
            self.dbOpen()
        query="UPDATE T_Q_ZONE_PC SET LAST_MOD_TM = now() , IP_ADDR = %s WHERE "
        query=query+" MAC_ADDR = %s "
      
        try:
            cursor = self.conn.cursor() 
            retval = cursor.execute(query,(ip_addr, mac))
          
            cursor.close()
            if retval > 0:
                self.conn.commit()
                return True
            else:
                return False
        except pymysql.Error, e:
            print "ERROR %d IN setTrustPC: %s" % (e.args[0], e.args[1])
