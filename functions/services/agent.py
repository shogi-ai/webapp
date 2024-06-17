import torch
import os
import numpy as np
from services.board import ShogiBoard

class ShogiAgent:

    def __init__(self, model_path: str):
        if os.path.isfile(model_path):
            model_dict = torch.load(model_path)
            self.target_network = self.target_network.load_state_dict(model_dict)
            self.q_network = self.q_network.load_state_dict(model_dict)

    def mask_and_valid_moves(self, board: ShogiBoard):
        """
        Get the mask and valid moves for the current player.

        Returns:
            tuple: Tuple containing the mask and valid moves for the current player.
        """
        mask = np.zeros((88, 81))
        valid_moves_dict = {}

        legal_moves = board.get_legal_moves()

        for move in legal_moves:
            mask[self.get_from_square(move), move.to_square] = 1
            valid_moves_dict[self.get_move_index(move)] = move

        return mask, valid_moves_dict

    def select_best_action(self, board: ShogiBoard):
        """
        Selects the best action using the target network.

        Args:
            env: Environment object with mask_and_valid_moves and get_state methods.

        Returns:
            tuple: Move index, chosen move, current state, valid moves.
        """
        valid_moves, valid_move_dict = self.mask_and_valid_moves(board)
        current_state = board.get_observation()

        valid_moves_tensor = torch.from_numpy(valid_moves).float().unsqueeze(0)
        current_state_tensor = torch.from_numpy(current_state).float().unsqueeze(0)
        valid_moves_tensor = valid_moves_tensor.view(
            current_state_tensor.size(0), -1
        )
        policy_values = self.target_network(
            current_state_tensor, valid_moves_tensor
        )
        chosen_move_index = int(policy_values.max(1)[1].view(1, 1))
        try:
            chosen_move = valid_move_dict[chosen_move_index]
        except Exception:
            chosen_move = board.sample_action()
            chosen_move_index = 81 * self.get_from_square(chosen_move) + chosen_move.to_square

        return chosen_move, chosen_move_index