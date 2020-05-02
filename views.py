import numpy as np
import time
import more_itertools as mit
import itertools as it


def timer(f):
    def timed(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()

        print('{}{}: {} ms'.format(f.__name__, (*args, *kwargs), (end - start)*1000))
        return result
    return timed


def create_bases(run_length, gs):
    """Initial conditions for main loop in 'views' """

    # full group size includes one unit buffer
    fgs = gs + 1
    group_number_space = np.array(range(1, int(np.floor((run_length - gs) / fgs) + 1) + 1))

    # loop through all possible number of groups in a base
    for num in group_number_space:
        yield np.array(list(mit.windowed([x for x in range(0, num*fgs) if x not in range(gs, num * fgs, fgs)],
                                         int(gs), step=int(gs))))


def views(run_length):
    """Returns views for all unique run subsets of a run"""

    group_size_space = range(3, run_length + 1)
    if len(group_size_space) == 0:
        yield np.array([0]*run_length)

    for group_size in group_size_space:
        for base in create_bases(run_length, group_size):
            for base_offset in sliding_blocks(base, run_length):
                yield base_offset.flatten()


def sliding_blocks(base, run_length):

    sliding_space_max = run_length - base[-1, -1]
    base_length = len(base)

    if base_length == 1:
        for x in range(sliding_space_max):
            base_new = base.copy()
            base_new[-1] += x
            yield base_new

    elif base_length == 2:
        for y in range(sliding_space_max):
            for x in range(y, sliding_space_max):
                base_new = base.copy()
                base_new[-1] += x
                base_new[-2] += y
                yield base_new

    elif base_length == 3:
        for z in range(sliding_space_max):
            for y in range(z, sliding_space_max):
                for x in range(y, sliding_space_max):
                    base_new = base.copy()
                    base_new[-1] += x
                    base_new[-2] += y
                    base_new[-3] += z
                    yield base_new

    else:
        raise Exception('Unknown base length')
