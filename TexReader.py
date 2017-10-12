import re
from Ceremony import Ceremony

def read_tex(file_name):
    if file_name:
        with open(file_name, "r") as tex:
            tex_lines = tex.readlines()

        print "\n\nFile: ", file_name
        parse = parse_tex(tex_lines)
        return build_ceremony(parse[0], parse[1])


def parse_tex(tex_lines):
    ceremony_steps = []
    keys = []

    print "\nREGULAR EXPRESSION result:"

    for line in tex_lines:
        if not line or line == "\n":
            continue

        encr_key = re.search(r"\\\{(.+)\\\}\s*\$\_([A-Za-z]+)\_\{pk\}\$\s*", line)
        if encr_key:
            encr = encr_key.groups()
            keys.append("key" + encr[1].lower())
        else:
            keys.append("")

        line = re.sub(r"(\d+\.\d+)", '', line)
        line = re.sub(r"(xrightarrow)|(textit)", '', line)
        line = re.sub(r"[\'\\\_\}\-\"]+", '', line)

        result = re.findall(r'[A-Za-z\d\+\s\,]*[^\s\$\.\&\{\}\(\)\:\[\]\*]+', line)
        print result
        ceremony_steps.append(result)

    return [keys, ceremony_steps]


def build_ceremony(keys, ceremony_steps):
    ceremony = Ceremony()
    ceremony.keys = keys

    for step in ceremony_steps:
        length = len(step)

        sender = step[0].lower()
        layer = step[1]

        if length == 5:
            capab = ["N"]
            att = [""]
            receiver = step[3].lower()
            message = step[4].replace(" ", "").lower()

            ceremony.add_step(sender, layer, capab, att, receiver, message)

        else: #not known length (2 ou more attackers)
            capabs =[] #capabilities
            attackers = []
            remaining = []

            if step[length-1] == "pk":
                remaining = step[2:length-4]
                receiver = step[length-4].lower()
                message = step[length-3].replace(" ", "").lower()
            else:
                 remaining = step[2:length-2]
                 receiver = step[length-2].lower()
                 message = step[length-1].replace(" ", "").lower()


            for index, element in enumerate(remaining):
                if index%2 == 0:
                    capabs.append(element)
                else:
                    attackers.append(element.lower().replace(",", ""))

            ceremony.add_step(sender, layer, capabs, attackers, receiver, message)


    ceremony.print_status()
    return ceremony
