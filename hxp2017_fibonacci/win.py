#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ctypes
import sys
import pyqbdi
import struct

""" solve by using gdb script
flag = ""
while True:
    e("si", to_string=True)
    pc = int(e("p/x $rip", to_string=True).split("=")[1].strip(), 16)
    if pc == 0x400686: # set fibo
        rdi = int(e("p/x $rdi", to_string=True).split("=")[1].strip(), 16)
        e("set $rax={:#x}".format(a[rdi]))
        e("set {{int}}$rbp={:#x}".format(sss[rdi-1]^sss[rdi-2]))
        e("set $rip=0x40069f")
    elif pc == 0x40055c: # print flag
        rdi = int(e("p/x $rdi", to_string=True).split("=")[1].strip(), 16)
        flag += chr(rdi)
        sys.stdout.write("\rflag: "+flag)
    elif pc == 0x4006ed:
        s = int(e("x/wx $rbp", to_string=True).split(":")[1].strip(), 16)
        sss.append(s)
    elif pc == 0x400570:
        break
"""

# generate fibo
fibo = []
sss = [1]
for i in range(256):
    if i == 0 or i == 1:
        fibo.append(1)
    else:
        r1 = fibo[i-1] & 0xffffffff
        r2 = fibo[i-2] & 0xffffffff
        now = (r1 + r2) & 0xffffffff
        fibo.append(ctypes.c_uint(now).value)
flag = ""

def u32(x):
    return struct.unpack('<I', x.ljust(4, '\x00'))[0]

def p32(x):
    return struct.pack('<I', x & 0xffffffff)

def cb1(vm, gpr, fpr, data):
    global sss, fibo
    rbp = pyqbdi.readMemory(gpr.rbp, 4)
    sss.append(u32(rbp))
    return pyqbdi.CONTINUE

def cb2(vm, gpr, fpr, data):
    global sss, fibo
    rdi = gpr.rdi
    gpr.rax = fibo[rdi]
    ddd = (sss[rdi-1] ^ sss[rdi-2])&0xffffffff
    pyqbdi.writeMemory(gpr.rbp, p32(ddd))
    gpr.rip = 0x40069f
    vm.setGPRState(gpr)
    return pyqbdi.BREAK_TO_VM

def cb3(vm, gpr, fpr, data):
    global flag
    rdi = gpr.rdi
    flag += chr(rdi)
    sys.stdout.write("\rflag: "+flag)
    if "}" in flag:
        print ""
        return pyqbdi.STOP
    else:
        return pyqbdi.CONTINUE

def pyqbdipreload_on_run(vm, start, stop):
    vm.addCodeAddrCB(0x4006ed, pyqbdi.PREINST, cb1, None)
    vm.addCodeAddrCB(0x400686, pyqbdi.PREINST, cb2, None)
    vm.addCodeAddrCB(0x40055c, pyqbdi.PREINST, cb3, None)
    vm.run(start, stop)
