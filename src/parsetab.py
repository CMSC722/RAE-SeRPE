
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'INT FLOAT BOOL NIL OBJ RIG SVS S0 GOAL ID LPAREN RPAREN LBRACK RBRACK COLON COMMA EQUALS TRUE FALSEstart : obj rig s0 goalobj : OBJ COLON obj_setsrig : RIG COLON rig_relss0 : S0 COLON initial_state_atomsgoal : GOAL COLON goal_state_atomsobj_sets :\n                | ID EQUALS obj_set obj_setsobj_set : LBRACK INT RBRACK\n               | LBRACK FLOAT RBRACK\n               | LBRACK BOOL RBRACK\n               | LBRACK NIL RBRACK\n               | LBRACK obj_atoms      obj_atoms : RBRACK\n                | obj_atom RBRACK\n                | obj_atom COMMA obj_atoms obj_atom : ID\n                | INT\n                | FLOAT\n                | TRUE\n                | FALSE\n                | NIL   rig_rels :\n                | ID EQUALS rig_rel rig_rels rig_rel : LBRACK tuplestuples : RBRACK\n              | tuple RBRACK\n              | tuple COMMA tuples tuple : LPAREN idsids : RPAREN\n           | ID RPAREN\n           | ID COMMA ids initial_state_atoms :\n                           | ID LPAREN ids EQUALS obj_atom initial_state_atoms goal_state_atoms :\n                        | ID LPAREN ids EQUALS ID goal_state_atoms '
    
