import sys, json
from client import MonorepoDependencyCycleDetector

def main():
    print("Testing MonorepoDependencyCycleDetector...")
    detector = MonorepoDependencyCycleDetector()
    res = detector.run_benchmark_monorepo_cycles()
    print(json.dumps(res, indent=2))
    assert res["benchmark_status"] == "PASSED"
    assert res["dag_build_status"] == "VALID_BUILD_PIPELINE"
    assert res["cyclic_detected"] is True
    print("All Monorepo Dependency Cycle Detector tests passed successfully!")

if __name__ == "__main__":
    main()
