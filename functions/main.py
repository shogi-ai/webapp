"""
Welcome to Cloud Functions for Firebase for Python!
To get started, simply uncomment the below code or create your own.
Deploy with `firebase deploy
"""

from firebase_functions.https_fn import Request, Response, on_request
from firebase_admin import initialize_app

initialize_app()


@on_request()
def on_request_example(req: Request) -> Response:
    """Test endpoint"""
    print(req.data)
    return Response("Hello world!")
