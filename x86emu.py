# flags = {
#   'zf' = None
# }
import unittest
from z3 import *

class Registers(object):

  def __init__(self):
    self._registers = {'eax':0,
                       'ebx':0, 
                       'ecx':0, 
                       'edx':0, 
                      }

  def set_reg(self, reg, val):
    if len(reg) is 3:
      self._registers[reg] = val

    if len(reg) is 2:
      self._registers['e'+reg[0]+'x'] &= 0xFFFFFF00
      self._registers['e'+reg[0]+'x'] |= val

  def get_reg(self, reg):
    if len(reg) is 3:
      return self._registers[reg]

    if len(reg) is 2:
      return self._registers['e'+reg[0]+'x'] & 0xFF

state = {}
state['memory'] = None
state['registers'] = Registers()
state['flags'] = {'zf':0}

def set_reg(*args):
  return state['registers'].set_reg(*args)

def get_reg(*args):
  return state['registers'].get_reg(*args)

# INSTRUCTION IMPLEMENTATIONS
def mov_imm(reg, imm):
  set_reg(reg, imm)

def mov_addr(reg, offset):
  set_reg(reg, state['memory'][offset])

def mov_regs(dst, src):
  set_reg(dst, get_reg(src))

def cmp(addr, reg):
  compare = state['memory'][addr] - get_reg(reg)
  if compare < 0:
    state['flags']['zf'] = -1
  elif compare > 0:
    state['flags']['zf'] = 1
  else:
    state['flags']['zf'] = 0

def add_imm(dst, imm):
  if type(imm) is str:
    imm = ord(imm)
  val = get_reg(dst) + imm
  set_reg(dst, val)

def xor_reg(dst, src):
  val = get_reg(dst) ^ get_reg(src)
  set_reg(dst, val)

def and_imm(dst, imm):
  if type(imm) is str:
    imm = ord(imm)
  val = get_reg(dst) & imm
  set_reg(dst, val)

def rol(reg, imm):
    value = get_reg(reg)
    for x in range(imm):
        if len(reg) is 2:
            msb = value >> 7
            value <<= 1
            value =  (msb + value) & 0xFF
        else:
            msb = value >> 31
            value <<= 1
            value = (msb + value) & 0xFFFFFFFF
    set_reg(reg, value)


