class SpassWriter(object):

    def write_spass(self, model, ceremony, spass_name):
        with open(model, "r") as spass_model:
            self.spass = spass_model.read() #open the model file

        self.ceremony = ceremony

        self.init = "\n"
        self.peers_forms = "\n"
        self.att_forms = "\n"
        self.keys_forms = "\n"
        self.knows = "\n"
        self.conjectures = "\n"
        self.text = "\n"

        self.generate_atts_formulae()
        self.generate_peers_formulae()
        self.generate_messages_formulae()
        self.generate_message_set_formulae()

        self.spass = self.spass.replace("%VARIABLES TODO\n", self.init)

        self.text += self.peers_forms + self.att_forms + self.keys_forms + self.knows + "\n\n\n"
        self.generate_steps()


        self.spass = self.spass.replace("%DECLARATIONS AND STEPS TODO", self.text)
        self.spass = self.spass.replace("%CONJECTURES TODO", self.conjectures)

        with open(spass_name + ".dfg","w") as spass_doc:
            spass_doc.write(self.spass)


    def split_capabilities(self, capab):
        if capab == "DY":
            return ["E", "B", "S", "I", "C", "O", "F"]

        return capab.split("+")


    def generate_steps(self):
        if self.ceremony.capab[0][0] == "N":
            form = 'formula(\n\t{}_N(sent({},{},{})),\nstep1).\n\n'.format(self.ceremony.layer[0], self.ceremony.sender[0], self.ceremony.receiver[0], self.ceremony.msg[0])
            previous = '\t\t{}_N(sent({},{},{})),\n'.format(self.ceremony.layer[0], self.ceremony.sender[0], self.ceremony.receiver[0], self.ceremony.msg[0])
            self.text += form

        elif len(self.ceremony.att[0]) > 1: #if the very first message has more than one attacker
            previous = self.generate_several_attackers_first_step()
        else: #ONE ATTACKER ONLY
            previous = self.generate_one_attacker_first_step() #method for one attacker only in first message

        self.generate_remaining_steps(previous) #calls method for remaining steps!


    def generate_one_attacker_first_step(self):
        if not "+" in self.ceremony.capab[0][0] and not "DY" in self.ceremony.capab[0][0]:  # only one capability: ' E' , ' S' ...
            form = 'formula(\n\t{}_{}(sent({},{},{}),{}),\nstep1).\n\n'.format(self.ceremony.layer[0], self.ceremony.capab[0][0], self.ceremony.sender[0], self.ceremony.receiver[0],
 self.ceremony.msg[0], self.ceremony.att[0][0])
            previous = '\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.ceremony.layer[0], self.ceremony.capab[0][0], self.ceremony.sender[0], self.ceremony.receiver[0], self.ceremony.msg[0], self.ceremony.att[0][0])

        else:  # more *capabilities* than just one
            cap_set = self.split_capabilities(self.ceremony.capab[0][0])

            form = "formula(\n\tand(\n" #needs and in the formulae
            previous = "\t\tand(\n" #needs and in the formulae

            for capability in cap_set[:-1]: #for each capability but the last

                form += '\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.ceremony.layer[0], capability, self.ceremony.sender[0], self.ceremony.receiver[0], self.ceremony.msg[0], self.ceremony.att[0][0])
                previous += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.ceremony.layer[0], capability, self.ceremony.sender[0], self.ceremony.receiver[0], self.ceremony.msg[0], self.ceremony.att[0][0])

            previous += '\t\t\t{}_{}(sent({},{},{}),{})\n\t\t),\n'.format(self.ceremony.layer[0], cap_set[-1], self.ceremony.sender[0], self.ceremony.receiver[0], self.ceremony.msg[0], self.ceremony.att[0][0])
            form += '\t\t{}_{}(sent({},{},{}),{})\n\t),\nstep1).\n\n'.format(self.ceremony.layer[0], cap_set[-1], self.ceremony.sender[0], self.ceremony.receiver[0], self.ceremony.msg[0], self.ceremony.att[0][0])

        self.text += form
        return previous


    def generate_several_attackers_first_step(self):
        form = "formula(\n\tand(\n"
        previous = "\t\tand(\n"

        for index, att in enumerate(self.ceremony.att[0]):

            if len(self.ceremony.capab[0][index]) == 1:  # only one cap: ' E' , ' S' ...
                form += '\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.ceremony.layer[0], self.ceremony.capab[0][index], self.ceremony.sender[0], self.ceremony.receiver[0], self.ceremony.msg[0], att)
                previous += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.ceremony.layer[0], self.ceremony.capab[0][index], self.ceremony.sender[0], self.ceremony.receiver[0], self.ceremony.msg[0], att)

            else:  # more capabilities than just one (DY or  E + B ...and so on and so forth)
                cap_set = self.split_capabilities(self.ceremony.capab[0][index])

                for capability in cap_set[:-1]:
                    form += '\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.ceremony.layer[0], capability, self.ceremony.sender[0], self.ceremony.receiver[0], self.ceremony.msg[0], att)
                    previous += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.ceremony.layer[0], capability, self.ceremony.sender[0], self.ceremony.receiver[0], self.ceremony.msg[0], att)

                previous += '\t\t\t{}_{}(sent({},{},{}),{})\n\t\t),\n'.format(self.ceremony.layer[0], cap_set[-1], self.ceremony.sender[0], self.ceremony.receiver[0], self.ceremony.msg[0], att)
                form += '\t\t{}_{}(sent({},{},{}),{})\n\t),\nstep1).\n\n'.format(self.ceremony.layer[0], cap_set[-1], self.ceremony.sender[0], self.ceremony.receiver[0], self.ceremony.msg[0], att)

        self.text += form
        return previous


    def generate_remaining_steps(self, previous):
        remaining_msgs = self.ceremony.msg[1:]
        index = 1

        for msg in remaining_msgs:
            form = "formula(\n\timplies(\n" + previous

            if self.ceremony.capab[index][0] == "N": #NO ATTACKER
                form += '\t\t{}_N(sent({},{},{}))\n\t),\nstep{}).\n\n'.format(self.ceremony.layer[index], self.ceremony.sender[index], self.ceremony.receiver[index], msg, str(index+1))
                previous = '\t\t{}_N(sent({},{},{})),\n'.format(self.ceremony.layer[index], self.ceremony.sender[index], self.ceremony.receiver[index], msg)

            elif len(self.ceremony.att[index]) == 1: #ONLY ONE ATTACKER
                if len(self.ceremony.capab[index][0]) == 1: ##ONLY ONE CAPABILITY!

                    form += '\t\t{}_{}(sent({},{},{}),{})\n\t),\nstep{}).\n\n'.format(self.ceremony.layer[index], self.ceremony.capab[index][0], self.ceremony.sender[index], self.ceremony.receiver[index], self.ceremony.msg[index], self.ceremony.att[index][0], str(index+1))
                    previous = '\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.ceremony.layer[index], self.ceremony.capab[index][0], self.ceremony.sender[index],self.ceremony.receiver[index], self.ceremony.msg[index], self.ceremony.att[index][0])

                else: # SEVERAL CAPABILITIES
                    form += "\t\tand(\n"
                    previous = "\t\tand(\n"

                    cap_set = self.split_capabilities(self.ceremony.capab[index][0])

                    for capab in cap_set[:-1]: #all capabilities of the list but the last one
                        form += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.ceremony.layer[index], capab, self.ceremony.sender[index], self.ceremony.receiver[index], msg, self.ceremony.att[index][0], str(index+1))
                        previous += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.ceremony.layer[index], capab, self.ceremony.sender[index], self.ceremony.receiver[index], msg, self.ceremony.att[index][0])

                    form += '\t\t\t{}_{}(sent({},{},{}),{})\n\t\t)\n\t),\nstep{}).\n\n'.format(self.ceremony.layer[index], cap_set[-1], self.ceremony.sender[index], self.ceremony.receiver[index], msg, self.ceremony.att[index][0], str(index+1))
                    previous += '\t\t\t{}_{}(sent({},{},{}),{})\n\t\t),\n'.format(self.ceremony.layer[index], cap_set[-1], self.ceremony.sender[index], self.ceremony.receiver[index], msg, self.ceremony.att[index][0])

            else: #SEVERAL ATTACKERS
                info = self.generate_several_attackers_steps(index, form)
                form = info[0]
                previous = info[1]

            self.text += form
            index += 1


    def generate_several_attackers_steps(self, index, form):
        form += "\t\tand(\n"
        previous = "\t\tand(\n"

        for att_index, att in enumerate(self.ceremony.att[index]):
            cap_set = self.split_capabilities(self.ceremony.capab[index][att_index])

            if len(cap_set) == 1:
                form += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.ceremony.layer[index], self.ceremony.capab[index][att_index], self.ceremony.sender[index], self.ceremony.receiver[index], self.ceremony.msg[index], att,str(index+1))
                previous += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.ceremony.layer[index], self.ceremony.capab[index][att_index], self.ceremony.sender[index], self.ceremony.receiver[index], self.ceremony.msg[index], att)

            else: #more than one capab
                for cap in cap_set[:-1]:
                    form += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.ceremony.layer[index], cap, self.ceremony.sender[index], self.ceremony.receiver[index], self.ceremony.msg[index], att)
                    previous += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.ceremony.layer[index], cap, self.ceremony.sender[index], self.ceremony.receiver[index], self.ceremony.msg[index], att)

                form += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.ceremony.layer[index], cap_set[-1], self.ceremony.sender[index], self.ceremony.receiver[index], self.ceremony.msg[index], att)
                previous += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.ceremony.layer[index], cap_set[-1], self.ceremony.sender[index], self.ceremony.receiver[index], self.ceremony.msg[index], att)


        form = form[:-2]
        form += '\n\t\t)\n\t),\nstep{}).\n\n'.format(str(index+1))

        previous = previous[:-2]
        previous += "\n\t\t),\n"

        return [form, previous]


    def generate_messages_formulae(self):
        for index, msg in enumerate(self.ceremony.msg): #for each message
            encrypted = False
            pair_flag = False
            sender = self.ceremony.sender[index]
            attacker = self.ceremony.att[index]
            key = self.ceremony.keys[index]

            if not key == "":
                self.generate_key_formula(index)
                encrypted = True

            if "," in msg:
                pair = msg.split(",");
                self.ceremony.msg[index] = "pair({0},{1})".format(pair[0],pair[1])
                pair_flag = True

                if '({0},0),\n'.format(pair[0]) and '({0},0),\n'.format(pair[1]) not in self.init:
                    self.init += '({0},0),\n'.format(pair[0])
                    self.init += '({0},0),\n'.format(pair[1])

                if 'formula(KnowsPair({0},pair({1},{2})),agent_{0}_knows_pair_{1}_and_{2}).\n'.format(sender, pair[0], pair[1]) not in self.knows:
                    self.knows += 'formula(KnowsPair({0},pair({1},{2})),agent_{0}_knows_pair_{1}_and_{2}).\n'.format(sender, pair[0], pair[1])

                if len(attacker) == 1 and not attacker[0] == "":
                    if 'formula(KnowsPair({0},pair({1},{2}))'.format(attacker,pair[0],pair[1],key) not in self.conjectures:
                        self.conjectures += 'formula(KnowsPair({0},pair({1},{2})),attacker_{0}_knows_pair_{1}_and_{2}).\n'.format(attacker[0],pair[0],pair[1])
                elif len(attacker) > 1 and not attacker[0] == "":
                    for att in attacker:
                        if 'formula(KnowsPair({0},pair({1},{2}))'.format(att,pair[0],pair[1]) not in self.conjectures:
                            self.conjectures += 'formula(KnowsPair({0},pair({1},{2})),attacker_{0}_knows_pair_{1}_and_{2}).\n'.format(att,pair[0],pair[1])


            if encrypted and pair_flag:
                if 'KnowsEncr({0},encr(pair({1},{2}),{3}))'.format(sender,pair[0],pair[1],key) not in self.knows:
                    self.knows += 'formula(KnowsEncr({0},encr(pair({1},{2}),{3})),agent_{0}_knows_encr_pair_{1}_and_{2}).\n'.format(sender,pair[0],pair[1],key)

                if len(attacker) == 1 and not attacker[0] == "":
                    if 'formula(KnowsEncr({0},encr(pair({1},{2}),{3}))'.format(attacker,pair[0],pair[1],key) not in self.conjectures:
                        self.conjectures += 'formula(KnowsEncr({0},encr(pair({1},{2}),{3})),attacker_{0}_knows_encr_pair_{1}_and_{2}).\n'.format(attacker[0],pair[0],pair[1],key)
                elif len(attacker) > 1 and not attacker[0] == "":
                    for att in attacker:
                        if 'formula(KnowsEncr({0},encr(pair({1},{2}),{3}))'.format(att,pair[0],pair[1],key) not in self.conjectures:
                            self.conjectures += 'formula(KnowsEncr({0},encr(pair({1},{2}),{3})),attacker_{0}_knows_encr_pair_{1}_and_{2}).\n'.format(att,pair[0],pair[1],key)


            if encrypted and not pair_flag:
                if 'KnowsEncr({0},encr({1},{2}))'.format(sender,msg,key) not in self.knows:
                    self.knows += 'formula(KnowsEncr({0},encr({1},{2})),agent_{0}_knows_encr_{1}_and_{2}).\n'.format(sender,msg,key)

                if len(attacker) == 1 and not attacker[0] == "":
                    if 'formula(KnowsEncr({0},encr({1},{2}))'.format(attacker,msg,key) not in self.conjectures:
                        self.conjectures += 'formula(KnowsEncr({0},encr({1},{2})),attacker_{0}_knows_encr_{1}_and_{2}).\n'.format(attacker[0],msg,key)
                elif len(attacker) > 1 and not attacker[0] == "":
                    for att in attacker:
                        if 'formula(KnowsEncr({0},encr({1},{2}))'.format(att,msg,key) not in self.conjectures:
                            self.conjectures += 'formula(KnowsEncr({0},encr({1},{2})),attacker_{0}_knows_encr_{1}_and_{2}).\n'.format(att,msg,key)


            if not encrypted and not pair_flag:
                if '({0},0),\n'.format(msg) not in self.init:
                    self.init += '({0},0),\n'.format(msg)

                if 'formula(Knows({0},{1})'.format(sender,msg) not in self.knows:
                    self.knows += 'formula(Knows({0},{1}),agent_{0}_knows_{1}).\n'.format(sender,msg)

                if len(attacker) == 1 and not attacker[0] == "":
                    if 'formula(Knows({0},{1})'.format(attacker,msg) not in self.conjectures:
                        self.conjectures += 'formula(Knows({0},{1}),attacker_{0}_knows_{1}).\n'.format(attacker[0],msg)
                elif len(attacker) > 1 and not attacker[0] == "":
                    for att in attacker:
                        if 'formula(Knows({0},{1})'.format(att,msg) not in self.conjectures:
                            self.conjectures += 'formula(Knows({0},{1}),attacker_{0}_knows_{1}).\n'.format(att,msg)


    def generate_key_formula(self, index):
        if '({},0),\n'.format(self.ceremony.keys[index]) not in self.init:
            self.init += '({},0),\n'.format(self.ceremony.keys[index])  #adds declaration for key as a variable

        if 'Key({0}),key_{0}'.format(self.ceremony.keys[index]) not in self.keys_forms:
            self.keys_forms += 'formula(Key({0}),key_{0}).\n'.format(self.ceremony.keys[index]) #adds Key predicate


    def generate_atts_formulae(self):
        for att in self.ceremony.atts:
            if (att != ""):
                if not "({0},0),".format(att) in self.init:
                    self.init += "({0},0),\n".format(att) #attackers declaration as a variable

                if not 'formula(Attacker({0}),attacker_{0}).\n'.format(att) in self.att_forms:
                    self.att_forms += 'formula(Attacker({0}),attacker_{0}).\n'.format(att) #attacker predicate

                if att == "dy" and not 'formula(DY({0}),DY_{0}).\n'.format(att) in self.att_forms:
                    self.att_forms += 'formula(DY({0}),DY_{0}).\n'.format(att)

                elif "da" in att and not 'formula(DA({0}),DA_{0}).\n'.format(att) in self.att_forms:
                    self.att_forms += 'formula(DA({0}),DA_{0}).\n'.format(att)

                elif "ma" in att and not 'formula(MA({0}),MA_{0}).\n'.format(att) in self.att_forms:
                    self.att_forms += 'formula(MA({0}),MA_{0}).\n'.format(att)


    def generate_peers_formulae(self):
        for peer in self.ceremony.peers: #CONSIDERING THAT NO AGENT IS ALSO AN ATTACKER!!!!!!!!!!!!!
            if not "({0},0),".format(peer) in self.init:
                self.init += '({},0),\n'.format(peer) #all peers with no repetition are declared in spass

            if not 'formula(Agent({0}),agent_{0}).\n'.format(peer) in self.peers_forms:
                self.peers_forms += 'formula(Agent({0}),agent_{0}).\n'.format(peer) #peers are agents (with no repetition)
                self.peers_forms += 'formula(Honest({0}),honest_{0}).\n'.format(peer) #all peers are honest


    def generate_message_set_formulae(self):
        for msg in self.ceremony.msgs:
            if  '({},0),\n'.format(msg) not in self.init and not "," in msg:
                self.init += '({},0),\n'.format(msg) #message declaration as a variable
