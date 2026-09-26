# Operating Procedure

## Before connection

Confirm the output polarity, closed enclosure, clear ventilation and load rating. Select loads within the source and component ratings. The report's calculation examples do not set a maximum hardware load.

## Startup

1. Remove external loads, set the maintained main switch OFF and disable the adjustable output.
2. Connect meter leads while AC is disconnected. Use insulated clips and a suitable voltage range.
3. Connect AC through the original PSU input. Check standby indication; +5VSB can be live while main outputs are off.
4. Close the PS_ON switch and check the selected fixed output. The red indicator follows gray PWR_OK; green remains on while purple +5VSB is present. An illuminated LED does not replace checking the selected output voltage.
5. Set the adjustable voltage and current limit, then verify the voltage at OUT+/OUT− using a DMM.
6. Disable output before connecting a load. Restore power only with insulated connections and a load within verified branch and combined-source limits.

## During operation

Use the written voltage labels; panel colors differ from ATX wire colors. Fixed rails have no user-adjustable current limit. Keep the adjustable return separate from the fixed COM wiring and avoid unintended earth connections through test equipment. Do not connect different rails in parallel or use the ±12 V rails as a general-purpose 24 V supply.

J8 is a 12 V panel-mount cigarette-lighter power socket with a protective cap for automotive accessories. Its connector shape does not establish a 10 A or 15 A current rating. A lighter heating insert is outside the documented use. The LED strip requires 5 V. Match the fan to its own voltage/current specification and retain the original PSU fan circuit.

Stop for unstable output, unexpected shutdown, damaged insulation, excessive heat or unusual odor. Investigate with AC removed; do not repeatedly cycle a fault or increase the fuse rating.

## Shutdown and fuse replacement

Disable the converter output, open the maintained PS_ON switch, switch off the PSU input and disconnect AC. Wait for stored energy to discharge and verify the relevant low-voltage points before touching wiring. Disconnect loads and allow cooling before storage.

For a blown fuse, identify the cause before replacement. Use the confirmed ampere rating, time characteristic, DC voltage rating, breaking capacity and physical size. Do not bridge the holder. Recheck wiring and polarity before returning the unit to service.
