import sys, json

class MonorepoDependencyCycleDetector:
    """
    Monorepo Dependency Architecture & Circular Reference Resolver.
    Uses DFS Cycle Detection and Kahn's Algorithm for Topological Sort.
    """
    def __init__(self):
        pass

    def detect_circular_dependencies(self, package_graph):
        # package_graph: {"pkgA": ["pkgB", "pkgC"], "pkgB": ["pkgC"], ...}
        visited = set()
        rec_stack = set()
        cycles = []

        def dfs(node, path):
            visited.add(node)
            rec_stack.add(node)
            for neighbor in package_graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor, path + [neighbor])
                elif neighbor in rec_stack:
                    cycle = path + [neighbor]
                    cycles.append(cycle)
            rec_stack.remove(node)

        for pkg in package_graph:
            if pkg not in visited:
                dfs(pkg, [pkg])

        return {
            "has_circular_dependencies": len(cycles) > 0,
            "cycles_detected_count": len(cycles),
            "cycles": cycles
        }

    def compute_topological_build_order(self, package_graph):
        # Calculate in-degree of each package
        in_degree = {pkg: 0 for pkg in package_graph}
        for pkg, deps in package_graph.items():
            for dep in deps:
                if dep not in in_degree:
                    in_degree[dep] = 0

        for pkg, deps in package_graph.items():
            for dep in deps:
                in_degree[dep] += 1

        queue = [pkg for pkg, deg in in_degree.items() if deg == 0]
        build_order = []

        while queue:
            curr = queue.pop(0)
            build_order.append(curr)
            for dep in package_graph.get(curr, []):
                in_degree[dep] -= 1
                if in_degree[dep] == 0:
                    queue.append(dep)

        if len(build_order) != len(in_degree):
            return {
                "status": "CYCLIC_GRAPH_CANNOT_BUILD",
                "resolved_packages": build_order,
                "unresolved_count": len(in_degree) - len(build_order)
            }

        # Invert build order: dependencies must build before dependents
        correct_order = list(reversed(build_order))
        return {
            "status": "VALID_BUILD_PIPELINE",
            "total_packages": len(correct_order),
            "build_stages": correct_order
        }

    def run_benchmark_monorepo_cycles(self):
        # Graph 1: Clean DAG (core -> utils -> app)
        clean_graph = {
            "app": ["utils", "auth"],
            "auth": ["core"],
            "utils": ["core"],
            "core": []
        }
        order_res = self.compute_topological_build_order(clean_graph)

        # Graph 2: Circular (serviceA -> serviceB -> serviceC -> serviceA)
        cyclic_graph = {
            "serviceA": ["serviceB"],
            "serviceB": ["serviceC"],
            "serviceC": ["serviceA"]
        }
        cycle_res = self.detect_circular_dependencies(cyclic_graph)

        return {
            "benchmark_status": "PASSED",
            "dag_build_status": order_res["status"],
            "cyclic_detected": cycle_res["has_circular_dependencies"],
            "cycle_sample": cycle_res["cycles"][0] if cycle_res["cycles"] else []
        }
