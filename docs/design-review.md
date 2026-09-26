# Circuit Discussion

## Outputs and return paths

The fixed outputs share COM. The adjustable load returns through U1 OUT− so its current follows the module's sensing path. The drawing uses standard ATX signal names and the described wiring arrangement.

## Indicators

Green uses +5VSB through 1 kΩ. Red uses PWR_OK through 1 kΩ. An ideal 5 V red-LED supply with a 2 V forward drop gives 3 mA. Intel specifies the PWR_OK high level at a 0.2 mA sourcing load, so this direct-drive arrangement depends on the PSU's particular driver. The signal's loaded voltage determines the actual LED current. [Intel specification](https://edc.intel.com/content/www/ca/fr/design/ipla/software-development-platforms/client/platforms/alder-lake-desktop/atx-version-3-0-multi-rail-desktop-platform-power-supply-design-guide/pwr-ok-required/)

## Protection

F1–F3 serve the three fixed positive outputs only. The adjustable-section holder is represented by F4 after OUT+ in the circuit model. The converter input, socket and strip connect to PSU outputs; the fan is part of the original PSU assembly. Protection must be coordinated with each branch's wire and components; the main source's protection does not by itself establish protection for every smaller wire. The fuse example uses an assumed 1 A load per fixed branch.

## Conversion losses

The converter input current follows input power. At an assumed 85% efficiency, a 15 W output requires 17.647 W input and produces about 2.647 W loss. Cooling and the combined load on the source therefore affect usable output power.

## Scope of the drawing

The schematic represents low-voltage distribution and control. The PSU and converter are functional blocks. Their internal circuits and mains wiring are outside this drawing. Connector and module symbols describe connectivity; ERC does not model the PWR_OK driver's current capability or fuse-clearing energy.
