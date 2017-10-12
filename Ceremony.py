class Ceremony(object):

    def __init__(self):

        self.peers = set() #no repetitions - senders and receivers
        self.msgs = set() #no repetitions
        self.atts = set() #no repetitions

        self.keys = [] #cryptographic keys - possible blank ("")
        self.sender = [] #senders
        self.layer = [] #layers
        self.capab = [] #capabilities
        self.att = [] #attackers - possible blank ("")
        self.receiver = [] #receivers
        self.msg = [] #all messages in the order which they happened


    def add_step(self, sender, layer, capab, attackers, receiver, message):
        self.peers.add(sender)
        self.sender.append(sender)
        self.layer.append(layer)
        self.capab.append(capab)
        for att in attackers:
            self.att.append([att])
            self.atts.add(att)
        self.receiver.append(receiver)
        self.peers.add(receiver)
        self.msg.append(message)
        self.msgs.add(message)


    def print_status(self):
        print "\n\nPEERS SET --------------------------------\n", self.peers
        print "\n\nMSGS SET ---------------------------------\n", self.msgs
        print "\n\nATTS SET ---------------------------------\n", self.atts

        print "\n\nKEYS -------------------------------------\n", self.keys
        print "\n\nSENDER -----------------------------------\n", self.sender
        print "\n\nLAYER ------------------------------------\n", self.layer
        print "\n\nCAPAB ------------------------------------\n", self.capab
        print "\n\nATT --------------------------------------\n", self.att
        print "\n\nRECEIVER ---------------------------------\n", self.receiver
        print "\n\nMSG --------------------------------------\n", self.msg
