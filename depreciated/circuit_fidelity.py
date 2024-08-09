
hadamard_fidelity = 0.999
cphase_fidelity = 0.999
iswap_fidelity = 0.999
cnot_fidelity = 0.999
readout_fidelity = 0.98
cdisplacement_fidelity = 0.9

include_readout_fidelity = True

def swap(x,y):
    x = x * cnot_fidelity * y
    y = x
    y = y * cnot_fidelity * x
    x = y
    x = x * cnot_fidelity * y
    y = x
    return x,y

'''def iswap(x,y):
    y = y * cnot_fidelity * x
    x = x * cnot_fidelity * y
    y = y * cnot_fidelity * x
    return x,y'''

## Begin error calculation on XX interaction, version 1
xx1_transmon_a_fidelity = 1
xx1_transmon_b_fidelity = 1
xx1_transmon_l_fidelity = 1
xx1_l_cavity_fidelity = 1
## Apply 2 hadamards to a and b
xx1_transmon_a_fidelity = xx1_transmon_a_fidelity * hadamard_fidelity
xx1_transmon_b_fidelity = xx1_transmon_b_fidelity * hadamard_fidelity
## Apply cnot from b onto a
xx1_transmon_a_fidelity = xx1_transmon_a_fidelity * cnot_fidelity * xx1_transmon_b_fidelity
xx1_transmon_b_fidelity = xx1_transmon_a_fidelity
## Apply swap (a and l)
xx1_transmon_a_fidelity, xx1_transmon_l_fidelity = swap(xx1_transmon_a_fidelity, xx1_transmon_l_fidelity)
## Apply controlled displacement (l and l_cavity)
xx1_l_cavity_fidelity = xx1_transmon_l_fidelity * cdisplacement_fidelity * xx1_l_cavity_fidelity
## Apply swap (l and a)
xx1_transmon_l_fidelity, xx1_transmon_a_fidelity = swap(xx1_transmon_l_fidelity, xx1_transmon_a_fidelity)
## Apply cnot from b onto a
xx1_transmon_a_fidelity = xx1_transmon_a_fidelity * cnot_fidelity * xx1_transmon_b_fidelity
xx1_transmon_b_fidelity = xx1_transmon_a_fidelity
## Apply 2 hadamards to a and b
xx1_transmon_a_fidelity = xx1_transmon_a_fidelity * hadamard_fidelity
xx1_transmon_b_fidelity = xx1_transmon_b_fidelity * hadamard_fidelity
print("XX Interaction, version 1")
print("transmon a fidelity: ", xx1_transmon_a_fidelity)
print("transmon b fidelity: ", xx1_transmon_b_fidelity)
print("transmon l fidelity: ", xx1_transmon_l_fidelity)
print("l cavity fidelity: ", xx1_l_cavity_fidelity)

## Begin error calculation on XX interaction, version 2
xx2_transmon_a_fidelity = 1
xx2_transmon_b_fidelity = 1
xx2_transmon_l_fidelity = 1
xx2_l_cavity_fidelity = 1
## Apply 2 hadamards to a and b
xx2_transmon_a_fidelity = xx2_transmon_a_fidelity * hadamard_fidelity
xx2_transmon_b_fidelity = xx2_transmon_b_fidelity * hadamard_fidelity
## Apply swap (b and l)
xx2_transmon_b_fidelity, xx2_transmon_l_fidelity = swap(xx2_transmon_b_fidelity, xx2_transmon_l_fidelity)
## Apply cnot from a onto l
xx2_transmon_l_fidelity = xx2_transmon_a_fidelity * cnot_fidelity * xx2_transmon_l_fidelity
xx2_transmon_a_fidelity = xx2_transmon_l_fidelity
## Apply controlled displacement (l and l_cavity)
xx2_l_cavity_fidelity = xx2_transmon_l_fidelity * cdisplacement_fidelity * xx2_l_cavity_fidelity
## Apply cnot from a onto l
xx2_transmon_l_fidelity = xx2_transmon_a_fidelity * cnot_fidelity * xx2_transmon_l_fidelity
xx2_transmon_a_fidelity = xx2_transmon_l_fidelity
## Apply swap (l and b)
xx2_transmon_l_fidelity, xx2_transmon_b_fidelity = swap(xx2_transmon_l_fidelity, xx2_transmon_b_fidelity)
## Apply 2 hadamards to a and b
xx2_transmon_a_fidelity = xx2_transmon_a_fidelity * hadamard_fidelity
xx2_transmon_b_fidelity = xx2_transmon_b_fidelity * hadamard_fidelity
print("XX Interaction, version 2")
print("transmon a fidelity: ", xx2_transmon_a_fidelity)
print("transmon b fidelity: ", xx2_transmon_b_fidelity)
print("transmon l fidelity: ", xx2_transmon_l_fidelity)
print("l cavity fidelity: ", xx2_l_cavity_fidelity)

