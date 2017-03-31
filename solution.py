assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    unitlist_instance = unitlist()
    peers_instance = peers()
    for unit in unitlist_instance:
        temp_buffer = dict((b, values[b]) for b in unit if len(values[b]) == 2)
        twins = []
        for b in temp_buffer:
            for a in temp_buffer:
                if a != b and temp_buffer[a] == temp_buffer[b]:
                    twins.append((a, b))

        #if there is a valid pair of naked twins
        length = len(twins)
        i = 0
        while i < length:
            if len(twins) > 0:
                #print(twins[0])
                a = twins[i][0]
                b = twins[i][1]
                i += 1
                common_peers = find_common_peers(a, b)
                first_char = values[a][:1]
                second_char = values[a][1:]


                #for the values of the peer, eliminate the digits that were represented by the naked twins
                for set_of_peers in common_peers:
                    for p in set_of_peers:
                        if p != a and p != b and len(values[p]) > 1:
                            values[p] = values[p].replace(first_char, '')
                            values[p] = values[p].replace(second_char, '')
        
    return values

def cross(A, B):
    """Cross product of elements in A and elements in B."""
    return [s+t for s in A for t in B]

def row_units():
    """
    Get the row units
    """
    rows = 'ABCDEFGHI'
    cols = '123456789'
    return [cross(r, cols) for r in rows]

def column_units():
    """
    Get the column units
    """
    rows = 'ABCDEFGHI'
    cols = '123456789'
    return [cross(rows, c) for c in cols]

def square_units():
    return [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]


def diagonal_units():
    """
    Get the diagonal units
    """
    rows = 'ABCDEFGHI'
    cols = '123456789'
    diagonal1 = [a[0]+a[1] for a in zip(rows, cols)]
    diagonal2 = [a[0]+a[1] for a in zip(rows, cols[::-1])]
    return [diagonal1, diagonal2]

def unitlist():
    return row_units() + column_units() + diagonal_units() + square_units()

def units():
    """
    units in a dictionary form. Each grid value's may have 3-4 units
    """
    ul = unitlist()
    b = cross('ABCDEFGHI', '123456789')
    return dict((s, [u for u in ul if s in u]) for s in b)

def peers():
    """
    peers of a grid value
    """
    un = units()
    b = cross('ABCDEFGHI', '123456789')
    return dict((s, set(sum(un[s],[]))-set([s])) for s in b)





def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    b = cross('ABCDEFGHI', '123456789')
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(b, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    boxes = cross('ABCDEFGHI', '123456789')
    cols = '123456789'
    rows = 'ABCDEFGHI'
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    boxes = cross('ABCDEFGHI', '123456789')
    peers_instance = peers()

    #for every solved value, remove that digit from the possible choices of its peers
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers_instance[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    unitlist_instance = unitlist()
    for unit in unitlist_instance:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def find_common_peers(a, b):
    """
    find common peers of two boxes, helper method for naked_twins
    """
    temp_holder = []
    units_instance = units()
    for u in units_instance[a]:
        if u in units_instance[b]:
            temp_holder.append(u)
    return temp_holder



def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    boxes = cross('ABCDEFGHI', '123456789')
    values = reduce_puzzle(values)
    if values is False:
        return False 
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
