from app.ai.router import CommandRouter


def test_open_app_command():
    router = CommandRouter()
    intent = router.route("Open Chrome")
    assert intent.action == "open_app"
    assert intent.target.lower() in {"chrome", "google chrome"}


def test_search_command():
    router = CommandRouter()
    intent = router.route("Search Google for Python tutorials")
    assert intent.action == "search_web"


def test_time_command():
    router = CommandRouter()
    intent = router.route("What time is it?")
    assert intent.action == "tell_time"


def test_ask_user_fallback():
    router = CommandRouter()
    intent = router.route("Do something mysterious")
    assert intent.action == "ask_user"
