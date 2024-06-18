"""
Agent for playing Shogi using a Deep Q-Network (DQN). Handles model initialization,
action selection, memory management, and training using experience replay.
"""

import os

import numpy as np
from shogi import Move
import torch

from services.ai.deep_q_network import DQN
from services.ai.environment import ShogiEnv


class ShogiAgent:
    """
    Agent for playing Shogi using a Deep Q-Network (DQN). Handles model initialization,
    action selection, memory management, and training using experience replay.
    """

    def __init__(self, path: str | None = None):
        """
        Initializes the ShogiAgent with parameters, networks, loss function, and optimizer.
        """
        self.target_network = DQN()
        if path:
            self.get_model(path)

    def mask_and_valid_moves(self, env: ShogiEnv) -> (np.array, dict):
        """
        Get the mask and valid moves for the current player.
        """
        mask = np.zeros((81, 81))
        valid_moves_dict = {}

        legal_moves = env.get_legal_moves()

        for move in legal_moves:
            mask[move.from_square, move.to_square] = 1
            index = 81 * move.from_square + move.to_square
            valid_moves_dict[index] = move

        return mask, valid_moves_dict

    def select_action(self, env: ShogiEnv) -> (Move, int):
        """
        Selects an action using an epsilon-greedy policy.
        """
        valid_moves, valid_move_dict = self.mask_and_valid_moves(env)
        current_state = env.get_observation()

        valid_moves_tensor = torch.from_numpy(valid_moves).float().unsqueeze(0)
        current_state_tensor = torch.from_numpy(current_state).float().unsqueeze(0)
        valid_moves_tensor = valid_moves_tensor.view(current_state_tensor.size(0), -1)
        policy_values = self.target_network(current_state_tensor, valid_moves_tensor)
        chosen_move_index = int(policy_values.max(1)[1].view(1, 1))
        chosen_move = valid_move_dict[chosen_move_index]

        return chosen_move, chosen_move_index

    def get_model(self, path: str):
        """
        Get the model parameters from the specified path.
        """
        if os.path.isfile(path):
            model_dict = torch.load(path)
            self.target_network.load_state_dict(model_dict)
