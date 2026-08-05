"""
Triggers code-exec-tool-without-sandbox: a custom agent tool posts the model's
generated code to an internal "compute" microservice endpoint that itself just
calls exec() on the request body with no isolation -- the sandboxing gap is
one hop away but still fully within the agent's own tool-execution path.
"""
from langchain.tools import Tool
import requests


def run_in_compute_service(code: str) -> str:
    resp = requests.post("http://compute-internal:9000/run", json={"code": code})
    return resp.json()["output"]


# compute-internal's /run handler (same repo, same trust boundary):
#     @app.route("/run", methods=["POST"])
#     def run():
#         result = {}
#         exec(request.json["code"], {}, result)   # <-- unsandboxed sink
#         return jsonify(output=result)

run_code_tool = Tool.from_function(
    func=run_in_compute_service,
    name="run_code",
    description="Run Python code on the compute cluster and return its output.",
)
