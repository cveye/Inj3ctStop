import logging
from flask import Flask, request, render_template_string, jsonify
from pipeline import ChainedGuardsPipeline

# Logging setup (just like you had in v1 / v2)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("v2-app")

# Map status to icon
STATUS_ICONS = {
    "delivered": "✅",
    "blocked": "❌",
    "flagged": "🚩"
}

# The simple HTML template with inline CSS + logic
HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>v2 — Chained Guards - LLM defence</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 30px; }
    textarea { width: 80%; height: 100px; }
    .result { margin-top: 20px; padding: 15px; border-radius: 8px; background: #f9f9f9; }
    .layer { margin: 5px 0; }
    .blocked { color: red; }
    .flagged { color: orange; }
    .delivered { color: green; }
    ul { list-style: none; padding-left: 0; }
  </style>
</head>
<body>
  <h1>🛡️ Chained Guards - LLM defence</h1>
  <form method="post" action="/api/check">
  <textarea name="prompt" placeholder="Type a prompt…">{{ request.form.get('prompt','') }}</textarea><br><br>

  <label><b>Choose Guardrails:</b></label><br>
  {% set selected_layers = request.form.getlist('layers') %}
  <input type="checkbox" name="layers" value="prefilter"
    {% if 'prefilter' in selected_layers or not selected_layers %}checked{% endif %}> Prefilter (regex)<br>
  <input type="checkbox" name="layers" value="embedding_check"
    {% if 'embedding_check' in selected_layers or not selected_layers %}checked{% endif %}> Embedding Check<br>
  <input type="checkbox" name="layers" value="llm_self_check"
    {% if 'llm_self_check' in selected_layers or not selected_layers %}checked{% endif %}> LLM Self-Check<br>
  <input type="checkbox" name="layers" value="sandbox_postprocess"
    {% if 'sandbox_postprocess' in selected_layers or not selected_layers %}checked{% endif %}> Sandbox Post-Process<br><br>

  <button type="submit">Test</button>
</form>

  {% if result %}
    <div class="result">
      <h2>
        Result:
        <span class="{{ result.final.status }}">
          {{ status_icons.get(result.final.status, "") }} {{ result.final.status.upper() }}
        </span>
      </h2>
      {% if result.final.status == "delivered" %}
        <p><b>Response:</b> {{ result.final.response }}</p>
      {% else %}
        <p><b>Reason:</b> {{ result.final.reason }}</p>
      {% endif %}

      <h3>🔍 Layers</h3>
      <ul>
      {% for layer in result.layers %}
        <li class="layer">
          <b>{{ layer.layer }}</b>:
          {% if layer.malicious %}
            🚩 <span class="flagged">
              flagged {% if layer.reason %}({{ layer.reason }}){% elif layer.explanation %}({{ layer.explanation }}){% elif layer.sim is not none %}({{ layer.sim }}){% endif %}
            </span>
          {% else %}
            ✅ <span class="delivered">clean</span>
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
default_pipeline = ChainedGuardsPipeline()

@app.route("/demo", methods=["GET"])
def demo():
    return render_template_string(HTML_TEMPLATE, result=None, status_icons=STATUS_ICONS)

@app.route("/api/check", methods=["POST"])
def api_check():
    prompt = request.form.get("prompt", "")
    layers_list = request.form.getlist("layers")
    if not layers_list:  # if user leaves all unchecked
        layers_list = None

    logger.info("Prompt: %s", prompt.replace("\n", " ")[:100])
    logger.info("Layers: %s", layers_list or "default")

    pipeline = ChainedGuardsPipeline(layers=layers_list)
    res = pipeline.run(prompt)

    status = res["final"].get("status")
    logger.info("Decision: %s, latency: %dms", status, res.get("latency_ms", -1))

    return render_template_string(HTML_TEMPLATE, result=res, status_icons=STATUS_ICONS)

if __name__ == "__main__":
    logger.info("Starting Chained Guards Demo on http://0.0.0.0:8080/demo")
    app.run(host="0.0.0.0", port=8080, debug=True)