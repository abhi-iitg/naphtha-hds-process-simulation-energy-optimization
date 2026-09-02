import math
from .config import *

def reactor_screen():
    liquid_m3_h=FEED_KG_H/LIQUID_DENSITY_KG_M3
    catalyst=liquid_m3_h/REACTOR_LHSV_HR
    gross=catalyst/(1-REACTOR_VOID_FRACTION)
    return {"liquid_feed_m3_h":liquid_m3_h,"catalyst_bed_volume_m3":catalyst,"gross_reactor_volume_m3":gross}

def pressure_drop_screen(flow_kg_h=FEED_KG_H,diameter_m=0.10,length_m=5.0,
                         density_kg_m3=700.0,viscosity_pa_s=0.0004,roughness_m=4.5e-5):
    area=math.pi*diameter_m**2/4
    velocity=(flow_kg_h/3600)/density_kg_m3/area
    Re=density_kg_m3*velocity*diameter_m/viscosity_pa_s
    f=64/Re if Re<2300 else 0.25/(math.log10(roughness_m/(3.7*diameter_m)+5.74/(Re**0.9))**2)
    dp=f*(length_m/diameter_m)*(density_kg_m3*velocity**2/2)
    return {"velocity_m_s":velocity,"reynolds":Re,"friction_factor":f,"pressure_drop_kpa":dp/1000}

def compressor_power_screen(h2_kmol_h,suction_bar=5.0,discharge_bar=40.0,
                            temperature_k=313.15,efficiency=COMPRESSOR_EFFICIENCY):
    n=h2_kmol_h*1000/3600
    w=n*R_GAS_J_MOL_K*temperature_k*math.log(discharge_bar/suction_bar)/efficiency
    return w/1000