def verify_code(code):
  state['memory'] = code

  mov_imm('esi', 0)
  mov_imm('edx', 0xfa)
  mov_addr('al', 0)
  rol('edx', 5)
  xor_reg('dl', 'al')
  add_imm('dl', 0xab)
  mov_addr('al', 1)
  rol('edx', 3)
  xor_reg('dl', 'al')
  add_imm('dl', 0x45)
  mov_addr('al', 2)
  rol('edx', 1)
  xor_reg('dl', 'al')
  add_imm('dl', 0x12)
  mov_addr('al', 3)
  rol('edx', 9)
  xor_reg('dl', 'al')
  add_imm('dl', 0xcd)
  mov_regs('cl', 'dl')
  and_imm('cl', 15)
  add_imm('cl', 'a')
  cmp(4, 'cl')
  if state['flags']['zf'] is not 0: 
    return False
  rol('edx', 12)
  xor_reg('dl', 'cl')
  add_imm('dl', 0x87)
  mov_regs('cl', 'dl')
  and_imm('cl', 15)
  add_imm('cl', 'a')
  cmp(5, 'cl')
  if state['flags']['zf'] is not 0: 
    return False
  rol('edx', 3)
  xor_reg('dl', 'cl')
  add_imm('dl', 0xef)
  mov_regs('cl', 'dl')
  and_imm('cl', 15)
  add_imm('cl', 'C')
  cmp(6, 'cl')
  if state['flags']['zf'] is not 0: 
    return False
  rol('edx', 1)
  xor_reg('dl', 'cl')
  add_imm('dl', 0x10)
  mov_regs('cl', 'dl')
  and_imm('cl', 15)
  add_imm('cl', 'f')
  cmp(7, 'cl')
  if state['flags']['zf'] is not 0: 
    return False
  rol('edx', 13)
  xor_reg('dl', 'cl')
  add_imm('dl', 0x9a)
  mov_regs('cl', 'dl')
  and_imm('cl', 15)
  add_imm('cl', 'e')
  cmp(8, 'cl')
  if state['flags']['zf'] is not 0: 
    return False
  rol('edx', 9)
  xor_reg('dl', 'cl')
  add_imm('dl', 0xa8)
  mov_regs('cl', 'dl')
  and_imm('cl', 15)
  add_imm('cl', 'D')
  cmp(9, 'cl')
  if state['flags']['zf'] is not 0: 
    return False
  rol('edx', 7)
  xor_reg('dl', 'cl')
  add_imm('dl', 0xca)
  mov_regs('cl', 'dl')
  and_imm('cl', 15)
  add_imm('cl', 'D')
  cmp(10, 'cl')
  if state['flags']['zf'] is not 0: 
    return False
  rol('edx', 2)
  xor_reg('dl', 'cl')
  add_imm('dl', 0x91)
  mov_regs('cl', 'dl')
  and_imm('cl', 15)
  add_imm('cl', 'c')
  cmp(11, 'cl')
  if state['flags']['zf'] is not 0: 
    return False
  rol('edx', 5)
  xor_reg('dl', 'cl')
  add_imm('dl', 0x86)
  mov_regs('cl', 'dl')
  and_imm('cl', 15)
  add_imm('cl', 'A')
  cmp(12, 'cl')
  if state['flags']['zf'] is not 0: 
    return False
  rol('edx', 6)
  xor_reg('dl', 'cl')
  add_imm('dl', 0xf1)
  mov_regs('cl', 'dl')
  and_imm('cl', 15)
  add_imm('cl', 'e')
  cmp(13, 'cl')
  if state['flags']['zf'] is not 0: 
    return False
  rol('edx', 3)
  xor_reg('dl', 'cl')
  add_imm('dl', 0x1f)
  mov_regs('cl', 'dl')
  and_imm('cl', 15)
  add_imm('cl', 'B')
  cmp(14, 'cl')
  if state['flags']['zf'] is not 0: 
    return False
  rol('edx', 4)
  xor_reg('dl', 'cl')
  add_imm('dl', 0x90)
  mov_regs('cl', 'dl')
  and_imm('cl', 15)
  add_imm('cl', 'f')
  cmp(15, 'cl')
  if state['flags']['zf'] is not 0: 
    return False

  return True




class TestEmu(unittest.TestCase):

  def test(self):
    set_reg('edx', 10)
    self.assertEqual(10, get_reg('edx'))
    self.assertEqual(10, get_reg('edx'))
    set_reg('dl', 30)
    self.assertEqual(30, get_reg('dl'))
    self.assertEqual(30, get_reg('edx'))
    set_reg('edx', 0xffff1337)
    self.assertEqual(0xffff1337, get_reg('edx'))
    self.assertEqual(0x37, get_reg('dl'))

def main():
  c0 = BitVec('c0', 8)
  c1 = BitVec('c1', 8)
  c2 = BitVec('c2', 8)
  c3 = BitVec('c3', 8)
  c4 = BitVec('c4', 8)
  c5 = BitVec('c5', 8)
  c6 = BitVec('c6', 8)
  c7 = BitVec('c7', 8)
  c8 = BitVec('c8', 8)
  c9 = BitVec('c9', 8)
  c10 = BitVec('c10', 8)
  c11 = BitVec('c11', 8)
  c12 = BitVec('c12', 8)
  c13 = BitVec('c13', 8)
  c14 = BitVec('c14', 8)
  c15 = BitVec('c15', 8)


  s = Solver()

  s.assert_and_track(verify_code([c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15]) == True)
  print(s.check())
  m = s.model()
  print(m[occWrites_1])
  print(m[occWrites_1].sexpr())

if __name__ == '__main__':
  main()