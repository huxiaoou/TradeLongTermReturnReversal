from setup import *
from configure import *
from skyrim.whiterun import CCalendar

'''
updated @ 2021-04-30
0.  standardize position as input
1.  both this date and prev date are set manually

updated @ 2021-05-31
0.  this script has not been actually ran, just prepared for future usage

updated @ 2021-06-30
0.  this script has been tested on G0015, between 20210531 and 20210630
'''

print(SEP_LINE_EQ)

this_exe_date = sys.argv[1]
prev_exe_date = sys.argv[2]

# ------ step 0: load data
this_file = "{}.{}.standardize.position.csv".format(gid, this_exe_date)
this_path = os.path.join(STANDARDIZE_POSITION_DIR, this_file)
if not os.path.exists(this_path):
    print("| {} | this date = {} | No file available, this script will terminate at once |".format(dt.datetime.now(), this_exe_date))
    sys.exit()
this_df = pd.read_csv(this_path).set_index(["contract", "direction"])
this_data: dict = this_df.to_dict(orient="index")
print(this_df)

print(SEP_LINE_DS)
prev_file = "{}.{}.standardize.position.csv".format(gid, prev_exe_date)
prev_path = os.path.join(STANDARDIZE_POSITION_DIR, prev_file)
if not os.path.exists(prev_path):
    print("| {} | prev date = {} | No file available, this script will terminate at once |".format(dt.datetime.now(), this_exe_date))
    sys.exit()
prev_df = pd.read_csv(prev_path).set_index(["contract", "direction"])
prev_data: dict = prev_df.to_dict(orient="index")
print(prev_df)

# ------ step 1: find operation
diff_list = []
# --- in prev not in this
for contract, direction in prev_data:
    if (contract, direction) not in this_data:
        diff_item = {
            "contract": contract,
            "operation": "buy_close" if direction < 0 else "sell_close",
            "quantity": prev_data[(contract, direction)]["trade_quantity"],
        }
        diff_list.append(diff_item)

# --- in this not in prev
for contract, direction in this_data:
    if (contract, direction) not in prev_data:
        diff_item = {
            "contract": contract,
            "operation": "buy_open" if direction > 0 else "sell_open",
            "quantity": this_data[(contract, direction)]["trade_quantity"],
        }
        diff_list.append(diff_item)

# --- in prev and in this
for contract, direction in this_data:
    if (contract, direction) in prev_data:
        this_quantity = this_data[(contract, direction)]["trade_quantity"]
        prev_quantity = prev_data[(contract, direction)]["trade_quantity"]
        delta_quantity = this_quantity - prev_quantity
        if delta_quantity > 0:
            if direction > 0:  # long open
                diff_item = {
                    "contract": contract,
                    "operation": "buy_open",
                    "quantity": delta_quantity,
                }
                diff_list.append(diff_item)
            elif direction < 0:  # 8 short open
                diff_item = {
                    "contract": contract,
                    "operation": "sell_open",
                    "quantity": delta_quantity,
                }
                diff_list.append(diff_item)
            else:
                pass

        if delta_quantity < 0:
            if direction > 0:  # long close
                diff_item = {
                    "contract": contract,
                    "operation": "sell_close",
                    "quantity": -delta_quantity,
                }
                diff_list.append(diff_item)
            elif direction < 0:  # short close
                diff_item = {
                    "contract": contract,
                    "operation": "buy_close",
                    "quantity": -delta_quantity,
                }
                diff_list.append(diff_item)
            else:
                pass

diff_df = pd.DataFrame(diff_list)
diff_df = diff_df.sort_values(by=["operation", "contract"], ascending=True)
diff_file = "{}.position.diff.csv".format(this_exe_date)
diff_path = os.path.join(position_diff_dir, diff_file)
diff_df.to_csv(diff_path, index=False)
print("| {0} | diff position | this_exe_date = {1} | prev_exe_date = {2} | calculated |".format(
    dt.datetime.now(), this_exe_date, prev_exe_date))

# --- check
merge_df = pd.merge(
    left=prev_df[["trade_quantity"]],
    right=this_df[["trade_quantity"]],
    left_index=True, right_index=True,
    how="outer", suffixes=["_" + prev_exe_date, "_" + this_exe_date]
)  # type:pd.DataFrame
merge_file = "{}.execute.merged.csv".format(this_exe_date)
merge_path = os.path.join(position_diff_dir, merge_file)
merge_df.to_csv(merge_path, index_label=["contract", "direction"])
print(SEP_LINE_DS)
print(merge_df)
print(SEP_LINE_DS)
print(diff_df)
