from firebase_admin.firestore import client

from repository.dataclasses.game import Game


class GameReposiory:
    def __init__(self, app: any):
        self.db = client(app)
        self.collection = "games"

    def get(self, uid: str) -> dict | None:
        game_ref = self.db.collection(self.collection).document(uid)
        game_doc = game_ref.get()
        if not game_doc.exists:
            return None
        return game_doc.to_dict()

    def create(self, game: Game) -> None:
        self.db.collection(self.collection).document(game.uid).set(game.to_dict())
