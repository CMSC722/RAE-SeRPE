def pickupCargo(state, r, c, p):
	if state['state_vars']['on-robot'][(r,)] == 'None' and state['state_vars']['in-pile'][(c,)] == p:
		state['state_vars']['on-robot'][(r,)] = c
		state['state_vars']['in-pile'][(c,)] = 'None'
		return True
	else:
		return False

def putCargo(state, r, c, p):
	if state['state_vars']['on-robot'][(r,)] == c:
		state['state_vars']['on-robot'][(r,)] = 'None'
		state['state_vars']['in-pile'][(c,)] = p
		return True
	else:
		return False