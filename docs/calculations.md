# Calculation Notes

These examples use the assumptions stated below. The functional test summary is in [Testing](testing.md).

## 1. LED resistors

`I = (Vs − Vf) / R` and `PR = (Vs − Vf)² / R`.

Nominal R = 1 kΩ. Assume Vf = 2.1 V for green and 2.0 V for red. The tolerance examples use R = 950 Ω and Vf = 1.8 V, with 5.25 V for standby and an ideal 5 V for PWR_OK.

| Example | Current (mA) | Resistor power (mW) |
|---|---:|---:|
| Green, nominal 5 V | 2.9000 | 8.4100 |
| Red, ideal 5 V signal | 3.0000 | 9.0000 |
| Red, ideal 2.4 V signal | 0.4000 | 0.1600 |
| Red, tolerance example | 3.3684 | 10.7789 |
| Green, tolerance example | 3.6316 | 12.5289 |

A 0.25 W resistor has ample power margin in these examples. The red-LED figures assume an ideal signal voltage. Intel specifies PWR_OK high at a 0.2 mA sourcing load; the ideal 5 V example demands 3 mA, or 15 times that condition. Actual LED current depends on the PSU driver and loaded voltage. The 0.2 mA specification is a guaranteed test condition, not an absolute damage limit. [PWR_OK specification](https://edc.intel.com/content/www/ca/fr/design/ipla/software-development-platforms/client/platforms/alder-lake-desktop/atx-version-3-0-multi-rail-desktop-platform-power-supply-design-guide/pwr-ok-required/)

## 2. Converter input and loss

Assume Pout = 15 W and efficiency = 85%.

`Pin = Pout / efficiency = 17.647 W`

At Vin = 11.2 V, `Iin = Pin / Vin = 1.576 A`.

At Vin = 12 V, `Iin = 15 / (0.85 × 12) = 1.471 A`.

`Ploss = Pin − Pout = 2.647 W`.

These are steady-state examples. Startup current and idle consumption are separate contributions. Usable output also depends on source, wire, module and thermal ratings.

## 3. Wire voltage drop

Assume copper resistivity = 0.0175 Ω·mm²/m at 20 °C, cross-section = 0.75 mm², and length = 0.5 m each way. The total circuit length is 1.0 m.

`Rloop = 0.0175 × 1.0 / 0.75 = 0.023333 Ω`

At an assumed 3 A:

- Voltage drop = 0.070 V.
- Wire power loss = 0.210 W.
- Drop relative to 3.3 V = 2.12%.

Contact resistance and fuse resistance add to this result. Wire ampacity also depends on insulation, temperature, routing and termination quality.

## 4. Fixed-output fuse example

Assume a continuous load of 1 A per fixed output and a preliminary loading factor of 75%.

| Branch | Assumed current (A) | I / 0.75 (A) | Calculation candidate (A) |
|---|---:|---:|---:|
| F1 | 1.00 | 1.333 | 2 |
| F2 | 1.00 | 1.333 | 2 |
| F3 | 1.00 | 1.333 | 2 |


The 2 A values belong to this selection example, rather than a fitted-fuse record. The exact part must coordinate with the wire, holder, load, ambient temperature and fault current. See [Wiring and Protection](wiring-and-protection.md).

## 5. Source current budget

`I12 = I12_terminal + Isocket + Iconverter_input`

`I5 = I5_terminal + Istrip`

`I3.3 = I3.3_terminal`

`I5VSB = Igreen_LED + other standby loads`

The original fan belongs to the PSU internal circuit and is outside the external branch-current sum. The red LED loads PWR_OK separately. The common return carries the combined current of its connected branches. Total loading is subject to the PSU's individual-rail and combined-power ratings.

## 6. Useful test formulas

- Load power: `P = V × I`.
- Branch drop: `Vdrop = Vsource − Vterminal`.
- Regulation change: `100 × (Vloaded − Vno-load) / Vno-load`.
- Converter efficiency: `100 × (Vout × Iout) / (Vin × Iin)`.
- Temperature rise: `Thotspot − Tambient`.
