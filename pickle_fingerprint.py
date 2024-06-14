from pathlib import Path
import functools
import operator
import pandas
import pickle

# Add custom explore tool
import sys
LIB_PATH = Path(
    "C:/Data/Documents/python_projects/custom_libraries")
sys.path.append(LIB_PATH.__str__())
import dndm_tools

PATH_TO_MAT_FILES = Path("reference_data/traces/mat_files/")
PERIPHERALS = [
    "AUR",
    "APA",
    "ALR",
    "LL1",
    "LL2",
    "SLR",
    "VPA",
    "SUR"
]

"""
Pickle a machine's reference fingerprint in format dict[peripheral][test_cycle][repeat_cycle] = DataFrame(time, trace_1, trace_n).
"""
d = dict.fromkeys(PERIPHERALS)
for peripheral_key in d.keys():
    # d["AUR"]

    # Get the test cycle names dynamically
    test_cycles = list(PATH_TO_MAT_FILES.glob(f"default_{peripheral_key}*cycle_1*"))
    test_cycles = ["_".join(cycle.stem.split("_")[1:4]) for cycle in test_cycles]

    # Initialise 2nd level of dictionary: Test Cycles
    d[peripheral_key] = dict.fromkeys(test_cycles)
    for test_cycle_key in d[peripheral_key].keys():
        # d["AUR"]["AUR_APA_LL2top"]

        # Get the repeat cycle names statically.
        d[peripheral_key][test_cycle_key] = dict.fromkeys(["cycle_1", "cycle_2", "cycle_3", "cycle_4", "cycle_5"])
        for repeat_cycle_key in d[peripheral_key][test_cycle_key].keys():
            # d["AUR"]["AUR_APA_LL2top"]["cycle_1"]
            print(f"{peripheral_key}\t{test_cycle_key}\t{repeat_cycle_key}")

            # Fetch the trace file that belongs in this field of the dict
            path = next(PATH_TO_MAT_FILES.glob(f"default_{test_cycle_key}_{repeat_cycle_key}*"))
            trace = dndm_tools.load_mat(path)["fileTosave"]

            # Initialise the DataFrame that will be the value of this dictionary field
            trace_df = pandas.DataFrame(index=trace["time"])
            for trace_name in trace['struct']:
                # CG_wafhnd.SENSOR.fdsjkf

                # Navigate through the MAT trace structure, to the signal's data
                trace_name = trace_name.rstrip()
                signal_path = trace_name.split(".")
                trace_df[trace_name] = functools.reduce(operator.getitem, signal_path, trace)

            # The DataFrame is now complete; assign it to the dictionary.
            d[peripheral_key][test_cycle_key][repeat_cycle_key] = trace_df

# Dump the dictionary as a pickle file
with open("reference_data/fingerprint_BTR4.pickle", "wb") as f:
    pickle.dump(d, f)
