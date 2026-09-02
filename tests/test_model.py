import math
from src.config import *
from src.model import material_balance,heat_integration,run_case
from src.equipment import reactor_screen,pressure_drop_screen,compressor_power_screen
from src.optimization import grid_search

def test_feed_closes():
    assert math.isclose(sum(FEED_MASS_FRACTIONS.values()),1,abs_tol=1e-12)

def test_total_mass_balance():
    r=material_balance()
    assert math.isclose(r.feed_total_with_h2_kg_h,r.total_product_kg_h,rel_tol=1e-10,abs_tol=1e-8)

def test_sulfur_element_balance():
    r=material_balance()
    assert math.isclose(r.sulfur_in_kg_h-r.sulfur_out_kg_h,r.h2s_kmol_h*MW["S"],rel_tol=1e-10,abs_tol=1e-10)

def test_hydrogen_stoichiometry():
    r=material_balance()
    assert math.isclose(r.h2_fresh_kmol_h,r.h2_consumed_kmol_h*H2_EXCESS_FACTOR,rel_tol=1e-12)

def test_sulfur_specification():
    assert run_case()["balance"].sulfur_ppm<=TARGET_SULFUR_PPM

def test_heat_recovery_and_approach():
    h=run_case()["heat"]
    assert h["q_recovered_kj_h"]>0 and h["furnace_duty_kj_h"]>=0
    assert h["hot_outlet_c"]-FEED_T_C>=MIN_APPROACH_C-1e-8
    assert BASE_REACTOR_T_C-h["cold_outlet_c"]>=MIN_APPROACH_C-1e-8

def test_lmtd_and_area():
    h=run_case()["heat"]
    assert h["lmtd_c"]>0 and h["hx_area_m2"]>0 and h["hx_area_m2"] < 1000

def test_reactor_screen():
    x=reactor_screen()
    assert x["gross_reactor_volume_m3"]>x["catalyst_bed_volume_m3"]>0

def test_pressure_drop():
    x=pressure_drop_screen()
    assert x["pressure_drop_kpa"]>0 and x["reynolds"]>0

def test_compressor_power():
    assert compressor_power_screen(5)>0

def test_optimization():
    x=grid_search()
    assert x["sulfur_ppm"]<=TARGET_SULFUR_PPM and x["furnace_duty_mj_h"]>0

def test_deterministic():
    a=run_case(); b=run_case()
    assert a["balance"].sulfur_ppm==b["balance"].sulfur_ppm
    assert a["heat"]["hx_area_m2"]==b["heat"]["hx_area_m2"]

def test_low_conversion_fails_spec():
    x=run_case(conversion={"thiophene":0.90,"benzothiophene":0.90})
    assert not x["sulfur_spec_met"]

def test_infeasible_temperature_rejected():
    try:
        heat_integration(130,material_balance())
    except ValueError:
        return
    raise AssertionError("Infeasible exchanger temperature was not rejected.")
