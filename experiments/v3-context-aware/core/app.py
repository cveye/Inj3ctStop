import logging
from flask import Flask, request, render_template_string, jsonify
from core.session_manager import SessionManager
from core.pipeline import ContextAwarePipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("v3-app")

STATUS_ICONS = {"delivered": "✅", "blocked": "❌", "flagged": "🚩"}

HTML = """
<!doctype html>
<html>
<head>
  <title>v3 — Context-Aware Guard</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 30px; }
    textarea { width: 80%; height: 100px; }
    .history { background: #f6f8fa; padding: 12px; border-radius: 8px; margin-bottom: 10px; }
    .result { background: #f9f9f9; padding: 15px; border-radius: 8px; margin-top: 15px; }
    .flagged { color: #d97706; }
    .delivered { color: #16a34a; }
  </style>
</head>
<body>
  <h1>🧠 Context-Aware Injection Detection</h1>

  <form method="post" action="/v3exp">
    <label><input type="checkbox" name="memory" value="on" {% if memory %}checked{% endif %}> Enable memory (last 3 turns)</label><br><br>

    {% if memory and history %}
      <div class="history"><b>Chat history (most recent first):</b><br/>
        {% for h in history|reverse %}
          <div>👤 <b>User:</b> {{ h.user }}</div>
          <div>🤖 <b>Model:</b> {{ h.model }}</div>
          <hr/>
        {% endfor %}
      </div>
    {% endif %}

    <textarea name="prompt" placeholder="Type your prompt...">{{ prompt or '' }}</textarea><br><br>
    <button type="submit">Test</button>
  </form>

  {% if result %}
    <div class="result">
      <h3>Result: <span class="{{ result.final.status }}">{{ icons[result.final.status] }} {{ result.final.status.upper() }}</span></h3>
      {% if result.final.status == "delivered" %}
        <p><b>Response:</b> {{ result.final.response }}</p>
      {% else %}
        <p class="flagged"><b>Reason:</b> {{ result.final.reason }}</p>
      {% endif %}

      <h4>🔎 Layers</h4>
      <ul>
      {% for layer in result.layers %}
        <li>
          <b>{{ layer.layer }}</b> —
          {% if layer.malicious %}
            🚩 flagged ({{ layer.reason }}, sim={{ "%.2f"|format(layer.similarity) }})
          {% else %}
            ✅ clean (sim={{ "%.2f"|format(layer.similarity) }})
          {% endif %}
        </li>
      {% endfor %}
      </ul>
      <small>⏱ {{ result.latency_ms }} ms</small>
    </div>
  {% endif %}
</body>
</html>
"""

app = Flask(__name__)
GLOBAL_SESSION = SessionManager(window=3)  # Demo: single in-memory session

@app.route("/v3exp", methods=["GET", "POST"])
def demo():
    memory = False
    prompt = ""
    result = None

    if request.method == "POST":
        memory = request.form.get("memory") == "on"
        prompt = request.form.get("prompt", "")

        pipeline = ContextAwarePipeline(session=GLOBAL_SESSION if memory else None)
        result = pipeline.run(prompt)

        logger.info("Memory=%s | Prompt=%s | Decision=%s",
                    memory, prompt[:80], result["final"]["status"])

    return render_template_string(
        HTML,
        result=result,
        prompt=prompt,
        memory=memory,
        history=[type("Obj", (), h) for h in GLOBAL_SESSION.history()] if memory else [],
        icons=STATUS_ICONS,
    )

@app.route("/api/check", methods=["POST"])
def api_check():
    memory = request.form.get("memory") == "on"
    prompt = request.form.get("prompt", "")

    pipeline = ContextAwarePipeline(session=GLOBAL_SESSION if memory else None)
    res = pipeline.run(prompt)
    return jsonify(res)

if __name__ == "__main__":
    logger.info("Starting v3 demo at http://0.0.0.0:8080/v3exp")
    app.run(host="0.0.0.0", port=8080, debug=True)