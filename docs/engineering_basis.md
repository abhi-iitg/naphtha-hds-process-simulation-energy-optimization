# Engineering Basis

The feed is a transparent surrogate rather than a refinery assay.

The HDS reactor uses specified conversions. Hydrogen demand is calculated
stoichiometrically. Remaining hydrogen is retained on the product-side basis
so the total mass balance closes.

Heat integration uses constant heat capacities and a minimum terminal
temperature approach. Exchanger area is screened from:

A = Q / (U × LMTD)

with a configured U-value.

Reactor volume is a first-pass LHSV calculation. Pressure drop is a
Darcy-Weisbach line screen, not a packed-bed Ergun calculation. Compressor
power is an ideal-gas isothermal-work screen divided by efficiency.

Fuel and CO2 results are scenario calculations and are not plant economics.

For industrial use, add rigorous thermodynamics/VLE, pseudocomponents,
kinetics, catalyst deactivation, recycle convergence, detailed hydraulics,
exchanger pressure drop, equipment mechanical design, safety studies and
validated cost data.
