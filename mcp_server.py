import sys, json
from client import MonorepoDependencyCycleDetector

def main():
    detector = MonorepoDependencyCycleDetector()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(detector.run_benchmark_monorepo_cycles(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            rid = req.get("id")

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "detect_circular_dependencies", "description": "Detect dependency loops in monorepo packages."},
                        {"name": "compute_topological_build_order", "description": "Compute valid build execution order."},
                        {"name": "run_benchmark_monorepo_cycles", "description": "Run monorepo cycle benchmark."}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "detect_circular_dependencies":
                    out = detector.detect_circular_dependencies(args.get("package_graph", {}))
                elif tname == "compute_topological_build_order":
                    out = detector.compute_topological_build_order(args.get("package_graph", {}))
                elif tname == "run_benchmark_monorepo_cycles":
                    out = detector.run_benchmark_monorepo_cycles()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