_lr_action_items = {'RBRACK':([18,24,25,26,27,30,31,32,33,35,45,46,52,55,56,57,60,61,65,69,],[29,40,-20,41,42,43,44,-19,-16,47,29,59,-29,-18,-21,-17,47,-28,-30,-31,]),'FLOAT':([18,45,63,],[24,55,55,]),'OBJ':([0,],[1,]),'GOAL':([10,17,23,25,32,33,55,56,57,68,71,],[16,-32,-4,-20,-19,-16,-18,-21,-17,-32,-33,]),'NIL':([18,45,63,],[26,56,56,]),'INT':([18,45,63,],[27,57,57,]),'RPAREN':([39,49,51,54,64,],[52,52,52,65,52,]),'S0':([6,9,13,36,47,48,50,59,66,],[11,-22,-3,-22,-25,-24,-23,-26,-27,]),'EQUALS':([8,14,52,53,62,65,69,],[12,20,-29,63,67,-30,-31,]),'FALSE':([18,45,63,],[25,25,25,]),'LBRACK':([12,20,],[18,35,]),'BOOL':([18,],[30,]),'COLON':([1,5,11,16,],[4,9,17,21,]),'LPAREN':([22,35,38,60,],[39,49,51,49,]),'RIG':([3,4,7,19,28,29,34,40,41,42,43,44,58,],[5,-6,-2,-6,-12,-13,-7,-9,-11,-8,-10,-14,-15,]),'COMMA':([24,25,26,27,31,32,33,46,52,54,55,56,57,61,65,69,],[-18,-20,-21,-17,45,-19,-16,60,-29,64,-18,-21,-17,-28,-30,-31,]),'TRUE':([18,45,63,],[32,32,32,]),'ID':([4,9,17,18,19,21,25,28,29,32,33,36,39,40,41,42,43,44,45,47,48,49,51,55,56,57,58,59,63,64,66,67,68,70,],[8,14,22,33,8,38,-20,-12,-13,-19,-16,14,54,-9,-11,-8,-10,-14,33,-25,-24,54,54,-18,-21,-17,-15,-26,33,54,-27,70,22,38,]),'$end':([2,15,21,37,70,72,],[0,-1,-34,-5,-34,-35,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'rig_rels':([9,36,],[13,50,]),'obj':([0,],[3,]),'goal':([10,],[15,]),'tuple':([35,60,],[46,46,]),'rig_rel':([20,],[36,]),'obj_atoms':([18,45,],[28,58,]),'s0':([6,],[10,]),'obj_sets':([4,19,],[7,34,]),'ids':([39,49,51,64,],[53,61,62,69,]),'start':([0,],[2,]),'tuples':([35,60,],[48,66,]),'obj_set':([12,],[19,]),'obj_atom':([18,45,63,],[31,31,68,]),'rig':([3,],[6,]),'goal_state_atoms':([21,70,],[37,72,]),'initial_state_atoms':([17,68,],[23,71,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('start -> obj rig s0 goal','start',4,'p_start','dom_parser.py',63),
  ('obj -> OBJ COLON obj_sets','obj',3,'p_obj','dom_parser.py',76),
  ('rig -> RIG COLON rig_rels','rig',3,'p_rig','dom_parser.py',80),
  ('s0 -> S0 COLON initial_state_atoms','s0',3,'p_s0','dom_parser.py',90),
  ('goal -> GOAL COLON goal_state_atoms','goal',3,'p_goal','dom_parser.py',94),
  ('obj_sets -> <empty>','obj_sets',0,'p_obj_sets','dom_parser.py',103),
  ('obj_sets -> ID EQUALS obj_set obj_sets','obj_sets',4,'p_obj_sets','dom_parser.py',104),
  ('obj_set -> LBRACK INT RBRACK','obj_set',3,'p_obj_set','dom_parser.py',114),
  ('obj_set -> LBRACK FLOAT RBRACK','obj_set',3,'p_obj_set','dom_parser.py',115),
  ('obj_set -> LBRACK BOOL RBRACK','obj_set',3,'p_obj_set','dom_parser.py',116),
  ('obj_set -> LBRACK NIL RBRACK','obj_set',3,'p_obj_set','dom_parser.py',117),
  ('obj_set -> LBRACK obj_atoms','obj_set',2,'p_obj_set','dom_parser.py',118),
  ('obj_atoms -> RBRACK','obj_atoms',1,'p_obj_atoms','dom_parser.py',134),
  ('obj_atoms -> obj_atom RBRACK','obj_atoms',2,'p_obj_atoms','dom_parser.py',135),
  ('obj_atoms -> obj_atom COMMA obj_atoms','obj_atoms',3,'p_obj_atoms','dom_parser.py',136),
  ('obj_atom -> ID','obj_atom',1,'p_obj_atom','dom_parser.py',146),
  ('obj_atom -> INT','obj_atom',1,'p_obj_atom','dom_parser.py',147),
  ('obj_atom -> FLOAT','obj_atom',1,'p_obj_atom','dom_parser.py',148),
  ('obj_atom -> TRUE','obj_atom',1,'p_obj_atom','dom_parser.py',149),
  ('obj_atom -> FALSE','obj_atom',1,'p_obj_atom','dom_parser.py',150),
  ('obj_atom -> NIL','obj_atom',1,'p_obj_atom','dom_parser.py',151),
  ('rig_rels -> <empty>','rig_rels',0,'p_rig_rels','dom_parser.py',170),
  ('rig_rels -> ID EQUALS rig_rel rig_rels','rig_rels',4,'p_rig_rels','dom_parser.py',171),
  ('rig_rel -> LBRACK tuples','rig_rel',2,'p_rig_rel','dom_parser.py',181),
  ('tuples -> RBRACK','tuples',1,'p_tuples','dom_parser.py',185),
  ('tuples -> tuple RBRACK','tuples',2,'p_tuples','dom_parser.py',186),
  ('tuples -> tuple COMMA tuples','tuples',3,'p_tuples','dom_parser.py',187),
  ('tuple -> LPAREN ids','tuple',2,'p_tuple','dom_parser.py',196),
  ('ids -> RPAREN','ids',1,'p_ids','dom_parser.py',200),
  ('ids -> ID RPAREN','ids',2,'p_ids','dom_parser.py',201),
  ('ids -> ID COMMA ids','ids',3,'p_ids','dom_parser.py',202),
  ('initial_state_atoms -> <empty>','initial_state_atoms',0,'p_initial_state_atoms','dom_parser.py',237),
  ('initial_state_atoms -> ID LPAREN ids EQUALS obj_atom initial_state_atoms','initial_state_atoms',6,'p_initial_state_atoms','dom_parser.py',238),
  ('goal_state_atoms -> <empty>','goal_state_atoms',0,'p_goal_state_atoms','dom_parser.py',270),
  ('goal_state_atoms -> ID LPAREN ids EQUALS ID goal_state_atoms','goal_state_atoms',6,'p_goal_state_atoms','dom_parser.py',271),
]