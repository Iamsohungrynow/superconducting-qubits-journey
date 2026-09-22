"""Run labs in separate processes and verify independent physics identities.

python hands-on/run_labs.py --list
python hands-on/run_labs.py --all --check
python hands-on/run_labs.py 09 10 --check
Without --check, plots open interactively; close each window to continue.
"""
import argparse
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def labs():
    return {p.parent.name[:2]: p for p in sorted(ROOT.glob("[0-9][0-9]-*/*.py"))}


def verify(key, v):
    import numpy as np
    close = np.testing.assert_allclose
    if key == "01":
        close(v["xs"], 0, atol=1e-5)
        close(v["ys"], -np.sin(v["Omega"]*v["tlist"]), atol=1e-4)
        close(v["zs"], np.cos(v["Omega"]*v["tlist"]), atol=1e-4)
    elif key == "02":
        close(v["P1"], np.sin(v["Omega"]*v["tlist"]/2)**2, atol=1e-4)
    elif key == "03":
        close(v["P1"], np.exp(-v["t1_times"]/v["T1"]), atol=1e-5)
        close(v["Sx"], np.exp(-v["t2_times"]/v["T2_pred"])*np.cos(v["detuning"]*v["t2_times"]), atol=1e-4)
        close(v["T2_fit"], v["T2_pred"], rtol=.003)
    elif key == "04":
        for z, name, trajectory in [(1, "ss_g", "a_g"), (-1, "ss_e", "a_e")]:
            rate = v["kappa"]/2 + 1j*(v["delta"]-z*v["chi"])
            steady = -1j*v["drive"]/rate
            close(v[name], steady, atol=1e-5)
            close(v[trajectory], steady*(1-np.exp(-rate*v["tlist"])), atol=1e-4)
    elif key == "05":
        for _, p0, p1, p2 in v["results"].values():
            close(p0+p1+p2, 1, atol=1e-6)
        assert v["results"]["DRAG"][3][-1] < v["results"]["no DRAG"][3][-1]/100
        # Tiny leakage is not the same as a calibrated X gate.
        assert v["results"]["DRAG"][2][-1] < .999
    elif key == "06":
        from scipy.linalg import expm
        exact = expm(-1j*v["H_res"].full()*v["t_cz"])
        for ij, ket in v["comp"].items():
            numerical = v["states"][ij][v["k_cz"]].full().ravel()
            target = exact @ ket.full().ravel()
            assert abs(np.vdot(numerical, target))**2 > 1-1e-6
        close(v["gap"].min(), v["gap_theory"], rtol=.005)
        assert .98 < v["P11"][v["k_cz"]] < 1
    elif key == "07":
        close(v["means"], .5+.5*v["p_theory"]**(v["lengths"]+1), atol=1e-10)
        close(v["p_fit"], v["p_theory"], atol=1e-6)
        for c in v["cliffords"]:
            close(c.conj().T@c, np.eye(2), atol=1e-12)
    elif key == "08":
        p = np.linspace(0, 1, 101)
        close(v["logical_error_analytic"](3, p), 3*p*p-2*p**3, atol=1e-14)
        for d, samples in v["mc_curves"].items():
            expected = v["logical_error_analytic"](d, v["p_grid_mc"])
            stderr = np.sqrt(expected*(1-expected)/v["n_shots"])
            assert np.all(np.abs(samples-expected) < 7*stderr+5/v["n_shots"])
    else:
        assert v.get("metrics"), "New labs must return checked metrics"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lab", nargs="*", help="Two-digit lab numbers")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--check", action="store_true", help="Headless execution with physics checks")
    parser.add_argument("--worker", help=argparse.SUPPRESS)
    args = parser.parse_args()
    available = labs()
    if args.worker:
        os.environ["MPLBACKEND"] = "Agg"
        import matplotlib.pyplot as plt
        plt.show = lambda: None
        values = runpy.run_path(str(available[args.worker]), run_name="__main__")
        verify(args.worker, values)
        print("PASS: numerical physics checks")
        return
    if args.list:
        for key, path in available.items():
            print(f"{key}: {path.relative_to(ROOT)}")
        return
    selected = list(available) if args.all else args.lab
    if not selected or any(key not in available for key in selected):
        parser.error("Choose valid lab numbers (see --list) or --all")
    report = []
    for key in selected:
        start = time.monotonic()
        cmd = [sys.executable, str(Path(__file__).resolve()), "--worker", key] if args.check else [sys.executable, str(available[key])]
        print(f"\nRunning {available[key].parent.name}", flush=True)
        try:
            result = subprocess.run(cmd, cwd=ROOT.parent, capture_output=args.check,
                                    text=True, timeout=300 if args.check else None)
            if args.check:
                print(result.stdout, end="")
                if result.stderr:
                    print(result.stderr, file=sys.stderr, end="")
            entry = {"lab": key, "passed": result.returncode == 0,
                     "seconds": round(time.monotonic()-start, 2)}
        except subprocess.TimeoutExpired:
            entry = {"lab": key, "passed": False, "error": "Timed out after 300 seconds"}
        report.append(entry)
    if args.check:
        import importlib.metadata
        versions = {name: importlib.metadata.version(name) for name in ("numpy", "scipy", "matplotlib", "qutip")}
        (ROOT / "run-report.json").write_text(json.dumps({"python": sys.version, "dependencies": versions, "results": report}, indent=2), encoding="utf-8")
    failures = sum(not item["passed"] for item in report)
    print(f"\n{len(report)-failures}/{len(report)} labs passed")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
