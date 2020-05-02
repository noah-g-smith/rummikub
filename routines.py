import numpy as np
import time
from itertools import combinations
import more_itertools as mit

default_tiles = np.array([[1, 1, 1, 1, 2, 1, 1, 0, 0, 1, 1, 1, 0],
                          [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
                          [0, 0, 1, 2, 1, 1, 0, 0, 1, 0, 1, 0, 0],
                          [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 2, 0, 0]])


def timer(f):
    def timed(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()

        print('{}{}: {} ms'.format(f.__name__, (*args, *kwargs), (end - start)*1000))
        return result
    return timed


def view(offset_y, offset_x, shape, step=1):
    """
    Function returning two matching numpy views for moving window routines.
    - 'offset_y' and 'offset_x' refer to the shift in relation to the analysed (central) cell
    - 'shape' are 2 dimensions of the data array (not of the window!)
    - 'view_in' is the shifted view and 'view_out' is the position of central cells
    """
    size_y, size_x = shape
    x, y = abs(offset_x), abs(offset_y)

    x_in = slice(x, size_x, step)
    x_out = slice(0, size_x - x, step)

    y_in = slice(y, size_y, step)
    y_out = slice(0, size_y - y, step)

    # the swapping trick
    if offset_x < 0:
        x_in, x_out = x_out, x_in
    if offset_y < 0:
        y_in, y_out = y_out, y_in

    # return window view (in) and main view (out)
    return np.s_[y_in, x_in], np.s_[y_out, x_out]


@timer
def complements(tiles=default_tiles):
    """Returns possible grouping by suits and/or runs"""

    # map non-zero values to one
    tiles = (tiles != 0)*1

    # suit complements
    column_bool = np.apply_along_axis(np.sum, 0, tiles) >= 3
    suit_bool = np.logical_and(tiles == 1, column_bool)

    # run complements
    run_complements_1 = np.zeros(tiles.shape)
    run_complements_2 = np.zeros(tiles.shape)
    run_complements_3 = np.zeros(tiles.shape)

    # -------- configure window_1 --------
    window_1 = np.array([[1, 1, 1]])

    # loop through window_1
    for (x, y), weight in np.ndenumerate(window_1):
        view_in, view_out = view(x, y - 1, tiles.shape)
        run_complements_1[view_out] += weight * tiles[view_in]

    # -------- configure window_2 --------
    window_2 = np.array([[0, 0, 1, 1, 1]])

    # loop through window_2
    for (x, y), weight in np.ndenumerate(window_2):
        if weight == 0:
            continue
        view_in, view_out = view(x, y - 2, tiles.shape)
        run_complements_2[view_out] += weight * tiles[view_in]

    # -------- configure window_3 --------
    window_3 = np.array([[1, 1, 1, 0, 0]])

    # loop through window_3
    for (x, y), weight in np.ndenumerate(window_3):
        if weight == 0:
            continue
        view_in, view_out = view(x, y - 2, tiles.shape)
        run_complements_3[view_out] += weight * tiles[view_in]

    # -------- boolean selection --------
    bool_select_1 = (run_complements_1 == 3)
    bool_select_2 = (run_complements_2 == 3)
    bool_select_3 = (run_complements_3 == 3)
    run_bool = np.logical_or.reduce((bool_select_1, bool_select_2, bool_select_3))

    return suit_bool, run_bool


@timer
def segments(a, k):
    n = len(a)
    assert 1 <= k <= n, (n, k)

    def split_at(js):
        i = 0

        for j in js:
            yield a[i:j]
            i = j

        yield a[i:]

    for separations in combinations(range(1, n), k - 1):
        yield list(split_at(separations))


@timer
def run_combinations(tiles=default_tiles):
    for row in tiles:
        for k in range(1, len(np.trim_zeros(row))):
            for segmentation in segments(row):
                print(segmentation)


@timer
def trim_to_runs(tiles=default_tiles):
    i = 0
    runs_list = [[], [], [], []]
    remains_list = [[], [], [], []]
    for row in tiles:
        row_numbers = np.where(row >= 1)[0]
        for group_1 in mit.consecutive_groups(row_numbers):
            group_2 = list(group_1)
            if len(group_2) >= 3:
                runs_list[i].append(group_2)
            else:
                remains_list[i].append(group_2)
        i += 1

    return runs_list, remains_list


default_runs_list = [[[0, 1, 2, 3, 4, 5, 6], [9, 10, 11]], [], [[2, 3, 4, 5]], []]
default_run = [0, 1, 2, 3, 4, 5, 6]


def timer(f):
    def timed(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()

        print('{}{}: \n {} ms'.format(f.__name__, (*args, *kwargs), (end - start)*1000))
        return result
    return timed
