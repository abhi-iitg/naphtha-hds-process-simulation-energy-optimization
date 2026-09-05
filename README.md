# Naphtha HDS Process Simulation & Energy Optimization

Chemical Engineering | Refinery Process Design | Heat Integration | Engineering Economics | Python | GitHub | Live Demo

A reproducible screening model of a representative **3,000 kg/h naphtha hydrodesulfurization (HDS)** unit. The project combines component material balances, hydrogen demand, sulfur specification, process-to-process heat recovery, LMTD/exchanger-area screening, utility and CO2 estimates, reactor-volume screening, pressure-drop screening, sensitivity analysis, and bounded operating optimization.

---

## Live Demo

[Launch Interactive HDS Simulator](https://naphtha-hds-process-simulation-energy-optimization-abhi-iitg.streamlit.app/)

An interactive Streamlit interface for exploring the HDS material balance,
heat integration, equipment screening, sensitivity analysis, and constrained
operating optimization.

---

## 📑 Table of Contents

- [Project Overview](#project-overview)
    - [Design Objective](#design-objective)
- [Key Features](#key-features)
    - [Process modelling](#process-modelling)
    - [Energy analysis](#energy-analysis)
    - [Equipment screening](#equipment-screening)
    - [Optimization and analytics](#optimization-and-analytics)
- [Process Flow](#process-flow)
- [Engineering Methodology](#engineering-methodology)
- [Feed Basis](#feed-basis)
    - [Overall feed basis](#overall-feed-basis)
    - [Surrogate feed composition](#surrogate-feed-composition)
- [Hydrodesulfurization Model](#hydrodesulfurization-model)
    - [Thiophene](#thiophene)
    - [Benzothiophene](#benzothiophene)
    - [Base conversions](#base-conversions)
- [Material Balances](#material-balances)
    - [Sulfur specification](#sulfur-specification)
- [Heat Integration](#heat-integration)
    - [Heat available from hot stream](#heat-available-from-hot-stream)
    - [Heat required by cold stream](#heat-required-by-cold-stream)
    - [Thermal feasibility](#thermal-feasibility)
- [Heat Exchanger Sizing](#heat-exchanger-sizing)
    - [LMTD](#lmtd)
- [Reactor Sizing](#reactor-sizing)
- [Hydraulic Screening](#hydraulic-screening)
    - [Default screening geometry](#default-screening-geometry)
- [Compressor Power](#compressor-power)
- [Process Optimization](#process-optimization)
    - [Reactor temperature](#reactor-temperature)
    - [Thiophene conversion](#thiophene-conversion)
    - [Benzothiophene conversion](#benzothiophene-conversion)
    - [Feasibility constraint](#feasibility-constraint)
    - [Optimization objective](#optimization-objective)
- [Sensitivity Analysis](#sensitivity-analysis)
    - [Interpretation of the current sensitivity run](#interpretation-of-the-current-sensitivity-run)
- [Live Interactive Demo](#live-interactive-demo)
    - [Run locally](#run-locally)
- [Results](#results)
- [Baseline Results](#baseline-results)
    - [Baseline KPI table](#baseline-kpi-table)
- [Optimized Results](#optimized-results)
    - [Baseline vs. optimized interpretation](#baseline-vs-optimized-interpretation)
- [Project Structure](#project-structure)
- [Engineering Limitations](#engineering-limitations)
    - [Thermodynamics](#thermodynamics)
    - [Reactor engineering](#reactor-engineering)
    - [Separation and recycle](#separation-and-recycle)
    - [Heat integration](#heat-integration)
    - [Equipment and operations](#equipment-and-operations)
    - [Economics and sustainability](#economics-and-sustainability)
- [Interview Talking Points](#interview-talking-points)
    - [Chemical engineering](#chemical-engineering)
    - [Analytics and optimization](#analytics-and-optimization)
    - [Strong engineering answer](#strong-engineering-answer)
- [References](#references)
- [Future Improvements](#future-improvements)
    - [Priority 1 — Rigorous reaction model](#priority-1-rigorous-reaction-model)
    - [Priority 2 — Rigorous thermodynamics](#priority-2-rigorous-thermodynamics)
    - [Priority 3 — Detailed reactor design](#priority-3-detailed-reactor-design)
    - [Priority 4 — Heat-exchanger network](#priority-4-heat-exchanger-network)
    - [Priority 5 — Hydrogen system](#priority-5-hydrogen-system)
    - [Priority 6 — Economic optimization](#priority-6-economic-optimization)
    - [Priority 7 — Digital engineering interface](#priority-7-digital-engineering-interface)
- [Author](#author)
- [License](#license)
- [Engineering takeaway](#engineering-takeaway)
---

## Project Overview

Naphtha hydrodesulfurization removes sulfur-containing compounds from naphtha before downstream processing. The engineering challenge is not only achieving the required sulfur specification, but doing so while balancing:

- hydrogen consumption,
- reactor operating temperature,
- heat recovery,
- furnace duty,
- exchanger area,
- reactor volume,
- hydraulic constraints,
- compressor power,
- and overall energy/environmental performance.

This project converts those trade-offs into a transparent computational workflow:

```text
Feed Basis
    ↓
Component Material Balance
    ↓
HDS Stoichiometry
    ↓
H₂ Demand + H₂S Generation
    ↓
Sulfur Specification Check
    ↓
Reactor-Volume Screening
    ↓
Process-to-Process Heat Recovery
    ↓
LMTD + Heat-Exchanger Area
    ↓
Residual Furnace Duty
    ↓
Fuel / CO₂ Screening
    ↓
Hydraulic + Compressor Screening
    ↓
Temperature Sensitivity
    ↓
Constrained Operating Optimization
```

### Design Objective

Find operating conditions that:

1. satisfy the calculated **product sulfur target of ≤10 ppm**;
2. respect the thermal feasibility constraints used by the model;
3. reduce furnace duty through heat recovery;
4. keep equipment-screening metrics visible;
5. provide a reproducible basis for comparing operating scenarios.

---

## Key Features

### Process modelling

- Component-level surrogate naphtha feed.
- Steady-state material balance.
- Explicit sulfur-species conversion.
- Stoichiometric hydrogen consumption.
- H₂S generation calculation.
- Product sulfur calculation in ppm.
- Sulfur-removal percentage.

### Energy analysis

- Reactor-effluent-to-feed heat recovery.
- Minimum temperature-approach constraint.
- LMTD calculation.
- Heat-exchanger area screening.
- Residual furnace duty.
- Fuel-consumption scenario estimate.
- Annual fuel-cost saving estimate.
- Annual CO₂-reduction scenario estimate.

### Equipment screening

- LHSV-based catalyst-bed volume.
- Gross reactor-volume estimate using void fraction.
- Darcy-Weisbach line pressure-drop screen.
- Reynolds number and friction-factor calculation.
- Ideal-gas isothermal compressor-power screen.

### Optimization and analytics

- Reactor-temperature sensitivity analysis.
- Bounded conversion sweep.
- Sulfur-specification constraint.
- Deterministic grid-search optimization.
- Baseline vs. optimized comparison.
- CSV result generation.
- Automated validation tests.
- Interactive Streamlit dashboard.

---

## Process Flow

The simplified process representation used by the computational model is:

```text
Naphtha Feed
   │
   ├────────────── H₂
   │
   ▼
Mixer / Feed Preparation
   │
   ▼
Feed / Effluent Heat Exchanger
   │
   ▼
Furnace
   │
   ▼
HDS Reactor
   │
   ▼
Cooling / Separation
   │
   ▼
Desulfurized Naphtha
```

The hot reactor effluent is used as the heat source for preheating the cold feed. This creates the central energy-integration trade-off: **recover more process heat to reduce furnace duty while respecting a minimum temperature approach.**

The repository also generates a process-flow figure at:

`figures/process_flow_diagram.png`

---

# Engineering Methodology

## Feed Basis

The model uses a transparent surrogate naphtha rather than a proprietary or plant-specific assay.

### Overall feed basis

| Parameter | Value |
|---|---:|
| Naphtha feed | 3,000 kg/h |
| Feed temperature | 40 °C |
| Reactor pressure | 40 bar |
| Base reactor temperature | 350 °C |
| Fresh H₂ excess | 25% |
| Product sulfur target | ≤10 ppm |
| Minimum HX approach | 20 °C |
| Hot-side outlet target | 120 °C |
| LHSV screening basis | 3 h⁻¹ |
| HX U-value screening basis | 250 W/m²-K |
| Liquid density | 700 kg/m³ |
| Reactor void fraction | 0.40 |
| Annual operating hours | 8,000 h/y |

### Surrogate feed composition

| Component | Mass fraction |
|---|---:|
| n-Hexane | 0.350 |
| n-Heptane | 0.300 |
| n-Octane | 0.315 |
| Thiophene | 0.020 |
| Benzothiophene | 0.015 |
| **Total** | **1.000** |

The feed fractions are explicitly checked for closure before the material balance is performed.

---

## Hydrodesulfurization Model

Two representative sulfur species are modelled:

### Thiophene

```text
C₄H₄S + 4 H₂ → C₄H₁₀ + H₂S
```

### Benzothiophene

```text
C₈H₆S + 3 H₂ → C₈H₁₀ + H₂S
```

The model uses specified conversions rather than kinetic rate equations.

### Base conversions

| Sulfur species | Base conversion |
|---|---:|
| Thiophene | 99.99% |
| Benzothiophene | 99.98% |

For each sulfur species:

1. feed mass is converted to kmol/h;
2. reacted kmol/h is calculated from the specified conversion;
3. stoichiometric H₂ demand is calculated;
4. corresponding hydrocarbon product is generated;
5. unreacted sulfur species remain in the product;
6. H₂S production is calculated from sulfur-species conversion.

This approach is deliberately transparent and suitable for **screening and sensitivity analysis**, not detailed catalyst/reactor design.

---

## Material Balances

The model calculates:

- feed component flowrates,
- reacted sulfur-species flowrates,
- unreacted sulfur-species flowrates,
- hydrocarbon product flowrates,
- stoichiometric H₂ demand,
- fresh H₂ requirement,
- H₂S generation,
- sulfur entering the reactor,
- sulfur remaining in the product,
- calculated product sulfur concentration,
- sulfur-removal percentage.

Fresh hydrogen is calculated as:

```text
Fresh H₂ = Stoichiometric H₂ × 1.25
```

The remaining fresh H₂ is retained on the product-side accounting basis so that the overall mass balance closes.

### Sulfur specification

The calculated product sulfur concentration is:

```text
Product sulfur (ppm)
= Sulfur remaining in product / Total product mass × 10⁶
```

The process is considered specification-compliant when:

```text
Product sulfur ≤ 10 ppm
```

---

## Heat Integration

The reactor effluent is treated as a hot process stream and the feed plus fresh hydrogen as the cold process stream.

The model applies constant heat capacities and a minimum temperature approach.

### Heat available from hot stream

```text
Qhot = Cp,hot × ΔT
```

### Heat required by cold stream

```text
Qcold = Cp,cold × ΔT
```

The recoverable heat is limited by the smaller of the two:

```text
Qrecovered = min(Qhot, Qcold)
```

The model then calculates:

- hot-stream outlet temperature,
- cold-stream outlet temperature,
- LMTD,
- exchanger area,
- baseline furnace duty,
- integrated furnace duty,
- percentage heat-recovery saving.

### Thermal feasibility

The heat exchanger must satisfy the configured minimum approach of:

```text
ΔTmin = 20 °C
```

The implementation rejects an infeasible reactor-temperature basis when the reactor temperature is too close to the configured hot-side outlet target.

---

## Heat Exchanger Sizing

The exchanger area is screened using:

```text
A = Q / (U × LMTD)
```

where:

- `A` = heat-transfer area, m²
- `Q` = recovered heat duty, W
- `U` = overall heat-transfer coefficient, W/m²-K
- `LMTD` = log-mean temperature difference, K

The configured screening value is:

```text
U = 250 W/m²-K
```

### LMTD

For terminal temperature differences `ΔT₁` and `ΔT₂`:

```text
LMTD = (ΔT₁ - ΔT₂) / ln(ΔT₁ / ΔT₂)
```

The model also checks that the temperature-approach constraints remain valid.

> **Interpretation:** The exchanger area is a preliminary screening estimate, not a mechanical design. Real exchanger design would require detailed fluid properties, fouling factors, pressure drops, geometry, allowable velocities, metallurgy, and vendor/design correlations.

---

## Reactor Sizing

The first-pass reactor screen uses liquid hourly space velocity:

```text
LHSV = Liquid volumetric flow / Catalyst-bed volume
```

Therefore:

```text
Catalyst-bed volume = Liquid volumetric flow / LHSV
```

The liquid feed volume is estimated from:

```text
Liquid volumetric flow = Mass flow / Liquid density
```

Using:

- feed = 3,000 kg/h,
- liquid density = 700 kg/m³,
- LHSV = 3 h⁻¹,

the model calculates the catalyst-bed and gross reactor-volume screens.

The gross volume accounts for the configured reactor void fraction:

```text
Gross reactor volume
= Catalyst-bed volume / (1 - void fraction)
```

with:

```text
Void fraction = 0.40
```

---

## Hydraulic Screening

A simplified line-pressure-drop calculation is included as a screening tool.

The model calculates:

- flow velocity,
- Reynolds number,
- friction factor,
- pressure drop.

The calculation uses a Darcy-Weisbach formulation:

```text
ΔP = f × (L/D) × (ρv²/2)
```

For the friction factor, the implementation uses:

- laminar `64/Re` behaviour below the laminar threshold;
- an explicit turbulent correlation using roughness and Reynolds number above the threshold.

### Default screening geometry

| Parameter | Value |
|---|---:|
| Diameter | 0.10 m |
| Length | 5.0 m |
| Density | 700 kg/m³ |
| Viscosity | 0.0004 Pa·s |
| Roughness | 4.5 × 10⁻⁵ m |

> This is a **line-screening calculation**, not a packed-bed pressure-drop model. It should not be interpreted as an Ergun-based reactor pressure-drop calculation.

---

## Compressor Power

Hydrogen compressor power is screened using an ideal-gas isothermal-work relationship divided by compressor efficiency:

```text
W = nRT ln(P₂/P₁) / η
```

The default screening basis uses:

| Parameter | Value |
|---|---:|
| Suction pressure | 5 bar |
| Discharge pressure | 40 bar |
| Temperature | 313.15 K |
| Compressor efficiency | 72% |

The resulting value is a **screening estimate**, not a compressor datasheet/design calculation.

---

# Process Optimization

The optimization module performs a deterministic grid search over:

### Reactor temperature

```text
320–370 °C
```

in 5 °C increments.

### Thiophene conversion

```text
99.90%
99.92%
99.94%
99.96%
99.98%
99.99%
99.995%
```

### Benzothiophene conversion

```text
99.90%
99.92%
99.94%
99.96%
99.98%
99.99%
```

### Feasibility constraint

Only cases satisfying:

```text
Calculated product sulfur ≤ 10 ppm
```

are retained.

### Optimization objective

Among feasible cases, the selected operating point minimizes:

1. furnace duty;
2. reactor temperature as a secondary tie-breaker.

This is a **bounded deterministic grid search**, not a nonlinear mathematical-programming solver.

---

# Sensitivity Analysis

The repository evaluates reactor-temperature sensitivity from:

```text
320 °C → 370 °C
```

in 5 °C increments.

For each temperature, the model records:

- product sulfur,
- furnace duty,
- heat-exchanger area.

The generated results are stored in:

`results/sensitivity_results.csv`

and visualized through:

- `figures/furnace_duty_sensitivity.png`
- `figures/sulfur_sensitivity.png`

### Interpretation of the current sensitivity run

At the base conversion values, calculated product sulfur remains approximately **1.474 ppm** across the temperature sweep, because the current model specifies conversion independently of temperature.

Furnace duty increases across the temperature range, while exchanger area also increases. This is an important modelling insight: **temperature sensitivity in the current model primarily affects thermal integration and equipment-screening metrics, not reaction conversion.**

A more physically rigorous model would couple conversion to temperature through validated reaction kinetics.

---

## Live Interactive Demo

The repository includes a Streamlit application in `streamlit_app.py` for interactive exploration of:

- reactor temperature and sulfur-species conversion inputs
- product sulfur and sulfur-removal KPIs
- fresh H2 demand and H2S generation
- heat recovery, LMTD and exchanger-area screening
- reactor volume, pressure-drop and compressor-power screens
- reactor-temperature sensitivity plots
- deterministic constrained optimization against the **≤10 ppm** sulfur target

### Run locally

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
python -m pytest -q
streamlit run streamlit_app.py
```
The browser application should open at the local Streamlit address shown in the terminal.

---

# Results

All headline values below are taken from the repository's generated CSV outputs rather than being manually invented for this README.

## Baseline Results

The current baseline case uses:

- 3,000 kg/h feed;
- 350 °C reactor temperature;
- 40 bar reactor pressure;
- 99.99% thiophene conversion;
- 99.98% benzothiophene conversion;
- 25% fresh-H₂ excess.

### Baseline KPI table

| Metric | Result |
|---|---:|
| Feed | 3,000 kg/h |
| Reactor temperature | 350 °C |
| Reactor pressure | 40 bar |
| Fresh H₂ | 4.823 kmol/h |
| H₂ consumed | 3.858 kmol/h |
| H₂S produced | 1.048 kmol/h |
| Sulfur in | 33.614 kg/h |
| Sulfur out | 0.00444 kg/h |
| Calculated product sulfur | **1.474 ppm** |
| Sulfur removal | **99.9868%** |
| Heat recovered | 2,034.877 MJ/h |
| LMTD | 21.978 °C |
| HX area | 102.872 m² |
| Integrated furnace duty | 171.402 MJ/h |
| Heat-recovery saving | **92.231%** |
| Catalyst-bed volume | 1.429 m³ |
| Gross reactor volume | 2.381 m³ |
| Screened line ΔP | 0.0102 kPa |
| H₂ compressor-power screen | 10.073 kW |
| Annual fuel saving | 325,580 kg/y |
| Annual fuel-cost saving | USD 179,069/y |
| Annual CO₂ reduction | 1,025,578 kg/y |

The baseline case comfortably satisfies the model's ≤10 ppm sulfur specification.

Source: `results/baseline_results.csv`.

---

## Optimized Results

The current deterministic grid search identifies the following feasible point:

| Metric | Optimized result |
|---|---:|
| Reactor temperature | **320 °C** |
| Thiophene conversion | **99.90%** |
| Benzothiophene conversion | **99.94%** |
| Calculated product sulfur | **9.740 ppm** |
| Sulfur removal | **99.9128%** |
| Furnace duty | **168.373 MJ/h** |
| HX area | **93.079 m²** |
| Heat-recovery saving | **91.551%** |

Source: `results/optimization_result.csv`.

### Baseline vs. optimized interpretation

The optimization does not simply maximize conversion or temperature. It searches for a **feasible operating point that meets the sulfur specification while minimizing furnace duty**.

Compared with the baseline case, the selected point:

- reduces reactor temperature from 350 °C to 320 °C;
- reduces furnace duty from 171.402 to 168.373 MJ/h;
- reduces screened exchanger area from 102.872 to 93.079 m²;
- still meets the ≤10 ppm product-sulfur target.

This result should be interpreted strictly within the model assumptions. It does **not** prove that 320 °C is an industrially optimal HDS operating temperature because the current model does not contain temperature-dependent reaction kinetics, catalyst deactivation, rigorous phase behaviour, or detailed reactor hydraulics.

---

# Project Structure

```text
naphtha-hds-process-simulation-energy-optimization/
│
├── README.md
├── LICENSE
├── requirements.txt
├── streamlit_app.py
│
├── data/
│   └── feed_basis.csv
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── model.py
│   ├── equipment.py
│   ├── optimization.py
│   └── reporting.py
│
├── tests/
│   └── test_model.py
│
├── results/
│   ├── baseline_results.csv
│   ├── optimization_result.csv
│   └── sensitivity_results.csv
│
├── figures/
│   ├── process_flow_diagram.png
│   ├── heat_integration.png
│   ├── furnace_duty_sensitivity.png
│   └── sulfur_sensitivity.png
│
└── docs/
    ├── engineering_basis.md
    ├── final_report.txt
    ├── final_test_runs.txt
    ├── interview_guide.md
    ├── references.md
    └── validation_log.md
```

---
# Engineering Limitations

This repository is intended for **engineering learning, screening, comparison, and portfolio demonstration**. It is not intended for plant operation or final equipment specification.

A real industrial HDS design would require, at minimum:

### Thermodynamics

- rigorous phase-equilibrium calculations;
- realistic naphtha assay/pseudocomponents;
- temperature- and pressure-dependent physical properties;
- hydrogen/hydrocarbon phase behaviour;
- validated property methods.

### Reactor engineering

- Langmuir-Hinshelwood or other validated kinetics;
- catalyst-specific activity;
- catalyst deactivation;
- reactor temperature profile;
- pressure drop through catalyst bed;
- catalyst loading and shape-factor considerations;
- validated reactor performance data.

### Separation and recycle

- rigorous gas-liquid equilibrium;
- hydrogen recycle convergence;
- purge optimization;
- H₂S separation;
- amine treating and regeneration where applicable.

### Heat integration

- detailed stream segmentation;
- multiple exchangers;
- pressure-drop constraints;
- fouling factors;
- exchanger configuration;
- metallurgy;
- mechanical design.

### Equipment and operations

- detailed compressor design;
- pump sizing;
- control-valve sizing;
- relief-system design;
- equipment mechanical design;
- process-control strategy;
- HAZOP/LOPA and other safety studies.

### Economics and sustainability

- current equipment-cost basis;
- installation factors;
- utility pricing;
- maintenance and labour;
- lifecycle economics;
- emissions accounting boundaries;
- uncertainty analysis.

Accordingly, values such as **annual fuel saving** and **annual CO₂ reduction** should be interpreted as **scenario calculations from the screening model**, not plant-certified economic or environmental claims.

---

## Interview Talking Points

This project can support discussion around both **chemical engineering** and **analytical decision making**.

### Chemical engineering

- Why is the H₂:N₂ feed ratio 3:1?
- Why is recycle required?
- Why is a purge required?
- Why does electrolysis dominate energy demand?
- Why does pressure influence ammonia synthesis?
- What is the role of NH₃ condensation?
- How would you validate the process in Aspen Plus?

### Analytics and optimization

- Which assumptions dominate LCOA?
- Why use deterministic grid search?
- How would you handle uncertainty?
- How would you introduce a pressure-dependent compressor model?
- How would you optimize for cost and carbon simultaneously?
- How would you model renewable intermittency?
- What would you change before calling this a bankable TEA?

### Strong engineering answer

> "I intentionally separated the transparent screening layer from the rigorous validation layer. The Python model is useful for fast scenario analysis and optimization, while Aspen Plus should be used to validate thermodynamics, recycle convergence, phase behavior and unit-operation duties before treating the results as design-grade."

---

# References

The repository maintains a separate reference landscape in:

`docs/references.md`

The reference landscape includes public examples covering:

- naphtha HDS and heat integration;
- Aspen Plus automation;
- process-simulation optimization;
- pinch-analysis workflows;
- chemical-engineering process design;
- equipment sizing/costing;
- CFD/process-engineering platforms.

The references are used for **scope and workflow benchmarking**, not as a source of copied project-specific calculations.

---

# Future Improvements

The next level of the project would move from a transparent screening model toward a more rigorous process-engineering simulator.

### Priority 1 — Rigorous reaction model

- Add temperature-dependent HDS kinetics.
- Model catalyst activity and deactivation.
- Couple conversion to reactor conditions.
- Add reactor-temperature-profile calculations.

### Priority 2 — Rigorous thermodynamics

- Add a thermodynamic property package.
- Introduce realistic pseudocomponents.
- Add VLE calculations.
- Improve hydrogen/hydrocarbon phase behaviour.

### Priority 3 — Detailed reactor design

- Replace the LHSV-only screen with a kinetic reactor model.
- Add packed-bed pressure drop using the Ergun equation.
- Include catalyst density, voidage, and pellet properties.
- Evaluate reactor diameter and length.

### Priority 4 — Heat-exchanger network

- Move from a single process-to-process exchanger to a multi-stream HEN.
- Add pressure-drop constraints.
- Include fouling factors.
- Perform pinch analysis.
- Optimize exchanger network configuration.

### Priority 5 — Hydrogen system

- Add hydrogen recycle and purge.
- Model compressor stages.
- Include compressor efficiency maps.
- Optimize hydrogen utilization.

### Priority 6 — Economic optimization

- Add equipment-cost correlations.
- Include utility costs.
- Add operating expenditure.
- Add capital expenditure.
- Calculate NPV, IRR, and payback period.
- Perform uncertainty/sensitivity analysis.

### Priority 7 — Digital engineering interface

- Add scenario comparison.
- Add downloadable engineering reports.
- Add parameter provenance.
- Add automated regression testing.
- Add CI/CD validation through GitHub Actions.

---

# Author

**Abhishek Kumar Gond**

IIT Guwahati  
Chemical Engineering

- **Email : mr.abhishekaaa@gmail.com**
- **[Portfolio]()**
- **[LinkedIn](https://www.linkedin.com/in/abhishekkumargond/)**

---

## License

Released under the [MIT License](LICENSE).

---

## Engineering takeaway

The central screening insight is straightforward:

> **For green ammonia, the cost and energy story is strongly driven by electricity-intensive hydrogen production.**

The value of this project is not a single "optimal" number. It is the **reproducible chain from engineering assumptions → process balances → energy → economics → emissions → optimization → validation**.

---
