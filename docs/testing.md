# Functional Test Summary

The table records the team's reported test outcomes for the completed prototype. It is a qualitative pass/fail summary; the calculations in this report are theoretical examples.

| Check | Result |
|---|---|
| Unpowered wiring, polarity and continuity | PASS |
| PS_ON switching and standby/main indication | PASS |
| Startup, repeated-start and no-load operation | PASS |
| Fixed-output operation under load | PASS |
| Adjustable-output operation and current-limit check | PASS |
| Voltage-drop check | PASS |
| Ripple check | PASS |
| Thermal observation | PASS |
| Socket, fan and LED strip operation | PASS |
| Shutdown | PASS |

## Test scope

The checks cover the assembled 12 V, 5 V and 3.3 V outputs, adjustable output, controls and accessories. PASS describes the reported outcome of each check rather than a numerical maximum rating or full ATX compliance result.

The direct PWR_OK LED connection has the signal-loading limitation discussed in the [circuit discussion](design-review.md). Functional indication and signal-drive margin are different quantities. Fuse selection is analysed separately in the [calculation notes](calculations.md).

## Drawing checks

KiCad ERC and netlist checks cover the drawing's connections, including the three fixed-output fuses, LED polarity, PS_ON switch and separate adjustable return. These software checks concern the schematic. The prototype results above come from the team.
