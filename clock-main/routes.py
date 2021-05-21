from config import app
from views import (
    index
)

app.add_url_rule("/", "index", index, methods=["GET"])