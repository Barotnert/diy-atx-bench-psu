# Wiring and Protection

## Standard ATX signal map

The table follows course handout Section 3.4.1. Pin numbers refer to the motherboard-side 24-pin connector. The project uses these names as a logical signal reference for the PSU board connections.

| Pin | Signal | Conventional color | Pin | Signal | Conventional color |
|---:|---|---|---:|---|---|
| 1 | +3.3 V | Orange | 13 | +3.3 V / optional sense | Orange / brown sense |
| 2 | +3.3 V | Orange | 14 | −12 V | Blue |
| 3 | COM | Black | 15 | COM | Black |
| 4 | +5 V | Red | 16 | PS_ON active low | Green |
| 5 | COM | Black | 17 | COM | Black |
| 6 | +5 V | Red | 18 | COM | Black |
| 7 | COM | Black | 19 | COM | Black |
| 8 | PWR_OK logic | Gray | 20 | Reserved / NC | None |
| 9 | +5VSB | Purple | 21 | +5 V | Red |
| 10 | +12 V | Yellow | 22 | +5 V | Red |
| 11 | +12 V | Yellow | 23 | +5 V | Red |
| 12 | +3.3 V | Orange | 24 | COM | Black |

Pin 20 follows the handout's logical table: reserved / no connection. Original sense connections remain part of the source circuit. Connector mating-face and wire-entry views are mirrored, so the logical table is not a physical connector-view drawing.

## Project connections

| Source | Destination |
|---|---|
| +12 V | F1 → red fixed terminal; direct feeds to ZK-4KX and J8 socket |
| +5 V | F2 → yellow fixed terminal; LED strip |
| +3.3 V | F3 → green fixed terminal |
| COM | Black terminal and supply returns |
| Purple +5VSB | R1 → green LED → COM |
| Gray PWR_OK | R2 → red LED → COM |
| Green PS_ON | Main switch → COM |
| U1 OUT+ | F4 → adjustable positive terminal in the circuit model |
| U1 OUT− | Adjustable negative terminal |

The original fan remains within the PSU assembly. F1–F3 serve the fixed outputs. The adjustable-section holder is represented as F4 between OUT+ and the positive terminal. The socket, strip and indicators have no separate external branch fuse in this arrangement.

## Fuse calculation basis

For the example 1 A continuous load on each fixed output, a preliminary 75% loading factor gives `1 / 0.75 = 1.33 A`. A 2 A component is a candidate within that example. This calculation is separate from the fitted component record.

The final selection depends on the exact fuse's time-current curve, DC voltage and breaking ratings, ambient temperature, inrush and protected wire. Fuse rating is not an adjustable current limit. Place the fuse in the positive branch, with the common return continuous. [Littelfuse selection guide](https://www.littelfuse.com/assetdocs/fuseology-selection-guide?assetguid=fa4aa360-f6c4-4eec-88a6-3d7ec3fe57d5)

## Control and return paths

PWR_OK is a status signal, while PS_ON is an input control. The standby supply can remain active when the main switch is off. The adjustable output returns to U1 OUT−; the fixed outputs use COM. A shared COM wire carries the total return current from its connected loads.


[PLENTY ATX500WS source ratings](source-psu.md)
