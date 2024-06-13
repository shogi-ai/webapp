"""Repository class to manage games in the database"""

from firebase_admin.firestore import client

from repository.dataclasses.game import Game


class GameRepository:
    """Repository class to manage games in the database"""

    def __init__(self, app: any):
        self.db = client(app)
        self.collection = "games"

    def get(self, uid: str) -> Game | None:
        """Get the game from the database as a Game object"""
        game_ref = self.db.collection(self.collection).document(uid)
        game_doc = game_ref.get()
        if not game_doc.exists:
            return None
        game = Game.from_dict(game_doc.to_dict())
        return game

    def create(self, game: Game) -> None:
        """Add a new game to the database"""
        self.db.collection(self.collection).document(game.uid).set(game.to_dict())

    def update(self, game: Game) -> None:
        """Update the state of the game"""
        self.db.collection(self.collection).document(game.uid).set(game.to_dict())
