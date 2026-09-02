from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import (  # noqa: E402
    BASE_CONVERSION,
    BASE_REACTOR_T_C,
    FEED_KG_H,
    FEED_T_C,
    REACTOR_P_BAR,
    TARGET_SULFUR_PPM,
)
from src.equipment import compressor_power_screen, pressure_drop_screen, reactor_screen  # noqa: E402
from src.model import run_case  # noqa: E402
from src.optimization import grid_search  # noqa: E402

st.set_page_config(
    page_title="Naphtha HDS Process Simulation",
    page_icon="⚗️",
    layout="wide",
)

st.title("Naphtha HDS Process Simulation & Energy Optimization")
st.caption("First-principles engineering screening model • 3,000 kg/h representative naphtha feed")

with st.sidebar:
    st.header("Operating Inputs")
    reactor_t = st.slider(
        "Reactor temperature (°C)",
        min_value=320,
        max_value=370,
        value=int(BASE_REACTOR_T_C),
        step=5,
    )
    thiophene_conv = st.slider(
        "Thiophene conversion",
        min_value=0.9900,
        max_value=0.99995,
        value=float(BASE_CONVERSION["thiophene"]),
        step=0.00005,
        format="%.5f",
    )
    benzothiophene_conv = st.slider(
        "Benzothiophene conversion",
        min_value=0.9900,
        max_value=0.99990,
        value=float(BASE_CONVERSION["benzothiophene"]),
        step=0.00005,
        format="%.5f",
    )

    st.divider()
    st.info(
        f"Fixed design basis: {FEED_KG_H:,.0f} kg/h feed, {REACTOR_P_BAR:.0f} bar reactor pressure, "
        f"{FEED_T_C:.0f} °C feed temperature."
    )

conversion = {
    "thiophene": thiophene_conv,
    "benzothiophene": benzothiophene_conv,
}

try:
    result = run_case(reactor_t, conversion)
    balance = result["balance"]
    heat = result["heat"]
    equipment = reactor_screen()
    pressure = pressure_drop_screen()
    compressor = compressor_power_screen(balance.h2_fresh_kmol_h)
except Exception as exc:
    st.error(f"The selected operating point is infeasible: {exc}")
    st.stop()

# KPI row
k1, k2, k3, k4 = st.columns(4)
k1.metric("Product sulfur", f"{balance.sulfur_ppm:.3f} ppm", "PASS" if result["sulfur_spec_met"] else "ABOVE 10 ppm")
k2.metric("Sulfur removal", f"{balance.sulfur_removal_pct:.4f}%")
k3.metric("Fresh H₂", f"{balance.h2_fresh_kmol_h:.3f} kmol/h")
k4.metric("Furnace duty", f"{heat['furnace_duty_kj_h']/1000:.3f} MJ/h")

st.divider()

left, right = st.columns(2)
with left:
    st.subheader("Material Balance")
    material_rows = [
        ["Feed", f"{FEED_KG_H:,.2f}", "kg/h"],
        ["Fresh H₂", f"{balance.h2_fresh_kmol_h:.4f}", "kmol/h"],
        ["H₂ consumed", f"{balance.h2_consumed_kmol_h:.4f}", "kmol/h"],
        ["H₂S generated", f"{balance.h2s_kmol_h:.4f}", "kmol/h"],
        ["Sulfur in feed", f"{balance.sulfur_in_kg_h:.4f}", "kg/h"],
        ["Sulfur in product", f"{balance.sulfur_out_kg_h:.4f}", "kg/h"],
        ["Total product + gas", f"{balance.total_product_kg_h:,.3f}", "kg/h"],
    ]
    st.dataframe(pd.DataFrame(material_rows, columns=["Metric", "Value", "Unit"]), hide_index=True, use_container_width=True)

