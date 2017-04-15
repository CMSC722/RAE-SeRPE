def pickupCargo(state, r, c, p):
	if state['on-robot'][(r,)] is None and state['in-pile'][(c,)] == p:
		state['on-robot'][(r,)] = c
		state['in-pile'][(c,)] = None
		return True
	else:
		return False

def putCargo(state, r, c, p):
	if state['on-robot'][(r,)] == c:
		state['on-robot'][(r,)] = None
		state['in-pile'][(c,)] = p
		return True
	else:
		return False