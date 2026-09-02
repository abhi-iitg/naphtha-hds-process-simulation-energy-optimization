from .model import run_case
from .config import TARGET_SULFUR_PPM

def grid_search():
    candidates=[]
    for t in range(320,371,5):
        for xt in [0.9990,0.9992,0.9994,0.9996,0.9998,0.9999,0.99995]:
            for xb in [0.9990,0.9992,0.9994,0.9996,0.9998,0.9999]:
                r=run_case(t,{"thiophene":xt,"benzothiophene":xb})
                if r["balance"].sulfur_ppm<=TARGET_SULFUR_PPM:
                    candidates.append({
                        "reactor_temperature_c":t,
                        "thiophene_conversion":xt,
                        "benzothiophene_conversion":xb,
                        "sulfur_ppm":r["balance"].sulfur_ppm,
                        "sulfur_removal_pct":r["balance"].sulfur_removal_pct,
                        "furnace_duty_mj_h":r["heat"]["furnace_duty_kj_h"]/1000,
                        "hx_area_m2":r["heat"]["hx_area_m2"],
                        "heat_recovery_saving_pct":r["heat"]["heat_recovery_savings_pct"]
                    })
    if not candidates:
        raise RuntimeError("No feasible operating point.")
    return min(candidates,key=lambda x:(x["furnace_duty_mj_h"],x["reactor_temperature_c"]))
