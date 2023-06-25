import numpy as np 


board = np.zeros((4,5), dtype=int)

# board is 5 in x, 4 in y
# 0,0 -> 0,5
# |
# \/
# 4,0

# there are 4 1x1 yellow blocks
# there is 1 2x1 black block
# there is 3 1x2 black blocks
# there is 1 2x2 red block 
# blocks are 

class Block:
    shape: tuple #(w,h)
    location: np.ndarray #(i,j), top left corner
    id: int 

    def __init__(self, shape, location, board:np.ndarray, id:int):
        self.shape = shape
        self.location = location
        self.id = id
        board[location[0]:location[0]+shape[0], location[1]:location[1]+shape[1]] = id

    def check_move(self, board, shift:np.ndarray):
        # check if move is valid (one space away)
        if np.sum(np.abs(shift)) != 1:
            return False
        # check if new location is in bounds
        new_location = self.location + shift
        if new_location[0] < 0 or new_location[0] + self.shape[0] > board.shape[0]:
            return False
        if new_location[1] < 0 or new_location[1] + self.shape[1] > board.shape[1]:
            return False
        # check if new location is empty
        new_board_slice = board[new_location[0]:new_location[0]+self.shape[0], new_location[1]:new_location[1]+self.shape[1]]
        # if anything in board slice is not 0 or self.id, return false
        if np.any((new_board_slice != 0) & (new_board_slice != self.id)):
            return False
        return True

    def move(self, board, shift:np.ndarray):
        # if valid, move
        if not self.check_move(board, shift):
            return False
        new_location = self.location + shift
        new_board_slice = board[new_location[0]:new_location[0]+self.shape[0], new_location[1]:new_location[1]+self.shape[1]]
        old_board_slice = board[self.location[0]:self.location[0]+self.shape[0], self.location[1]:self.location[1]+self.shape[1]]

        old_board_slice[:,:] = 0
        new_board_slice[:,:] = self.id
        self.location = new_location
        return True

class Board:
    pieces:dict[int, Block]
    state: np.ndarray

    def __init__(self):
        board = np.zeros((4,5), dtype=int)
        red = Block((2,2), np.array([1,3]), board, 1)
        black1 = Block((1,2), np.array([0,3]), board, 2)
        black2 = Block((1,2), np.array([3,3]), board, 3)
        black3 = Block((1,2), np.array([0,1]), board, 4)
        black4 = Block((1,2), np.array([3,1]), board, 5)
        black5 = Block((2,1), np.array([1,2]), board, 6)
        yellow1 = Block((1,1), np.array([1,0]), board, 7)
        yellow2 = Block((1,1), np.array([2,0]), board, 8)
        yellow3 = Block((1,1), np.array([1,1]), board, 9)
        yellow4 = Block((1,1), np.array([2,1]), board, 10)
        self.pieces = {1:red, 2:black1, 3:black2, 4:black3, 5:black4, 6:black5, 7:yellow1, 8:yellow2, 9:yellow3, 10:yellow4}
        self.state = board
    
    def print_state(self):
        print(self.state)

    def find_proposal_moves(self):
        # find the zeros in the board
        zero_indices = np.argwhere(self.state == 0)
        assert zero_indices.shape[0] == 2
        neighbor_shifts = np.array([[0,1],[0,-1],[1,0],[-1,0]])
        zero_1_neighbors = zero_indices[0] + neighbor_shifts
        zero_2_neighbors = zero_indices[1] + neighbor_shifts
        final_neighbors, neighbor_indicies = np.unique(np.concatenate([zero_1_neighbors, zero_2_neighbors], axis=0), axis=0, return_index=True)
        final_shifts = np.concatenate([neighbor_shifts, neighbor_shifts], axis=0)[neighbor_indicies,:]
        # remove out of bounds
        valid_trims = (final_neighbors[:,0] >= 0) & (final_neighbors[:,0] < self.state.shape[0]) & \
                            (final_neighbors[:,1] >= 0) & (final_neighbors[:,1] < self.state.shape[1])
        final_neighbors = final_neighbors[valid_trims, :]
        final_shifts = final_shifts[valid_trims, :]
        final_piece_ids = self.state[final_neighbors[:,0], final_neighbors[:,1]]
        move_proposals = []
        for i in range(final_piece_ids.shape[0]):
            if final_piece_ids[i] != 0:
                move_proposals.append((final_piece_ids[i], -1 * final_shifts[i])) # -1 since we are moving the piece, not the zero
        return move_proposals
    
    def check_win(self):
        return self.state[1,0] == 1 # the red block is ready to leave




def find_solution(board:Board):

    unique_states = dict()
    while True:
        # find proposal moves
        proposal_moves = board.find_proposal_moves()
        # pick a random move
        move = proposal_moves[np.random.randint(len(proposal_moves))]
        # execute 
        board.pieces[move[0]].move(board.state, move[1])
        # check if we have seen this state before
        # if str(board.state) not in unique_states: # new state, keep going
        #     unique_states[str(board.state)] = 1
        # else:
        #     # we have seen this state before, undo the move
        #     # board.pieces[move[0]].move(board.state, -1 * move[1])
        #     continue
        board.print_state()
        # check if win
        if board.check_win():
            return board



if __name__ == "__main__":
    b = Board()
    b.print_state()
    # valid_moves = b.find_proposal_moves()
    # print(valid_moves)
    # make the first move 
    # move = valid_moves[3]
    # b.pieces[move[0]].move(b.state, move[1])
    # b.print_state()
    final_board = find_solution(b)
    print("final board")
    final_board.print_state()