'''
## Begin error calculation on XX interaction, version 1
xx1_transmon_a_fidelity = 1
xx1_transmon_b_fidelity = 1
xx1_transmon_l_fidelity = 1
xx1_l_cavity_fidelity = 1
## Apply 2 hadamards to a and b
xx1_transmon_a_fidelity = xx1_transmon_a_fidelity * hadamard_fidelity
xx1_transmon_b_fidelity = xx1_transmon_b_fidelity * hadamard_fidelity
## Apply cnot from b onto a
xx1_transmon_a_fidelity = xx1_transmon_a_fidelity * cnot_fidelity * xx1_transmon_b_fidelity
## Apply swap (a and l)
xx1_transmon_a_fidelity, xx1_transmon_l_fidelity = iswap(xx1_transmon_a_fidelity, xx1_transmon_l_fidelity)
## Apply controlled displacement (l and l_cavity)
xx1_l_cavity_fidelity = xx1_transmon_l_fidelity * cdisplacement_fidelity * xx1_l_cavity_fidelity
## Apply swap (l and a)
xx1_transmon_l_fidelity, xx1_transmon_a_fidelity = iswap(xx1_transmon_l_fidelity, xx1_transmon_a_fidelity)
## Apply cnot from b onto a
xx1_transmon_a_fidelity = xx1_transmon_a_fidelity * cnot_fidelity * xx1_transmon_b_fidelity
## Apply 2 hadamards to a and b
xx1_transmon_a_fidelity = xx1_transmon_a_fidelity * hadamard_fidelity
xx1_transmon_b_fidelity = xx1_transmon_b_fidelity * hadamard_fidelity
print("XX Interaction, version 1 iswap11")
print("transmon a fidelity: ", xx1_transmon_a_fidelity)
print("transmon b fidelity: ", xx1_transmon_b_fidelity)
print("transmon l fidelity: ", xx1_transmon_l_fidelity)
print("l cavity fidelity: ", xx1_l_cavity_fidelity)


## Begin error calculation on XX interaction, version 2
xx2_transmon_a_fidelity = 1
xx2_transmon_b_fidelity = 1
xx2_transmon_l_fidelity = 1
xx2_l_cavity_fidelity = 1
## Apply 2 hadamards to a and b
xx2_transmon_a_fidelity = xx2_transmon_a_fidelity * hadamard_fidelity
xx2_transmon_b_fidelity = xx2_transmon_b_fidelity * hadamard_fidelity
## Apply swap (b and l)
xx2_transmon_b_fidelity, xx2_transmon_l_fidelity = iswap(xx2_transmon_b_fidelity, xx2_transmon_l_fidelity)
## Apply cnot from a onto l
xx2_transmon_l_fidelity = xx2_transmon_a_fidelity * cnot_fidelity * xx2_transmon_l_fidelity
## Apply controlled displacement (l and l_cavity)
xx2_l_cavity_fidelity = xx2_transmon_l_fidelity * cdisplacement_fidelity * xx2_l_cavity_fidelity
## Apply cnot from a onto l
xx2_transmon_l_fidelity = xx2_transmon_a_fidelity * cnot_fidelity * xx2_transmon_l_fidelity
## Apply swap (l and b)
xx2_transmon_l_fidelity, xx2_transmon_b_fidelity = iswap(xx2_transmon_l_fidelity, xx2_transmon_b_fidelity)
## Apply 2 hadamards to a and b
xx2_transmon_a_fidelity = xx2_transmon_a_fidelity * hadamard_fidelity
xx2_transmon_b_fidelity = xx2_transmon_b_fidelity * hadamard_fidelity
print("XX Interaction, version 2 iswap11")
print("transmon a fidelity: ", xx2_transmon_a_fidelity)
print("transmon b fidelity: ", xx2_transmon_b_fidelity)
print("transmon l fidelity: ", xx2_transmon_l_fidelity)
print("l cavity fidelity: ", xx2_l_cavity_fidelity)

## Begin error calculation on XX interaction, version 1
xx1_transmon_a_fidelity = 1
xx1_transmon_b_fidelity = 1
xx1_transmon_l_fidelity = 1
xx1_l_cavity_fidelity = 1
## Apply 2 hadamards to a and b
xx1_transmon_a_fidelity = xx1_transmon_a_fidelity * hadamard_fidelity
xx1_transmon_b_fidelity = xx1_transmon_b_fidelity * hadamard_fidelity
## Apply cnot from b onto a
xx1_transmon_a_fidelity = xx1_transmon_a_fidelity * cnot_fidelity * xx1_transmon_b_fidelity
## Apply swap (a and l)
xx1_transmon_a_fidelity, xx1_transmon_l_fidelity = iswap(xx1_transmon_a_fidelity, xx1_transmon_l_fidelity)
## Apply controlled displacement (l and l_cavity)
xx1_l_cavity_fidelity = xx1_transmon_l_fidelity * cdisplacement_fidelity * xx1_l_cavity_fidelity
## Apply swap (l and a)
xx1_transmon_l_fidelity, xx1_transmon_a_fidelity = swap(xx1_transmon_l_fidelity, xx1_transmon_a_fidelity)
## Apply cnot from b onto a
xx1_transmon_a_fidelity = xx1_transmon_a_fidelity * cnot_fidelity * xx1_transmon_b_fidelity
## Apply 2 hadamards to a and b
xx1_transmon_a_fidelity = xx1_transmon_a_fidelity * hadamard_fidelity
xx1_transmon_b_fidelity = xx1_transmon_b_fidelity * hadamard_fidelity
print("XX Interaction, version 1 iswap10")
print("transmon a fidelity: ", xx1_transmon_a_fidelity)
print("transmon b fidelity: ", xx1_transmon_b_fidelity)
print("transmon l fidelity: ", xx1_transmon_l_fidelity)
print("l cavity fidelity: ", xx1_l_cavity_fidelity)


## Begin error calculation on XX interaction, version 2
xx2_transmon_a_fidelity = 1
xx2_transmon_b_fidelity = 1
xx2_transmon_l_fidelity = 1
xx2_l_cavity_fidelity = 1
## Apply 2 hadamards to a and b
xx2_transmon_a_fidelity = xx2_transmon_a_fidelity * hadamard_fidelity
xx2_transmon_b_fidelity = xx2_transmon_b_fidelity * hadamard_fidelity
## Apply swap (b and l)
xx2_transmon_b_fidelity, xx2_transmon_l_fidelity = iswap(xx2_transmon_b_fidelity, xx2_transmon_l_fidelity)
## Apply cnot from a onto l
xx2_transmon_l_fidelity = xx2_transmon_a_fidelity * cnot_fidelity * xx2_transmon_l_fidelity
## Apply controlled displacement (l and l_cavity)
xx2_l_cavity_fidelity = xx2_transmon_l_fidelity * cdisplacement_fidelity * xx2_l_cavity_fidelity
## Apply cnot from a onto l
xx2_transmon_l_fidelity = xx2_transmon_a_fidelity * cnot_fidelity * xx2_transmon_l_fidelity
## Apply swap (l and b)
xx2_transmon_l_fidelity, xx2_transmon_b_fidelity = swap(xx2_transmon_l_fidelity, xx2_transmon_b_fidelity)
## Apply 2 hadamards to a and b
xx2_transmon_a_fidelity = xx2_transmon_a_fidelity * hadamard_fidelity
xx2_transmon_b_fidelity = xx2_transmon_b_fidelity * hadamard_fidelity
print("XX Interaction, version 2 iswap10")
print("transmon a fidelity: ", xx2_transmon_a_fidelity)
print("transmon b fidelity: ", xx2_transmon_b_fidelity)
print("transmon l fidelity: ", xx2_transmon_l_fidelity)
print("l cavity fidelity: ", xx2_l_cavity_fidelity)

## Begin error calculation on XX interaction, version 1
xx1_transmon_a_fidelity = 1
xx1_transmon_b_fidelity = 1
xx1_transmon_l_fidelity = 1
xx1_l_cavity_fidelity = 1
## Apply 2 hadamards to a and b
xx1_transmon_a_fidelity = xx1_transmon_a_fidelity * hadamard_fidelity
xx1_transmon_b_fidelity = xx1_transmon_b_fidelity * hadamard_fidelity
## Apply cnot from b onto a
xx1_transmon_a_fidelity = xx1_transmon_a_fidelity * cnot_fidelity * xx1_transmon_b_fidelity
## Apply swap (a and l)
xx1_transmon_a_fidelity, xx1_transmon_l_fidelity = swap(xx1_transmon_a_fidelity, xx1_transmon_l_fidelity)
## Apply controlled displacement (l and l_cavity)
xx1_l_cavity_fidelity = xx1_transmon_l_fidelity * cdisplacement_fidelity * xx1_l_cavity_fidelity
## Apply swap (l and a)
xx1_transmon_l_fidelity, xx1_transmon_a_fidelity = iswap(xx1_transmon_l_fidelity, xx1_transmon_a_fidelity)
## Apply cnot from b onto a
xx1_transmon_a_fidelity = xx1_transmon_a_fidelity * cnot_fidelity * xx1_transmon_b_fidelity
## Apply 2 hadamards to a and b
xx1_transmon_a_fidelity = xx1_transmon_a_fidelity * hadamard_fidelity
xx1_transmon_b_fidelity = xx1_transmon_b_fidelity * hadamard_fidelity
print("XX Interaction, version 1 iswap01")
print("transmon a fidelity: ", xx1_transmon_a_fidelity)
print("transmon b fidelity: ", xx1_transmon_b_fidelity)
print("transmon l fidelity: ", xx1_transmon_l_fidelity)
print("l cavity fidelity: ", xx1_l_cavity_fidelity)


## Begin error calculation on XX interaction, version 2
xx2_transmon_a_fidelity = 1
xx2_transmon_b_fidelity = 1
xx2_transmon_l_fidelity = 1
xx2_l_cavity_fidelity = 1
## Apply 2 hadamards to a and b
xx2_transmon_a_fidelity = xx2_transmon_a_fidelity * hadamard_fidelity
xx2_transmon_b_fidelity = xx2_transmon_b_fidelity * hadamard_fidelity
## Apply swap (b and l)
xx2_transmon_b_fidelity, xx2_transmon_l_fidelity = swap(xx2_transmon_b_fidelity, xx2_transmon_l_fidelity)
## Apply cnot from a onto l
xx2_transmon_l_fidelity = xx2_transmon_a_fidelity * cnot_fidelity * xx2_transmon_l_fidelity
## Apply controlled displacement (l and l_cavity)
xx2_l_cavity_fidelity = xx2_transmon_l_fidelity * cdisplacement_fidelity * xx2_l_cavity_fidelity
## Apply cnot from a onto l
xx2_transmon_l_fidelity = xx2_transmon_a_fidelity * cnot_fidelity * xx2_transmon_l_fidelity
## Apply swap (l and b)
xx2_transmon_l_fidelity, xx2_transmon_b_fidelity = iswap(xx2_transmon_l_fidelity, xx2_transmon_b_fidelity)
## Apply 2 hadamards to a and b
xx2_transmon_a_fidelity = xx2_transmon_a_fidelity * hadamard_fidelity
xx2_transmon_b_fidelity = xx2_transmon_b_fidelity * hadamard_fidelity
print("XX Interaction, version 2 iswap01")
print("transmon a fidelity: ", xx2_transmon_a_fidelity)
print("transmon b fidelity: ", xx2_transmon_b_fidelity)
print("transmon l fidelity: ", xx2_transmon_l_fidelity)
print("l cavity fidelity: ", xx2_l_cavity_fidelity)
'''