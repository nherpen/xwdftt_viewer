from pathlib import Path
import matplotlib.pyplot as plt
import pickle

PATH = Path("reference_data/fingerprint_BTR4_downsampled.pickle")
with open(PATH, 'rb') as f:
    d = pickle.load(f)

trace = d["AUR"]["AUR_APA_LL2top"]["cycle_1"]["WXRBxAUR.MeasSys.Kinematics.ODT_POS_PHI"] 
[plt.plot(p["WXRBxAUR.MeasSys.Kinematics.ODT_POS_PHI"], color="0.8") for p in d["AUR"]["AUR_APA_LL2top"].values()]
plt.plot(trace, linewidth=2.0)
plt.xlabel("Time [s]")
plt.ylabel("Phi [rad]")
plt.title('WXRBxAUR.MeasSys.Kinematics.ODT_POS_PHI')
plt.grid()
plt.tight_layout()
plt.show()

pass