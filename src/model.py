from dataclasses import dataclass
import math
from .config import *

@dataclass
class BalanceResult:
    feed: dict
    product: dict
    h2_stoich_kmol_h: float
    h2_fresh_kmol_h: float
    h2_consumed_kmol_h: float
    h2s_kmol_h: float
    sulfur_in_kg_h: float
    sulfur_out_kg_h: float
    sulfur_ppm: float
    sulfur_removal_pct: float
    total_product_kg_h: float
    feed_total_with_h2_kg_h: float
    product_cp_kj_h_k: float

def feed_basis(feed_kg_h=FEED_KG_H):
    if not math.isclose(sum(FEED_MASS_FRACTIONS.values()),1.0,abs_tol=1e-12):
        raise ValueError("Feed fractions do not close.")
    return {k:feed_kg_h*v for k,v in FEED_MASS_FRACTIONS.items()}

def material_balance(feed_kg_h=FEED_KG_H, conversion=None):
    conversion = conversion or BASE_CONVERSION
    feed = feed_basis(feed_kg_h)
    product = {}
    h2_stoich = 0.0
    h2s_kmol = 0.0

    for n in ("n_hexane","n_heptane","n_octane"):
        product[n] = feed[n]

    for s in ("thiophene","benzothiophene"):
        reacted_kmol = feed[s]/COMPONENTS[s].mw * conversion[s]
        unreacted_kg = feed[s] - reacted_kmol*COMPONENTS[s].mw
        pn = REACTIONS[s]["product"]
        product[pn] = reacted_kmol*COMPONENTS[pn].mw
        product[s] = unreacted_kg
        h2_stoich += reacted_kmol*REACTIONS[s]["h2_per_kmol"]
        h2s_kmol += reacted_kmol

    h2_fresh = h2_stoich*H2_EXCESS_FACTOR
    h2_consumed_kg = h2_stoich*H2_MW
    h2_fresh_kg = h2_fresh*H2_MW
    h2s_kg = h2s_kmol*H2S_MW
    remaining_h2_kg = h2_fresh_kg-h2_consumed_kg

    sulfur_in = sum(feed[n]*COMPONENTS[n].sulfur_mass_fraction for n in ("thiophene","benzothiophene"))
    sulfur_out = sum(product[n]*COMPONENTS[n].sulfur_mass_fraction for n in ("thiophene","benzothiophene"))

    total_product = sum(product.values())+h2s_kg+remaining_h2_kg
    feed_total = sum(feed.values())+h2_fresh_kg

    cp = sum(m*COMPONENTS[n].cp_kj_kg_k for n,m in product.items())
    cp += h2s_kg*COMPONENTS["H2S"].cp_kj_kg_k + remaining_h2_kg*14.3

    if not math.isclose(feed_total,total_product,rel_tol=1e-10,abs_tol=1e-8):
        raise RuntimeError(f"Mass balance failed: {feed_total} vs {total_product}")

    return BalanceResult(
        feed,product,h2_stoich,h2_fresh,h2_stoich,h2s_kmol,
        sulfur_in,sulfur_out,sulfur_out/total_product*1e6,
        100*(1-sulfur_out/sulfur_in),total_product,feed_total,cp
    )

def heat_integration(reactor_t_c,balance,feed_t_c=FEED_T_C,
                     hot_outlet_c=HOT_OUTLET_C,min_approach_c=MIN_APPROACH_C):
    if reactor_t_c <= hot_outlet_c+min_approach_c:
        raise ValueError("Infeasible exchanger temperature basis.")

    cold_cp = sum(balance.feed[n]*COMPONENTS[n].cp_kj_kg_k for n in balance.feed)
    cold_cp += balance.h2_fresh_kmol_h*H2_MW*14.3
    hot_cp = balance.product_cp_kj_h_k

    qh = hot_cp*(reactor_t_c-(feed_t_c+min_approach_c))
    qc = cold_cp*((reactor_t_c-min_approach_c)-feed_t_c)
    q = max(0.0,min(qh,qc))

    hot_out = reactor_t_c-q/hot_cp
    cold_out = feed_t_c+q/cold_cp
    d1 = reactor_t_c-cold_out
    d2 = hot_out-feed_t_c
    lmtd = d1 if abs(d1-d2)<1e-10 else (d1-d2)/math.log(d1/d2)
    area = (q*1000/3600)/(HX_U_W_M2_K*lmtd)

    baseline = cold_cp*(reactor_t_c-feed_t_c)
    furnace = cold_cp*(reactor_t_c-cold_out)

    if hot_out-feed_t_c < min_approach_c-1e-8 or reactor_t_c-cold_out < min_approach_c-1e-8:
        raise RuntimeError("Temperature approach constraint violated.")

    return {
        "q_recovered_kj_h":q, "hot_cp_kj_h_k":hot_cp,
        "cold_cp_kj_h_k":cold_cp, "hot_outlet_c":hot_out,
        "cold_outlet_c":cold_out, "lmtd_c":lmtd, "hx_area_m2":area,
        "furnace_duty_kj_h":furnace, "baseline_furnace_kj_h":baseline,
        "heat_recovery_savings_pct":100*q/baseline
    }

def run_case(reactor_t_c=BASE_REACTOR_T_C,conversion=None,feed_kg_h=FEED_KG_H):
    b=material_balance(feed_kg_h,conversion)
    h=heat_integration(reactor_t_c,b)
    return {"balance":b,"heat":h,"sulfur_spec_met":b.sulfur_ppm<=TARGET_SULFUR_PPM}
