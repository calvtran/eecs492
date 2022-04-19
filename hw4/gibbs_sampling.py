# from typing import OrderedDict
import numpy as np
import random

class BayesNet:
	def __init__(self, node_specs=None):
		"""
		Nodes must be ordered with parents before children.
		:param node_specs: iterable object, each element contains (variable name, parents name, cpt) for each node
		"""
		self.nodes = []
		self.variables = []
		node_specs = node_specs or []
		for node_spec in node_specs:
			self.add(node_spec)

	def add(self, node_spec):
		"""
		Add a node to the net. Its parents must already be in the net, and its variable must not.
		"""
		node = BayesNode(*node_spec)
		assert node.variable not in self.variables
		assert all((parent in self.variables) for parent in node.parents)
		self.nodes.append(node)
		self.variables.append(node.variable)
		for parent in node.parents:
			self.variable_node(parent).children.append(node)

	def variable_node(self, var):
		"""
		Return the node for the variable named var.
		"""
		for n in self.nodes:
			if n.variable == var:
				return n
		raise Exception("No such variable: {}".format(var))

	def variable_values(self, var):
		"""Return the domain of var."""
		return [True, False]


class BayesNode:
	def __init__(self, X, parents, cpt):
		"""
		:param X: variable name,
		:param parents: a space-separated string representing the names of parent nodes or the empty string is the current node has no parents
		:param cpt: the conditional probability table, takes one of these forms:
		* A number, the unconditional probability P(X=true). You can use this form when there are no parents.
		* A dict {v: p, ...}, the conditional probability distribution P(X=true | parent=v) = p. Use this form when there's just one parent.
		* A dict {(v1, v2, ...): p, ...}, the distribution P(X=true | parent1=v1, parent2=v2, ...) = p. Each key must have as many values as there are parents. You can use this form always; the first two are just conveniences.
		In all cases the probability of X being false is left implicit, since it follows from P(X=true).
		>>> X = BayesNode('X', '', 0.2)
		>>> Y = BayesNode('Y', 'P', {T: 0.2, F: 0.7})
		>>> Z = BayesNode('Z', 'P Q', {(T, T): 0.2, (T, F): 0.3, (F, T): 0.5, (F, F): 0.7})
		"""
		if isinstance(parents, str):
			parents = parents.split()
		if isinstance(cpt, (float, int)):  # no parents, 0-tuple
			cpt = {(): cpt}
		elif isinstance(cpt, dict):
			# one parent, 1-tuple
			if cpt and isinstance(list(cpt.keys())[0], bool):
				cpt = {(v,): p for v, p in cpt.items()}

		assert isinstance(cpt, dict)
		for vs, p in cpt.items():
			assert isinstance(vs, tuple) and len(vs) == len(parents)
			assert all(isinstance(v, bool) for v in vs)
			assert 0 <= p <= 1

		self.variable = X
		self.parents = parents
		self.cpt = cpt
		self.children = []

	def cpt_prob(self, value, event):
		""" 
		Return the conditional probability P(X=value | parents=parent_values), where parent_values are the values of parents in event. (event must assign each parent a value.)
		>>> bn.cpt_prob(False, {'Burglary': False, 'Earthquake': True})
		"""
		assert isinstance(value, bool)
		p_true = self.cpt[self.event_values(event, self.parents)]
		return p_true if value else 1 - p_true

	def event_values(self, event, variables):
		"""Return a tuple of the values of variables in event.
		>>> event {'MaryCalls': True, 'Burglary': False, 'Earthquake': False, 'Alarm': False, 'JohnCalls': False}, variables ['Burglary', 'Earthquake']
		(False, False)
		>>> event {'MaryCalls': True, 'Burglary': False, 'Earthquake': False, 'Alarm': True, 'JohnCalls': False}, variables ['Alarm']
		(True,)
		"""
		if isinstance(event, tuple) and len(event) == len(variables):
			return event
		else:
			return tuple([event[var] for var in variables])


def gibbs_ask(X, e, bn, N):
	"""
	X: query variable
	e: evidence
	bn: Bayesian network
	N: number of samples
	"""
	assert X not in e, "Query variable must be distinct from evidence"

	### TODO: Implement Gibbs sampling algorithm as described in the pseudocode ####
	c = {True: 0, False: 0}
	z = []
	x = {}
	for i in bn.nodes:
		if i.variable not in e:
			x[i.variable] = random.choice([True, False])
			z.append(i.variable)
		else:
			x[i.variable] = e[i.variable]

	for k in range(N):
		for z_i in z:
			node_Z_i = bn.variable_node(z_i)

			par_vals = {}
			for par in node_Z_i.parents:
				par_vals[par] = x[par]
			p = node_Z_i.cpt_prob(True, par_vals)
			q = node_Z_i.cpt_prob(False, par_vals)
			for ch in node_Z_i.children:
				p_ch_par_vals = {}
				q_ch_par_vals = {}
				for ch_par in ch.parents:
					if ch_par is z_i:
						p_ch_par_vals[ch_par] = True
						q_ch_par_vals[ch_par] = False
					else:
						p_ch_par_vals[ch_par] = x[ch_par]
						q_ch_par_vals[ch_par] = x[ch_par]
				p *= ch.cpt_prob(x[ch.variable], p_ch_par_vals)
				q *= ch.cpt_prob(x[ch.variable], q_ch_par_vals)

			p = p / (p + q)
			q = q / (p + q)

			x[z_i] = sample(p)

		if x[X]:
			c[True] += 1
		else:
			c[False] += 1

	c[True] = c[True]/N
	c[False] = c[False]/N
	return c		

def sample(prob):
	if np.random.rand() < prob:
		return True
	return False


def main():
	T, F = True, False

	net = BayesNet([
		('Burglary', '', 0.001),
		('Earthquake', '', 0.002),
		('Alarm', 'Burglary Earthquake', {(T, T): 0.70, (T, F): 0.01, (F, T): 0.70, (F, F): 0.01}),
		('JohnCalls', 'Alarm', {T: 0.90, F: 0.05}),
		('MaryCalls', 'Alarm', {T: 0.70, F: 0.01})
		])

	print(gibbs_ask('JohnCalls', dict(Burglary=T), net, 100000))
	print(gibbs_ask('JohnCalls', dict(Alarm=T, Burglary=T), net, 100000))
	print(gibbs_ask('JohnCalls', dict(MaryCalls=T), net, 100000))
	print(gibbs_ask('MaryCalls', dict(Alarm=T, Burglary=F), net, 100000))
	print(gibbs_ask('MaryCalls', dict(Earthquake=F, JohnCalls=T), net, 100000))
	print(gibbs_ask('MaryCalls', dict(Alarm=F), net, 100000))

if __name__ == "__main__":
	main()