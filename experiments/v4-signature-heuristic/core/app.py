from __future__ import annotations
import logging
from flask import Flask, request, render_template_string, jsonify
from core.pipeline import SignatureHeuristicPipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log = logging.getLogger("v4-app")

STATUS_ICON = {"delivered": "✅", "flagged": "🚩"}

HTML = """
<!doctype html>
<html>
<head>
  <title>v4 — Signature + Heuristic Engine</title>
  <style>
    body { font-family: Inter, Arial, sans-serif; margin: 30px; }
    textarea { width: 80%; height: 110px; }
    .row { margin: 10px 0; }
    .result { background: #f7f7f8; padding: 16px; border-radius: 10px; margin-top: 16px; }
    .meter { height: 14px; width: 320px; background: #e5e7eb; border-radius: 9999px; overflow: hidden; display:inline-block; vertical-align:middle; }
    .bar { height: 100%; }
    .green { background: #10b981; }
    .yellow { background: #f59e0b; }
    .red { background: #ef4444; }
    .badge { display:inline-block; padding:2px 8px; border-radius:12px; font-size:12px; margin-left:8px; }
    .ok { background:#e6fffa; color:#0f766e; }
    .flag { background:#fff1f2; color:#be123c; }
    ul { line-height:1.5; }
    code { background:#eef2ff; padding:2px 4px; border-radius:6px; }
  </style>
</head>
<body>
  <h1>🛡️ v4 — Signature + Heuristic Engine</h1>
  <form method="post" action="/demo">
    <div class="row">
      <textarea name="prompt" placeholder="Type a prompt to test...">{{ prompt or '' }}</textarea>
    </div>
    <div class="row">
      <button type="submit">Analyze</button>
    </div>
  </form>

  {% if result %}
    <div class="result">
      {% set risk = result.risk %}
      {% set pct = (risk * 100) | round(1) %}
      {% set color = 'green' if risk < 0.3 else ('yellow' if risk < 0.7 else 'red') %}
      <h3>
        Decision: {{ status_icon[result.final.status] }} {{ result.final.status.upper() }}
        {% if result.final.status == 'delivered' %}
          <span class="badge ok">ok</span>
        {% else %}
          <span class="badge flag">high_risk</span>
        {% endif %}
      </h3>
      <div>Threat score:
        <div class="meter"><div class="bar {{ color }}" style="width: {{ pct }}%"></div></div>
        <strong>{{ pct }}%</strong>
      </div>

      <h4>Layers</h4>
      <ul>
        {% for layer in result.layers %}
          <li>
            <b>{{ layer.layer }}</b> — risk: {{ "%.2f"|format(layer.risk) }}
            {% if layer.layer == 'signature_guard' and layer.details.matches %}
              <div>Matches:
                <ul>
                  {% for m in layer.details.matches %}
                    <li><code>{{ m.id }}</code> ({{ m.category }}) × {{ m.count }}, sev={{ "%.2f"|format(m.severity) }}</li>
                  {% endfor %}
                </ul>
              </div>
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
pipeline = SignatureHeuristicPipeline()

@app.route("/demo", methods=["GET", "POST"])
def demo():
    prompt = ""
    result = None
    if request.method == "POST":
        prompt = request.form.get("prompt", "")
        result = pipeline.run(prompt)
        log.info("Prompt=%s | risk=%.3f | decision=%s",
                 prompt[:120].replace("\n"," "),
                 result["risk"],
                 result["final"]["status"])
    return render_template_string(HTML, result=result, prompt=prompt, status_icon=STATUS_ICON)

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    prompt = request.form.get("prompt", "")
    res = pipeline.run(prompt)
    return jsonify(res)

if __name__ == "__main__":
    log.info("Starting v4 demo at http://0.0.0.0:8080/demo")
    app.run(host="0.0.0.0", port=8080, debug=True)