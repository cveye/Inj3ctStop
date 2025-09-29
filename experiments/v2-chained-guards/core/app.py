import logging
from flask import Flask, request, render_template_string, jsonify
from pipeline import ChainedGuardsPipeline

# --------------------------------
# Logging setup (like v1)
# --------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("v2-app")

# --------------------------------
# Flask setup
# --------------------------------
app = Flask(__name__)

DEMO_HTML = """
<!doctype html>
<title>v2 — Chained Guards Demo</title>
<h1>Chained Guards Demo</h1>
<form method=post action="/api/check">
  <textarea name=prompt rows=6 cols=80 placeholder="Type an input to test..."></textarea><br>
  <label>Layers (comma separated):</label>
  <input name=layers value="prefilter,embedding_check,llm_self_check,sandbox_postprocess" size=60><br>
  <button type=submit>Test</button>
</form>
<pre id=result></pre>
<script>
const form = document.querySelector('form');
form.onsubmit = async (e) => {
  e.preventDefault();
  const data = new FormData(form);
  const resp = await fetch('/api/check', {method: 'POST', body: data});
  const json = await resp.json();
  document.getElementById('result').textContent = JSON.stringify(json, null, 2);
}
</script>
"""

# Default pipeline with all guards
pipeline = ChainedGuardsPipeline()


@app.route("/demo")
def demo():
    return render_template_string(DEMO_HTML)


@app.route("/api/check", methods=["POST"])
def api_check():
    prompt = request.form.get("prompt", "")
    layers = request.form.get("layers", "")
    layers_list = [l.strip() for l in layers.split(",") if l.strip()] or None

    logger.info("Received prompt: %s", prompt[:80] + ("..." if len(prompt) > 80 else ""))
    if layers_list:
        logger.info("Using layers: %s", layers_list)
    else:
        logger.info("Using default layers")

    pipeline_instance = ChainedGuardsPipeline(layers=layers_list)
    res = pipeline_instance.run(prompt)

    # Log final decision
    final_status = res["final"]["status"]
    logger.info("Final decision: %s | latency=%dms", final_status, res["latency_ms"])

    return jsonify(res)


if __name__ == "__main__":
    logger.info("Starting v2 Chained Guards Flask app on http://0.0.0.0:8080/demo")
    app.run(host="0.0.0.0", port=8080, debug=True)