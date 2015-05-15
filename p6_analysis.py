from p6_game import Simulator

ANALYSIS = {}

def analyze(design):

    global prev_state
    global abil
    prev_state = {}
    abil = {}

    sim = Simulator(design)
    init = sim.get_initial_state()
    moves = sim.get_moves()

    init_pos, init_abil = init
    # a state is a tuple (position, abilities)
    prev_state[init] = None
    abil[init_pos] = [init_abil]

    states = [init]

    for state in states:
        for move in moves:
            next_state = sim.get_next_state(state, move)
            if next_state is None:
                continue
            if next_state == state:
                continue
            if next_state in prev_state:
                continue

            position, abilities = next_state

            prev_state[next_state] = state

            if position in abil:
                duplicate = False
                for abil_set in abil[position]:
                    if not abil_set.symmetric_difference(abilities):
                        duplicate = True
                if not duplicate:
                    # if this ability set is novel for this position,
                    # add it to the list of ability sets at this position,
                    # and add this new state to the state list,
                    # otherwise, discard this state
                    abil[position].append(abilities)
                    states.append(next_state)
            else:
                # if this position has never been reached,
                # enter it into the abilities-by-position table,
                # and add this new state to the state list.
                abil[position] = [abilities]
                states.append(next_state)

    debug = "an assignment to break on"

def inspect((i,j), draw_line):

    print ""
    if (i,j) in abil:
        abilities = abil[(i,j)]
        for abil_set in abilities:
            state = ((i,j), abil_set)
            pos1 = (i,j)
            while prev_state[state] is not None:
                state = prev_state[state]
                pos2,_abs = state
                draw_line(pos1, pos2, abil_set, abil_set)
                pos1 = pos2

        print "("+str(i)+","+str(j)+"): " + str(abil[(i,j)])
    else:
        print "("+str(i)+","+str(j)+"): " + "unreachable"