from dataclasses import dataclass

MW = {"C":12.011, "H":1.008, "S":32.06}
H2_MW = 2*MW["H"]
H2S_MW = 2*MW["H"] + MW["S"]

def mw(c,h,s=0):
    return c*MW["C"] + h*MW["H"] + s*MW["S"]

@dataclass(frozen=True)
class Component:
    name: str
    formula: str
    mw: float
    sulfur_mass_fraction: float
    cp_kj_kg_k: float

COMPONENTS = {
    "n_hexane": Component("n_hexane","C6H14",mw(6,14),0,2.30),
    "n_heptane": Component("n_heptane","C7H16",mw(7,16),0,2.35),
    "n_octane": Component("n_octane","C8H18",mw(8,18),0,2.40),
    "thiophene": Component("thiophene","C4H4S",mw(4,4,1),MW["S"]/mw(4,4,1),1.80),
    "benzothiophene": Component("benzothiophene","C8H6S",mw(8,6,1),MW["S"]/mw(8,6,1),1.60),
    "butane": Component("butane","C4H10",mw(4,10),0,2.20),
    "ethylbenzene": Component("ethylbenzene","C8H10",mw(8,10),0,1.70),
    "H2S": Component("H2S","H2S",H2S_MW,MW["S"]/H2S_MW,1.10),
}

FEED_MASS_FRACTIONS = {
    "n_hexane":0.35, "n_heptane":0.30, "n_octane":0.315,
    "thiophene":0.02, "benzothiophene":0.015
}

FEED_KG_H = 3000.0
FEED_T_C = 40.0
REACTOR_P_BAR = 40.0
BASE_REACTOR_T_C = 350.0
BASE_CONVERSION = {"thiophene":0.9999, "benzothiophene":0.9998}
H2_EXCESS_FACTOR = 1.25
MIN_APPROACH_C = 20.0
HOT_OUTLET_C = 120.0
TARGET_SULFUR_PPM = 10.0

REACTIONS = {
    "thiophene":{"h2_per_kmol":4.0,"product":"butane"},
    "benzothiophene":{"h2_per_kmol":3.0,"product":"ethylbenzene"},
}

LIQUID_DENSITY_KG_M3 = 700.0
REACTOR_LHSV_HR = 3.0
REACTOR_VOID_FRACTION = 0.40
HX_U_W_M2_K = 250.0
FUEL_LHV_MJ_KG = 50.0
FUEL_COST_USD_KG = 0.55
FUEL_CO2_KG_KG = 3.15
ANNUAL_OPERATING_HOURS = 8000
COMPRESSOR_EFFICIENCY = 0.72
R_GAS_J_MOL_K = 8.314462618
