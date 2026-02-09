# Nama File: TaxCollector.py
# Nama / NIM: Visco Argatha Tawa Tawa / 24060125120023
# Tanggal: 23 September 2025

def TaxCollector(g,j):
    if g<50.0:
        return g*j*0.85
    elif g>=50.0 and g<=150.0:
        return g*j*0.9
    elif g>150.0 and g<=500.0:
        return g*j*0.95
    else:
        return g*j

#JANGAN DIUBAH!
print(eval(input()))