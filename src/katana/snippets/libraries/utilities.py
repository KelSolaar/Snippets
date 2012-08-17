def nodesWalker(node, ascendants=False):
	"""
	This definition is a generator used to walk into nodes hierarchy.

	:param node: Node to walk. ( Node )
	:param ascendants: Ascendants instead of descendants will be yielded. ( Boolean )
	:return: Node. ( Node )
	"""

	attribute = "getChildren" if not ascendants else "getParent"
	if not hasattr(node, attribute):
		return

	elements = getattr(node, attribute)
	elements = elements() if isinstance(elements(), list) else [elements()]

	for element in elements:
		yield element

		if not hasattr(element, attribute):
			continue

		for subElement in nodesWalker(element, ascendants=ascendants):
			yield subElement
