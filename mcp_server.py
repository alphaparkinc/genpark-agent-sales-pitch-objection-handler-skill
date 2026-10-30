import sys
import json

class SalesPitchEngine:
    OBJECTION_MATRIX = {
        "budget": "Demonstrate 3.8x ROI within 90 days by reducing manual workflow bottlenecks.",
        "security": "Highlight zero third-party Python dependencies, sandbox isolation, and standard library auditability.",
        "migration": "Point out native Model Context Protocol (MCP) compatibility for drop-in zero-downtime adoption.",
        "compliance": "Provide automated audit logging and deterministic schema validation."
    }

    @classmethod
    def generate(cls, industry, pain_point, objections):
        playbook = []
        for obj in objections:
            key = obj.lower().strip()
            answer = cls.OBJECTION_MATRIX.get(key, "Provide tailored proof-of-concept demonstrating rapid feature parity.")
            playbook.append({"objection": obj, "recommended_response": answer})

        return {
            "value_proposition": f"Autonomous productivity platform designed for {industry} organizations facing {pain_point}.",
            "objection_handling_playbook": playbook,
            "call_to_action": "Schedule 15-minute architectural demonstration with sandbox test run."
        }

def handle_rpc(request):
    method = request.get("method")
    req_id = request.get("id")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "generate_sales_pitch",
                        "description": "Generate sales pitch and objection handling matrix.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "industry": {"type": "string"},
                                "pain_point": {"type": "string"},
                                "objections": {"type": "array", "items": {"type": "string"}}
                            },
                            "required": ["industry", "pain_point"]
                        }
                    }
                ]
            }
        }

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "generate_sales_pitch":
            res = SalesPitchEngine.generate(
                args.get("industry", "Enterprise"),
                args.get("pain_point", "Operational latency"),
                args.get("objections", ["budget", "security"])
            )
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res)}]}}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()
