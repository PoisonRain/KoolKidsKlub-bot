from elf_kingdom import *
import math

Xa = 0
Ya = 0
Xb = 5
Yb = 5

Mab = (Ya - Yb) // (Xa - Xb)
A = -Mab
B = 1
C = Mab * Xb - Yb

Mbp = - 1

Xp = (5 * math.sqrt(A * A + B * B) - C - B * (Yb + ((1 // Mab)) * Xb)) // (A - (1 // Mab))
print (Xp)

