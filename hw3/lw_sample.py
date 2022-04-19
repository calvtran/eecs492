"""Likelihood Weighting"""

# from typing import OrderedDict
import numpy as np

NUM_ITER = 500000

def likelihood_weighting(cpt, cond_probs):
	"""
	:param cpt:
	A ordered dictionary specifies the input CPT parameters.
	Example:
	{
	'S': [[], [0.7]],
	'N': [[], [0.5]],
	'E': [['S','N'], [0.9, 0.6, 0.5, 0.2]],
	'R': [['E'], [0.6, 0.2]],
	'W': [['E','N'], [0.9, 0.7, 0.3, 0.2]]
	}

	:param cond_probs:
	An array specifies the output conditional probabilities we are interested in.
	Example:
	[[['w'],['n','e']], [['e'],['~s']], [['w'],[]]]
	which meanse we would like P(w|n,e), P(e|~s), and P(w).

	:return:
	An array specifies the output conditional probabilities you find.
	Example:
	[P(w|n,e), P(e|~s), P(w)]

	"""
	#TODO: Add codes here

	# Get cond_probs
	probs = np.array([])
	for cp in range(len(cond_probs)):

		# Parse queries
		Q_events = []
		Q_values = []
		for i in range(len(cond_probs[cp][0])):
			q = cond_probs[cp][0][i].upper()
			qVal = getVal(q)
			q = q.replace("~", "")

			Q_events.append(q)
			Q_values.append(qVal)

		# Parse evidence
		E_events = []
		E_values = []
		for j in range(len(cond_probs[cp][1])):
			e = cond_probs[cp][1][j].upper()
			eVal = getVal(e)
			e = e.replace("~", "")

			E_events.append(e)
			E_values.append(eVal)

		# Sampling
		passing = 0
		weights = 0
		for i in range(NUM_ITER):
			iter = {}
			w = 1
			# Evaluate each node every iteration
			for key, value in cpt.items():
				# If 'key' in evidence, update 'w'
				if key in E_values:
					offset = 0
					bin = []
					if len(value[0]) > 0:
						for k in range(len(value[0])):
							e = value[0][k]
							bin.append(iter[e])

						b_str = ''.join(['0' if b else '1' for b in bin])
						offset = int(b_str, 2)

					probability = value[1][offset]
					val = E_values[E_events.index(key)]
					if not val:
						probability = 1 - probability

					w *= probability
					x = val
				# Else, randomly sample given conditional probabilities
				else:
					offset = 0
					bin = []
					if len(value[0]) > 0:
						for k in range(len(value[0])):
							e = value[0][k]
							bin.append(iter[e])

						b_str = ''.join(['0' if b else '1' for b in bin])
						offset = int(b_str, 2)

					x = sample(value[1][offset])

				iter[key] = x
				
			q_matched = True
			e_matched = True
			for q in range(len(Q_events)):
				if Q_values[q] != iter[Q_events[q]]:
					q_matched = False
					break
			for e in range(len(E_events)):
				if E_values[e] != iter[E_events[e]]:
					e_matched = False
					break
			if e_matched:
				weights += w
				if q_matched:
					passing += w


		p = passing / weights

		if len(probs) == 0:
			probs = np.array([p])
		else:
			probs = np.append(probs, [p], axis=0)

	return probs

def getVal(x):
	if '~' in x:
		return False
	return True

def sample(prob):
	"""
	The standard sampling function. You should use this function to sample with the probability you specified.
	Example: sample(0.7) will return true with 70% probability and false with 30% probability.
	"""
	if np.random.rand() < prob:
		return True
	return False

if __name__ == '__main__':
	cpt = OrderedDict()
	cpt['S'] = [[], [0.7]]
	cpt['N'] = [[], [0.5]]
	cpt['E'] = [['S','N'], [0.9, 0.6, 0.5, 0.2]]
	cpt['R'] = [['E'], [0.6, 0.2]]
	cpt['W'] = [['E','N'], [0.9, 0.7, 0.3, 0.2]]

	cond_probs = [[['w'],['n','e']], [['r'],['e','~s']], [['w'],[]]]
	result = likelihood_weighting(cpt, cond_probs)