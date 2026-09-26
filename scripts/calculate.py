"""Reproducible example calculations, not measured or approved hardware ratings."""
from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parents[1]

def led(v, vf, r):
    if r <= 0 or v <= vf:
        raise ValueError('This model requires R > 0 and Vs > Vf.')
    return {'current_mA': 1000*(v-vf)/r, 'resistor_power_mW': 1000*(v-vf)**2/r}

def converter(vin, vout, iout, eta):
    if vin <= 0 or vout < 0 or iout < 0 or not 0 < eta <= 1:
        raise ValueError('Invalid converter operating point.')
    pout=vout*iout
    return {'output_W':pout,'input_A':pout/(eta*vin),'input_W':pout/eta,'loss_W':pout*(1/eta-1)}

def calculate():
    return {
        'status':'Design examples using stated assumptions',
        'assumptions':{'R_ohm':1000,'R_tolerance_percent':5,'green_Vf_V':2.1,'red_Vf_V':2.0,'eta':0.85,'copper_rho_ohm_mm2_per_m':0.0175,'area_mm2':0.75,'one_way_length_m':0.5},
        'green_5V':led(5,2.1,1000),
        'red_PWR_OK_5V_ideal':led(5,2.0,1000),
        'red_PWR_OK_2p4V_ideal':led(2.4,2.0,1000),
        'red_PWR_OK_5V_tolerance_ideal':led(5,1.8,950),
        'pwr_ok_source_test_current_mA':0.2,
        'green_5V_worst_assumed':led(5.25,1.8,950),
        'converter_24V_1A_at_12V':converter(12,24,1,0.85),
        'converter_24V_1A_at_11p4V':converter(11.4,24,1,0.85),
        'converter_15W_at_11p2V':converter(11.2,15,1,0.85),
        'wire_example':{'loop_R_ohm':0.0175*1.0/0.75,'current_A':3,'drop_V':3*0.0175/0.75,'loss_W':9*0.0175/0.75,'drop_percent_on_3p3V':100*3*0.0175/0.75/3.3},
        'dummy_load_example_not_fitted':{'V':5,'R_ohm':10,'current_A':0.5,'power_W':2.5},
    }

def main():
    d=calculate()
    protection=json.loads((ROOT/'hardware/protection-design.json').read_text(encoding='utf8'))
    d['fuse_candidates']=[{'ref':b['ref'],'assumed_continuous_A':b['assumed_continuous_A'],'minimum_preliminary_rating_A':b['assumed_continuous_A']/protection['loading_factor'],'candidate_A':b['candidate_fuse_A']} for b in protection['branches']]
    (ROOT/'docs/calculations.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf8')
    scenarios=[('Green, nominal 5 V','green_5V'),('Red, ideal 5 V signal','red_PWR_OK_5V_ideal'),('Red, ideal 2.4 V signal','red_PWR_OK_2p4V_ideal'),('Red, tolerance example','red_PWR_OK_5V_tolerance_ideal'),('Green, tolerance example','green_5V_worst_assumed')]
    rows=[f"| {label} | {d[key]['current_mA']:.4f} | {d[key]['resistor_power_mW']:.4f} |" for label,key in scenarios]
    c=d['converter_15W_at_11p2V']; w=d['wire_example']
    report="""# Calculation Notes

These examples use the assumptions stated below. The functional test summary is in [Testing](testing.md).

## 1. LED resistors

`I = (Vs − Vf) / R` and `PR = (Vs − Vf)² / R`.

Nominal R = 1 kΩ. Assume Vf = 2.1 V for green and 2.0 V for red. The tolerance examples use R = 950 Ω and Vf = 1.8 V, with 5.25 V for standby and an ideal 5 V for PWR_OK.

| Example | Current (mA) | Resistor power (mW) |
|---|---:|---:|
"""+'\n'.join(rows)+f"""

A 0.25 W resistor has ample power margin in these examples. The red-LED figures assume an ideal signal voltage. Intel specifies PWR_OK high at a 0.2 mA sourcing load; the ideal 5 V example demands 3 mA, or 15 times that condition. Actual LED current depends on the PSU driver and loaded voltage. The 0.2 mA specification is a guaranteed test condition, not an absolute damage limit. [PWR_OK specification](https://edc.intel.com/content/www/ca/fr/design/ipla/software-development-platforms/client/platforms/alder-lake-desktop/atx-version-3-0-multi-rail-desktop-platform-power-supply-design-guide/pwr-ok-required/)

## 2. Converter input and loss

Assume Pout = 15 W and efficiency = 85%.

`Pin = Pout / efficiency = {c['input_W']:.3f} W`

At Vin = 11.2 V, `Iin = Pin / Vin = {c['input_A']:.3f} A`.

At Vin = 12 V, `Iin = 15 / (0.85 × 12) = 1.471 A`.

`Ploss = Pin − Pout = {c['loss_W']:.3f} W`.

These are steady-state examples. Startup current and idle consumption are separate contributions. Usable output also depends on source, wire, module and thermal ratings.

## 3. Wire voltage drop

Assume copper resistivity = 0.0175 Ω·mm²/m at 20 °C, cross-section = 0.75 mm², and length = 0.5 m each way. The total circuit length is 1.0 m.

`Rloop = 0.0175 × 1.0 / 0.75 = {w['loop_R_ohm']:.6f} Ω`

At an assumed 3 A:

- Voltage drop = {w['drop_V']:.3f} V.
- Wire power loss = {w['loss_W']:.3f} W.
- Drop relative to 3.3 V = {w['drop_percent_on_3p3V']:.2f}%.

Contact resistance and fuse resistance add to this result. Wire ampacity also depends on insulation, temperature, routing and termination quality.

## 4. Fixed-output fuse example

Assume a continuous load of 1 A per fixed output and a preliminary loading factor of 75%.

| Branch | Assumed current (A) | I / 0.75 (A) | Calculation candidate (A) |
|---|---:|---:|---:|
"""
    for b in d['fuse_candidates']:
        report+=f"| {b['ref']} | {b['assumed_continuous_A']:.2f} | {b['minimum_preliminary_rating_A']:.3f} | {b['candidate_A']:g} |\n"
    report+="""

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
"""
    (ROOT/'docs/calculations.md').write_text(report,encoding='utf8')
    print('Calculated LED, converter, wire and fuse-selection examples.')

if __name__=='__main__':main()
