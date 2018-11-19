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
    elements, multiplicities = _get_multiplicities(multiset)
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
def combinations_multiset(multiset, r):
    '''combinations_multiset(mutliset) --> combinations generator
    
    Return successive combinations of elements in a multiset.
    itertools.combinations returns repeated combinations when the 
    multiplicity of an element in the multiset is greater than one.

    combinations_multiset([1,1,0,2],2) -->
        (1, 1),
        (1, 0),
        (1, 2),
        (0, 2)'''
    # Take unique elements of multiset, preserving order:
    elements, multiplicities = _get_multiplicities(multiset)
    return _combinations_multiset_from_multiplicities(elements,
                                                      multiplicities, r)
    
def _combinations_multiset_from_multiplicities(elements, multiplicities, r):
    n = sum(multiplicities)
    if n == 0 or n < r:
        return
    import itertools as it
    if r == 1:
        for x in elements:
            yield (x,)
        return
    if max(multiplicities) == 1:
        for x in it.combinations(elements, r):
            yield x
    elif len(multiplicities) == 1:
        yield (elements[0],)*min(r,multiplicities[0])
    else:
        for i,x in enumerate(elements):
            if multiplicities[i] == 1:
                g = _combinations_multiset_from_multiplicities(elements[(i+1):],
                                   multiplicities[(i+1):],
                                   r-1)

            else:
                g = _combinations_multiset_from_multiplicities(elements[i:],
                                   (multiplicities[i] - 1,) + \
                                   multiplicities[(i+1):],
                                   r-1)
            for y in g:
                yield (x,) + y

def _get_multiplicities(multiset):
    # Take unique elements of multiset, preserving order:
    elements = tuple(dict.fromkeys(multiset))
    multiplicities = tuple([multiset.count(x) for x in elements])
    return (elements, multiplicities)

def zip_multiset(multiset1, multiset2):
    e1, m1 = _get_multiplicities(multiset1)
    e2, m2 = _get_multiplicities(multiset2)
    return _zip_multiset_from_multiplicities(multiset1, e1, m1,
                                             multiset2, e2, m2)

def _multiset_difference(multiset, toremove):
    rem = list(multiset)
    for x in toremove:
        rem.remove(x)
    return tuple(rem)

def _zip_multiset_from_multiplicities(ms1, e1, m1, ms2, e2, m2):
    n1 = sum(m1)
    n2 = sum(m2)
    assert n1 == n2
    if len(m2) == 1:
        yield tuple([(z,e2[0]) for z in ms1])
        return
    for x in _combinations_multiset_from_multiplicities(e1, m1, m2[0]):
        xrem = _multiset_difference(ms1, x)
        erem, mrem = _get_multiplicities(xrem)
        g = _zip_multiset_from_multiplicities(xrem, erem, mrem,
                                              _multiset_difference(ms2,
                                                                   [e2[0],]*\
                                                                   m2[0]),
                                              
                                              e2[1:], m2[1:])
        for y in g:
            yield tuple(zip(x, [e2[0],]*m2[0])) + y
            
        
