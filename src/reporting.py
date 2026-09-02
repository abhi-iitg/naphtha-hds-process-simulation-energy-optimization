from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch
from .model import run_case
from .equipment import reactor_screen,pressure_drop_screen,compressor_power_screen
from .optimization import grid_search
from .config import *

ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/"results"; FIGURES=ROOT/"figures"

def make_pfd(path):
    fig,ax=plt.subplots(figsize=(12,4.5))
    ax.set_xlim(0,12); ax.set_ylim(0,5); ax.axis("off")
    blocks=[(0.3,2.0,"Naphtha Feed"),(2.0,2.0,"Mixer + H2"),
            (3.7,2.0,"Feed / Effluent HX"),(5.5,2.0,"Furnace"),
            (7.3,2.0,"HDS Reactor"),(9.1,2.0,"Cooling / Separation")]
    for x,y,label in blocks:
        p=FancyBboxPatch((x,y),1.35,.85,boxstyle="round,pad=.04",fill=False,linewidth=1.5)
        ax.add_patch(p); ax.text(x+.675,y+.425,label,ha="center",va="center",fontsize=8)
    for a,b in zip(blocks[:-1],blocks[1:]):
        ax.add_patch(FancyArrowPatch((a[0]+1.35,a[1]+.425),(b[0],b[1]+.425),
                                     arrowstyle="->",mutation_scale=12))
    ax.add_patch(FancyArrowPatch((9.775,2),(9.775,1.25),arrowstyle="->",mutation_scale=12))
    ax.text(9.775,.9,"Desulfurized\nnaphtha",ha="center",fontsize=8)
    ax.text(7.1,3.45,"HDS: sulfur species + H2 → hydrocarbon + H2S",fontsize=9)
    ax.text(3.4,1.0,"Hot reactor effluent provides sensible heat to the cold feed",fontsize=9)
    fig.tight_layout(); fig.savefig(path,dpi=180); plt.close(fig)

def main():
    RESULTS.mkdir(exist_ok=True); FIGURES.mkdir(exist_ok=True)
    r=run_case(); b=r["balance"]; h=r["heat"]
    eq=reactor_screen(); dp=pressure_drop_screen(); comp=compressor_power_screen(b.h2_fresh_kmol_h)

    base_fuel=h["baseline_furnace_kj_h"]/1000*ANNUAL_OPERATING_HOURS/FUEL_LHV_MJ_KG
    int_fuel=h["furnace_duty_kj_h"]/1000*ANNUAL_OPERATING_HOURS/FUEL_LHV_MJ_KG
    saving=base_fuel-int_fuel

    rows=[
        ("Feed",FEED_KG_H,"kg/h"),("Reactor temperature",BASE_REACTOR_T_C,"°C"),
        ("Reactor pressure",REACTOR_P_BAR,"bar"),("Fresh H2",b.h2_fresh_kmol_h,"kmol/h"),
        ("H2 consumed",b.h2_consumed_kmol_h,"kmol/h"),("H2S produced",b.h2s_kmol_h,"kmol/h"),
        ("Sulfur in",b.sulfur_in_kg_h,"kg/h"),("Sulfur out",b.sulfur_out_kg_h,"kg/h"),
        ("Product sulfur",b.sulfur_ppm,"ppm"),("Sulfur removal",b.sulfur_removal_pct,"%"),
        ("Heat recovered",h["q_recovered_kj_h"]/1000,"MJ/h"),("LMTD",h["lmtd_c"],"°C"),
        ("HX area",h["hx_area_m2"],"m²"),("Furnace duty",h["furnace_duty_kj_h"]/1000,"MJ/h"),
        ("Heat recovery saving",h["heat_recovery_savings_pct"],"%"),
        ("Catalyst bed volume",eq["catalyst_bed_volume_m3"],"m³"),
        ("Gross reactor volume",eq["gross_reactor_volume_m3"],"m³"),
        ("Screened line ΔP",dp["pressure_drop_kpa"],"kPa"),
        ("H2 compressor power screen",comp,"kW"),
        ("Annual fuel saving",saving,"kg/y"),
        ("Annual fuel-cost saving",saving*FUEL_COST_USD_KG,"USD/y"),
        ("Annual CO2 reduction",saving*FUEL_CO2_KG_KG,"kg/y")
    ]
    pd.DataFrame(rows,columns=["metric","value","unit"]).to_csv(RESULTS/"baseline_results.csv",index=False)

    best=grid_search()
    pd.DataFrame([best]).to_csv(RESULTS/"optimization_result.csv",index=False)

    sens=[]
    for t in range(320,371,5):
        x=run_case(t)
        sens.append([t,x["balance"].sulfur_ppm,x["heat"]["furnace_duty_kj_h"]/1000,x["heat"]["hx_area_m2"]])
    sdf=pd.DataFrame(sens,columns=["temperature_c","sulfur_ppm","furnace_duty_mj_h","hx_area_m2"])
    sdf.to_csv(RESULTS/"sensitivity_results.csv",index=False)

    ax=sdf.plot(x="temperature_c",y="furnace_duty_mj_h",marker="o",legend=False)
    ax.set_ylabel("Furnace duty (MJ/h)"); ax.set_title("Reactor-temperature sensitivity: furnace duty")
    ax.figure.tight_layout(); ax.figure.savefig(FIGURES/"furnace_duty_sensitivity.png",dpi=180); plt.close(ax.figure)

    ax=sdf.plot(x="temperature_c",y="sulfur_ppm",marker="o",legend=False)
    ax.axhline(TARGET_SULFUR_PPM,linestyle="--")
    ax.set_ylabel("Product sulfur (ppm)"); ax.set_title("Calculated product sulfur vs reactor temperature")
    ax.figure.tight_layout(); ax.figure.savefig(FIGURES/"sulfur_sensitivity.png",dpi=180); plt.close(ax.figure)

    energy=pd.DataFrame({"case":["No recovery","Integrated"],
                         "duty_mj_h":[h["baseline_furnace_kj_h"]/1000,h["furnace_duty_kj_h"]/1000]}).set_index("case")
    ax=energy.plot(kind="bar",legend=False); ax.set_ylabel("Furnace duty (MJ/h)")
    ax.set_title("Heat-integration screening")
    ax.figure.tight_layout(); ax.figure.savefig(FIGURES/"heat_integration.png",dpi=180); plt.close(ax.figure)

    make_pfd(FIGURES/"process_flow_diagram.png")

    print("=== BASELINE ===")
    print(f"Product sulfur: {b.sulfur_ppm:.4f} ppm")
    print(f"Sulfur removal: {b.sulfur_removal_pct:.4f}%")
    print(f"Fresh H2: {b.h2_fresh_kmol_h:.4f} kmol/h")
    print(f"Heat recovered: {h['q_recovered_kj_h']/1000:.3f} MJ/h")
    print(f"LMTD: {h['lmtd_c']:.3f} C")
    print(f"HX area: {h['hx_area_m2']:.3f} m2")
    print(f"Furnace duty: {h['furnace_duty_kj_h']/1000:.3f} MJ/h")
    print("\n=== BEST FEASIBLE GRID POINT ===")
    print(best)

if __name__=="__main__":
    main()
