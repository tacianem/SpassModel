

    def firstStepSeveral(self,ceremony): #first msg - several

        self.ceremony = ceremony
        form = "formula(\n\tand(\n"
        previous = "\t\tand(\n"

        for index, att in enumerate(self.att):

            if len(self.capab[0][index]) == 1:  # only one cap: ' E' , ' S' ...
                #print self.capab[0] #TODO

                form += '\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.layer[0], self.capab[0], self.sender[0], self.receiver[0], self.msg[0], att)
                previous += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.layer[0], self.capab[0], self.sender[0], self.receiver[0], self.msg[0], att)

            else:  # more capabilities than just one (DY or  E + B ...and so on and so forth)
                cap_set = self.capabilitiesArray(self.capab[0][index])

                for capab in cap_set[:-1]:

                        form += '\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.layer[0], capab, self.sender[0], self.receiver[0], self.msg[0], att)
                        previous += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.layer[0], capab, self.sender[0], self.receiver[0], self.msg[0], att)

                previous += '\t\t\t{}_{}(sent({},{},{}),{})\n\t\t),\n'.format(self.layer[0], cap_set[-1], self.sender[0], self.receiver[0], self.msg[0], att)
                form += '\t\t{}_{}(sent({},{},{}),{})\n\t),\nstep1).\n\n'.format(self.layer[0], cap_set[-1], self.sender[0], self.receiver[0], self.msg[0], att)

            self.ceremony += form
            return [self.ceremony, previous]



    def remainingSteps(self,info):
        self.ceremony = info[0]
        previous = info[1]

        msg1 = self.msg[1:]
        index = 1

        for msg in msg1:

            form = "formula(\n\timplies(\n" + previous #implies

            if self.capab[index][0] == "N": #NO ATTACKER
                form += '\t\t{}_N(sent({},{},{}))\n\t),\nstep{}).\n\n'.format(self.layer[index], self.sender[index], self.receiver[index], msg, str(index+1))
                previous = '\t\t{}_N(sent({},{},{})),\n'.format(self.layer[index], self.sender[index], self.receiver[index], msg)

            elif len(self.att[index]) == 1 and not self.att[index][0] == "": #ONLY ONE ATTACKER

                if len(self.capab[index][0]) == 1: ##ONLY ONE CAPABILITY!

                    form += '\t\t{}_{}(sent({},{},{}),{})\n\t),\nstep{}).\n\n'.format(self.layer[index], self.capab[index][0], self.sender[index], self.receiver[index], self.msg[index], self.att[index][0], str(index+1))
                    previous = '\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.layer[index], self.capab[index][0], self.sender[index],self.receiver[index], self.msg[index], self.att[index][0])

                else: # SEVERAL CAPABILITIES
                    form += "\t\tand(\n"
                    previous = "\t\tand(\n"

                    for capability in self.capab[index]:

                        cap_set = self.capabilitiesArray(capability)

                        for capab in cap_set[:-1]: #all capabilities of the list but the last one

                            form += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.layer[index], capab, self.sender[index], self.receiver[index], msg, self.att[index][0], str(index+1))
                            previous += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.layer[index], capab, self.sender[index], self.receiver[index], msg, self.att[index][0])

                        form += '\t\t\t{}_{}(sent({},{},{}),{})\n\t\t)\n\t),\nstep{}).\n\n'.format(self.layer[index], cap_set[-1], self.sender[index], self.receiver[index], msg, self.att[index][0], str(index+1))
                        previous += '\t\t\t{}_{}(sent({},{},{}),{})\n\t\t),\n'.format(self.layer[index], cap_set[-1], self.sender[index], self.receiver[index], msg, self.att[index][0])


            else: #SEVERAL ATTACKERS
                print msg
                ssi = self.severalSteps(index)
                form += ssi[0]
                previous = ssi[1]

            self.ceremony += form
            index += 1

        return self.ceremony



    def severalSteps(self, i):

        form = "\t\tand(\n"
        previous = "\t\tand(\n"

        for index, att in enumerate(self.att[i]):

            cap_set = self.capabilitiesArray(self.capab[i][index][0])
            if len(cap_set) == 1:
                form += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.layer[i], self.capab[i][index][0], self.sender[i], self.receiver[i], self.msg[i], att[0],str(i+1))
                previous += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.layer[i], self.capab[i][index][0], self.sender[i], self.receiver[i], self.msg[i], att[0])

            else: #more than one capab

                for cap in cap_set[:-1]:

                    form += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.layer[i], cap, self.sender[i], self.receiver[i], self.msg[i], att[0])
                    previous += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.layer[i], cap, self.sender[i], self.receiver[i], self.msg[i], att[0])

                form += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.layer[i], cap_set[-1], self.sender[i], self.receiver[i], self.msg[i], att[0])
                previous += '\t\t\t{}_{}(sent({},{},{}),{}),\n'.format(self.layer[i], cap_set[-1], self.sender[i], self.receiver[i], self.msg[i], att[0])


        form = form[:-2]
        form += '\n\t\t)\n\t),\nstep{}).\n\n'.format(str(i+1))

        previous = previous[:-2]
        previous += "\n\t\t),\n"

        return [form,previous]



spass = Spass()
