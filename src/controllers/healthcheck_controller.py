from flask_smorest import Blueprint
from controllers import BaseController

blp = Blueprint("Healthcheck", __name__, url_prefix="/healthcheck")


class HealthCheckController(BaseController):
    def __init__(self):
        self.healthcheck_bp = blp
        self.healthcheck_bp.add_url_rule(
            "/", view_func=self.healthcheck_get, methods=["GET"]
        )

    def healthcheck_get(self):
        return """
        <!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>API Online</title>
  <style>
    :root {
      --bg: #f5f7fb;
      --card: #fff;
      --text: #0f172a;
    }

    html,
    body {
      height: 100%;
    }

    body {
      margin: 0;
      font-family: system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial;
      background: var(--bg);
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .container {
      padding: 2rem 3rem;
      background: var(--card);
      border-radius: 16px;
      box-shadow: 0 8px 30px rgba(16, 24, 40, 0.08);
      text-align: center;
      max-width: 90%;
      width: 720px;
    }

    h1 {
      margin: 0 0 .5rem;
      font-size: clamp(1.25rem, 2.5vw, 2rem);
      color: var(--text);
    }

    p {
      margin: 0;
      color: #475569;
    }
  </style>
</head>
<body>
  <main class="container">
    <h1>API is online</h1>
  </main>
</body>
</html>
    """