with right:
    st.subheader("Heat Integration & Equipment Screen")
    engineering_rows = [
        ["Heat recovered", f"{heat['q_recovered_kj_h']/1000:.3f}", "MJ/h"],
        ["LMTD", f"{heat['lmtd_c']:.3f}", "°C"],
        ["HX area", f"{heat['hx_area_m2']:.3f}", "m²"],
        ["Hot-side outlet", f"{heat['hot_outlet_c']:.2f}", "°C"],
        ["Cold-side outlet", f"{heat['cold_outlet_c']:.2f}", "°C"],
        ["Catalyst-bed volume", f"{equipment['catalyst_bed_volume_m3']:.3f}", "m³"],
        ["Gross reactor volume", f"{equipment['gross_reactor_volume_m3']:.3f}", "m³"],
        ["Screened line ΔP", f"{pressure['pressure_drop_kpa']:.3f}", "kPa"],
        ["H₂ compressor power", f"{compressor:.3f}", "kW"],
    ]
    st.dataframe(pd.DataFrame(engineering_rows, columns=["Metric", "Value", "Unit"]), hide_index=True, use_container_width=True)

st.subheader("Operating-Point Assessment")
status_cols = st.columns(3)
status_cols[0].success("Sulfur specification met" if result["sulfur_spec_met"] else "Sulfur specification NOT met")
status_cols[1].write(f"**Target:** ≤ {TARGET_SULFUR_PPM:.0f} ppm")
status_cols[2].write(f"**Heat-recovery saving:** {heat['heat_recovery_savings_pct']:.2f}%")

st.divider()

st.subheader("Reactor Temperature Sensitivity")
sensitivity_rows = []
for temp in range(320, 371, 5):
    r = run_case(temp, conversion)
    sensitivity_rows.append(
        {
            "Reactor temperature (°C)": temp,
            "Product sulfur (ppm)": r["balance"].sulfur_ppm,
            "Furnace duty (MJ/h)": r["heat"]["furnace_duty_kj_h"] / 1000,
            "HX area (m²)": r["heat"]["hx_area_m2"],
        }
    )
sdf = pd.DataFrame(sensitivity_rows)

c1, c2 = st.columns(2)
with c1:
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(sdf.iloc[:, 0], sdf.iloc[:, 2], marker="o")
    ax.set_xlabel("Reactor temperature (°C)")
    ax.set_ylabel("Furnace duty (MJ/h)")
    ax.set_title("Furnace duty sensitivity")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)

with c2:
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(sdf.iloc[:, 0], sdf.iloc[:, 1], marker="o")
    ax.axhline(TARGET_SULFUR_PPM, linestyle="--", label="10 ppm target")
    ax.set_xlabel("Reactor temperature (°C)")
    ax.set_ylabel("Product sulfur (ppm)")
    ax.set_title("Product sulfur sensitivity")
    ax.legend()
    ax.grid(alpha=0.25)
    fig.tight_layout()
    st.pyplot(fig, clear_figure=True)

with st.expander("View sensitivity data"):
    st.dataframe(sdf, hide_index=True, use_container_width=True)

st.divider()

st.subheader("Constrained Optimization")
st.write(
    "Searches the project's deterministic grid over reactor temperature and sulfur-species conversions, "
    "retaining only points that meet the ≤10 ppm product-sulfur target."
)
if st.button("Run constrained optimization", type="primary"):
    with st.spinner("Evaluating feasible operating points..."):
        best = grid_search()
    st.success("Best feasible grid point found.")
    o1, o2, o3, o4 = st.columns(4)
    o1.metric("Optimal temperature", f"{best['reactor_temperature_c']:.0f} °C")
    o2.metric("Product sulfur", f"{best['sulfur_ppm']:.3f} ppm")
    o3.metric("Furnace duty", f"{best['furnace_duty_mj_h']:.3f} MJ/h")
    o4.metric("HX area", f"{best['hx_area_m2']:.3f} m²")
    st.dataframe(pd.DataFrame([best]), hide_index=True, use_container_width=True)

with st.expander("Process flow"):
    st.code(
        "Naphtha Feed → Mixer + H₂ → Feed/Effluent HX → Furnace → HDS Reactor → Cooling/Separation → Desulfurized Naphtha"
    )

with st.expander("Model scope and engineering disclaimer"):
    st.markdown(
        "This is a **license-free engineering screening model**, not a refinery licensing package and not an Aspen Plus file. "
        "It uses a transparent surrogate naphtha, constant heat capacities, specified HDS conversions, screening-level reactor "
        "hydraulics and deterministic optimization. Industrial design would require rigorous VLE, assay/pseudocomponent modeling, "
        "validated catalyst kinetics, reactor hydraulics, recycle convergence, detailed exchanger design, safety studies and plant data."
    )

st.caption("Model calculations are generated from the Python modules in src/. No external API or database is required.")
