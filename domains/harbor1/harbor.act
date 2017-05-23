def load(state, r, c, c_p, p, d):
  if (p,d) in state['rigid_rels']['at'] and state['state_vars']['cargo'][(r,)] == 'nil' and \
      state['state_vars']['loc'][(r,)] == d and state['state_vars']['pos'][(c,)] == c_p and \
      state['state_vars']['top'][(p,)] == c:
    state['state_vars']['cargo'][(r,)] = c
    state['state_vars']['pile'][(c,)] = 'nil'
    state['state_vars']['pos'][(c,)] = r
    state['state_vars']['top'][(p,)] = c_p
    return True
  else:
    return False

def unload(state, r, c, c_p, p, d):
  if (p,d) in state['rigid_rels']['at'] and state['state_vars']['pos'][(c,)] == r and \
      state['state_vars']['loc'][(r,)] == d and state['state_vars']['top'][(p,)] == c_p:
    state['state_vars']['cargo'][(r,)] = 'nil'
    state['state_vars']['pile'][(c,)] = p
    state['state_vars']['pos'][(c,)] = c_p
    state['state_vars']['top'][(p,)] = c
    return True
  else:
    return False

def move(state, r, d, d_p):
  if (d,d_p) in state['rigid_rels']['adjacent'] and state['state_vars']['loc'][(r,)] == d and \
      state['state_vars']['occupied'][(d_p,)] == 'false':
    state['state_vars']['loc'][(r,)] = d_p
    state['state_vars']['occupied'][(d,)] = 'false'
    state['state_vars']['occupied'][(d_p,)] = 'true'
    return True
  else:
    return False
