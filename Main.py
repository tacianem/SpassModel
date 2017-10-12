from TexReader import read_tex
from SpassWriter import SpassWriter
import os

files = ["ceremony1.tex", "ceremony2.tex", "ceremony3.tex", "ceremony4.tex", "ceremony5.tex"]

writer = SpassWriter()

for file_name in files:

    ceremony = read_tex(file_name)
    spass_name = os.path.splitext(file_name)[0]
    writer.write_spass("ceremony_model.dfg", ceremony, spass_name)
    
    os.system('SPASS -DocProof {0}.dfg > {0}.txt'.format(spass_name)) #run SPASS on terminal
