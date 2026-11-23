# The report, as submitted

*[← back to the project](../README.md)*

[`variable_pitch_propeller_report_as_submitted.pdf`](variable_pitch_propeller_report_as_submitted.pdf)
is our 39-page report, *Design and Prototype Development of Variable Pitch Propeller*, for the
project-based lab of Aerospace Propulsion (AS343AI), dated 3 July 2025. It is kept exactly as we
handed it in. What it gets wrong is listed below; the rest of this repository is the corrected
account.

## Corrections

| Where | What it says | What is right |
|---|---|---|
| Abstract; Tables 2.2 and 3.1; Sections 3.2, 4.1 and 4.2 | a measured thrust of up to 3.00 N at 28°, a simulated thrust rising smoothly from 0.12 N to 2.20 N, and experiment 10–15 % above simulation | no file in the project supports these numbers. The only bench measurements are the four in Section 2.8 (102–202 g, about 1.0–2.0 N, at 2°–15°), and the CFD estimates jump between −1.6 N and +3.5 N with no trend ([cfd/](../cfd/README.md)). The tables even skip their middle rows with dots |
| Section 2.4.8 | the best pitch is 26–28° in simulation and 24–26° in the tests | the tests went up to 15° |
| Section 2.4.7 | five trials at each pitch angle | we have no record of any trials; the four values in Section 2.8 are the only measurements |
| Section 2.4.4 | each CFD run gave the thrust, the drag and the lift-to-drag ratio | the force goal returned "Invalid" in every run we have a screenshot of; the thrust was worked out afterwards from velocities, and no drag or lift-to-drag ratio was extracted |
| Section 2.4.2 | a three-blade design was selected | three blades was the first hub, in May 2025; the hub we built, the CFD models and the bench have two blades, as Fig. 2.6 shows |
| Sections 2.4.6 and 2.4.10 | a handheld laser tachometer reading reflective tape on the hub, accurate to ±10 RPM | the bench's tachometer is a laser on one post and a receiver on the other, with the blades cutting the beam and an Arduino timing the gaps (Fig. 2.13, Section 2.6, [`FINAL_TACHO`](../bench/firmware/FINAL_TACHO/FINAL_TACHO.ino)); its accuracy was never measured |
| Sections 2.4.9 and 2.4.10, 2.4.12 and 2.4.13 | | the same text, twice each |
| Cover | Rutuj Dugar Manoj | Rutuj Dugad Manoj, as in the certificate and the declaration |
