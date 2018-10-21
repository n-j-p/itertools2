def permutations_multiset(multiset):
    '''permutations_multiset(mutliset) --> permutations generator
    
    Return successive permutations of elements in a multiset.
    itertools.permutations returns repeated permutations when the 
    multiplicity of an element in the multiset is greater than one.

    permutations_multiset([1,1,0,2]) -->
        (1, 1, 0, 2),
        (1, 1, 2, 0),
        (1, 0, 1, 2),
        (1, 0, 2, 1),
        (1, 2, 1, 0),
        (1, 2, 0, 1),
        (0, 1, 1, 2),
        (0, 1, 2, 1),
        (0, 2, 1, 1),
        (2, 1, 1, 0),
        (2, 1, 0, 1),
        (2, 0, 1, 1)'''
    # Take unique elements of multiset, preserving order:
    elements = tuple(dict.fromkeys(multiset))
    multiplicities = tuple([multiset.count(x) for x in elements])
    return _permutations_multiset_from_multiplicities(elements,
                                                      multiplicities)

def _permutations_multiset_from_multiplicities(elements, multiplicities):
    import itertools as it
    if max(multiplicities) == 1:
        for x in it.permutations(elements):
            yield x
    elif len(multiplicities) == 1:
        yield (elements[0],) * multiplicities[0]
    else:
        for i,x in enumerate(elements):
            if multiplicities[i] == 1:
                g = _permutations_multiset_from_multiplicities(elements[:i] +\
                                 elements[(i+1):],
                                 multiplicities[:i] + multiplicities[(i+1):])

            else:
                g = _permutations_multiset_from_multiplicities(elements,
                                 multiplicities[:i] + \
                                 (multiplicities[i] - 1,) + \
                                 multiplicities[(i+1):])
            for y in g:
                yield (x,) + y
