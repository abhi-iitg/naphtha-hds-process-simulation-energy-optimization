# Validation Log

The release test suite checks:
1. feed closure;
2. total mass balance;
3. elemental sulfur balance;
4. hydrogen stoichiometry;
5. sulfur specification;
6. heat-recovery and approach constraints;
7. positive LMTD and exchanger area;
8. reactor-volume screen;
9. pressure-drop screen;
10. compressor-power screen;
11. optimization feasibility;
12. deterministic repeatability;
13. deliberate low-conversion specification failure;
14. deliberate infeasible-temperature rejection.

Run:

`python -m pytest -q`

Expected:

`14 passed`

Then:

`python -m src.reporting`
