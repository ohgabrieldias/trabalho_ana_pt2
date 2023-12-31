
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ESTRELA_KLEENE OU PARENTESE_DIR PARENTESE_ESQ SIMBOLO\n    expression : termo\n               | expression OU termo\n    \n    termo : fator\n          | termo fator\n    \n    fator : atom\n          | fator ESTRELA_KLEENE\n    \n    atom : SIMBOLO\n         | PARENTESE_ESQ expression PARENTESE_DIR\n    '
    
_lr_action_items = {'SIMBOLO':([0,2,3,4,5,6,7,8,9,11,12,],[5,5,-3,-5,-7,5,5,-4,-6,5,-8,]),'PARENTESE_ESQ':([0,2,3,4,5,6,7,8,9,11,12,],[6,6,-3,-5,-7,6,6,-4,-6,6,-8,]),'$end':([1,2,3,4,5,8,9,11,12,],[0,-1,-3,-5,-7,-4,-6,-2,-8,]),'OU':([1,2,3,4,5,8,9,10,11,12,],[7,-1,-3,-5,-7,-4,-6,7,-2,-8,]),'PARENTESE_DIR':([2,3,4,5,8,9,10,11,12,],[-1,-3,-5,-7,-4,-6,12,-2,-8,]),'ESTRELA_KLEENE':([3,4,5,8,9,12,],[9,-5,-7,9,-6,-8,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,6,],[1,10,]),'termo':([0,6,7,],[2,2,11,]),'fator':([0,2,6,7,11,],[3,8,3,3,8,]),'atom':([0,2,6,7,11,],[4,4,4,4,4,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> termo','expression',1,'p_expression','gerador_automato.py',48),
  ('expression -> expression OU termo','expression',3,'p_expression','gerador_automato.py',49),
  ('termo -> fator','termo',1,'p_termo','gerador_automato.py',59),
  ('termo -> termo fator','termo',2,'p_termo','gerador_automato.py',60),
  ('fator -> atom','fator',1,'p_fator','gerador_automato.py',69),
  ('fator -> fator ESTRELA_KLEENE','fator',2,'p_fator','gerador_automato.py',70),
  ('atom -> SIMBOLO','atom',1,'p_atom','gerador_automato.py',79),
  ('atom -> PARENTESE_ESQ expression PARENTESE_DIR','atom',3,'p_atom','gerador_automato.py',80),
]
