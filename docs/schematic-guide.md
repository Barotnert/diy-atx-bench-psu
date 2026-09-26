# Circuit Drawing Guide

[Open the schematic image](images/schematic/diy_atx_psu.svg).

| Section | Circuit |
|---|---|
| A | ATX supply and control signals |
| B | Three fixed outputs, each with a series fuse, and common return |
| C | 12 V cigarette-lighter socket, LED strip and fan |
| D | ZK-4KX, F4 in the output-side model, and adjustable terminals |
| E | PS_ON main switch |
| F | Green standby and red power-good indicators |

Matching net names represent connected wires. J1 pin numbers use the conventional motherboard-side ATX map. F1–F3 identify the fixed-output fuse branches; F4 represents the adjustable-section fuse; fuse-selection calculations are in the report. R1 and R2 are the 1 kΩ LED resistors.

The source and module are represented by their external signals. See the [circuit discussion](design-review.md) for the return paths, PWR_OK loading and branch protection.
