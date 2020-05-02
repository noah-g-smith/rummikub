##
import numpy as np
import routines
import time
import views
import itertools as it
import more_itertools as mit
import multiset as mset
import routines
from _collections import defaultdict


##
@routines.timer
def super_runs():

    # initialise empty list of supersets
    leftover_supersets_out = []

    # loop through every
    for run_length in range(3, 14):

        # add trivial set (all tiles in super run returned)
        super_run = np.array(range(0, run_length))
        super_set = set()
        super_set.add(mset.FrozenMultiset(super_run + 1))

        # loop for all possible return tile sets
        for run in views.views(run_length):
            super_set.add(mset.FrozenMultiset(np.delete(super_run, run) + 1))

        # add superset of possible returned tile sets
        leftover_supersets_out.append(super_set)

    return leftover_supersets_out


##
@routines.timer
def combos(run_1, run_2):
    set_out = set()
    for sub_run_1 in views.views(len(run_1)):
        for sub_run_2 in views.views(len(run_2)):
            set_out.add(mset.FrozenMultiset(np.delete(run_1, sub_run_1))
                        + mset.FrozenMultiset(np.delete(run_2, sub_run_2)))

    return set_out


@routines.timer
def remains(run_1):
    set_out = set()
    for run in views.views(len(run_1)):
        set_out.add(mset.FrozenMultiset(np.delete(run_1, run)))

    return set_out


##
run1 = np.array([1, 2, 3, 4, 5, 6, 7])
run2 = np.array([4, 5, 6, 7, 8, 9, 10])
run3 = np.array(range(1, 11))
run4 = np.array([4, 5, 6, 7])
run5 = np.array([1, 2, 3, 4, 5, 6, 7])
run6 = np.array([5, 6, 7, 8, 9, 10])
run7 = np.array(range(1, 11))
run8 = np.array([5, 6, 7])


##
set_1, dups_1 = combos(run1, run2)
set_2, dups_2 = combos(run3, run4)


##


@routines.timer
def mset_mapping(set_in, mapping):
    set_out = set()
    for multiset in set_in:
        mset_dict = defaultdict()
        for x, y in multiset.items():
            mset_dict[x + mapping] = multiset[x]
        fmset_out = mset.FrozenMultiset(mset_dict)
        set_out.add(fmset_out)

    return set_out


##
leftover_supersets = super_runs()

mapped_set_1 = leftover_supersets[6]
mapped_set_2 = mset_mapping(leftover_supersets[6], 3)
mapped_set_3 = leftover_supersets[9]
mapped_set_4 = mset_mapping(leftover_supersets[1], 3)


@routines.timer
def combos_2(set_in_1, set_in_2):
    set_out = set()
    for x, y in it.product(set_in_1, set_in_2):
        set_out.add(x + y)

    return set_out


##
@routines.timer
def combos_3(*args):

    for combo in it.product(*args):
        print(set(combo))
    # return {sum(*combo) for combo in it.product(*args)}
