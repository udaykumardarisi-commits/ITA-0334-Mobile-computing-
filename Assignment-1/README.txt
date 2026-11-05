ITA0334 MOBILE COMPUTING - ASSIGNMENT 1 (TASKS 1-12)

RUNNING THE PROGRAM
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install requirements: pip install numpy matplotlib
4. Run: python cellular_network_project.py
5. The program creates cellular_results/ with a CSV and four PNG graphs.

TASK / EVIDENCE MAPPING
Task 1: Strategy descriptions and pseudocode belong in the written report; no code screenshot required.
Task 2: Explain N, Q, R, channel count and interferer count in the written report.
Task 3: Capture terminal output headed TASK 3 (geometry, capacity and SIR).
Task 4: Capture terminal output headed TASK 4 (Monte Carlo SIR statistics).
Task 5: Insert traffic_growth.png and discuss the growth table.
Task 6: Capture the TASK 6 / 7 recurrence table.
Task 7: Capture the calculated splitting-round line and explain the model assumptions.
Task 8: Capture TASK 8 simulation test matrix and the source-code listing.
Task 9: Insert blocking_comparison.png and sir_cdf.png; include strategy_results.csv as a results table.
Task 10: Capture TASK 10 theory-versus-simulation output.
Task 11: Capture TASK 11 recommendation output and provide your written justification.
Task 12: Capture TASK 12 output and insert stadium_event.png.

MODEL LIMITATIONS - IMPORTANT FOR ACADEMIC HONESTY
This is an educational, simplified simulator, not a commercial RF planning tool.
- Hexagonal coverage is approximated by area and a finite axial-coordinate grid.
- SIR uses six first-tier interferers; the Monte Carlo version samples users in a circular cell.
- Sectorisation is approximated by retaining two interferers; it is not a measured antenna pattern.
- Dynamic pooled assignment is an ideal centralised pooling upper bound, not a full real-time channel-borrowing algorithm.
- Erlang-B assumes a loss system with Poisson arrivals and no waiting queue.
- Cell-splitting capacity scaling is idealised; actual capacity depends on interference, backhaul, site placement and handoff constraints.
- Event cell-equivalent count is a capacity estimate, not an exact physical site count.

SCREENSHOTS
Run the program yourself and capture genuine screenshots of the terminal and generated graphs. Do not submit expected values as if they were screenshots of an actual run.
