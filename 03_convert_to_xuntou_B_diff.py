from setup import *
from configure import *
from class_custom import convert_mkt_code, convert_contract_code
from class_custom import split_xuntou_instruction

'''                           
created @ 2021-04-30
updated @ 2021-05-31
0.  this script has not been actually ran, just prepared for future usage
updated @ 2021-08-31
0.  this script has been tested on 20210730 and 20210831, so far so good.         
'''

print(SEP_LINE_EQ)

this_exe_date = sys.argv[1]
n_batch = int(sys.argv[2])

if not os.path.exists(OPERATION_XUNTOU_U_DISK_DIR):
    print("| {} | U disk is not ready! Please check again.|".format(dt.datetime.now()))
    sys.exit()

diff_file = "{}.position.diff.csv".format(this_exe_date)
diff_path = os.path.join(position_diff_dir, diff_file)
df = pd.read_csv(diff_path)
df = df.sort_values(by=["operation", "contract"], ascending=True)

for op, op_df in df.groupby(by="operation"):
    sub_df = op_df.copy()  # type:pd.DataFrame
    sub_df["代码"], sub_df["市场"] = zip(*sub_df.apply(lambda z: z["contract"].split("."), axis=1))
    sub_df["市场"] = sub_df["市场"].map(convert_mkt_code)
    sub_df["代码"] = sub_df[["市场", "代码"]].apply(convert_contract_code, axis=1)
    sub_df["数量"] = np.abs(sub_df["quantity"])
    sub_df["相对权重"] = 1
    sub_df = sub_df[["代码", "市场", "数量", "相对权重"]]  # type:pd.DataFrame

    if op in ["buy_open", "buy_close"]:
        sub_df["方向"] = 0

    if op in ["sell_open", "sell_close"]:
        sub_df["方向"] = 1

    sub_lbl = {
        "buy_close": "买入平仓",
        "buy_open": "买入开仓",
        "sell_close": "卖出平仓",
        "sell_open": "卖出开仓",
    }[op]

    sub_file = "{}_LTRR_{}_DIFF_{}.csv".format(gid, this_exe_date, sub_lbl)
    sub_path = os.path.join(OPERATION_XUNTOU_DIR, sub_file)
    u_disk_sub_path = os.path.join(OPERATION_XUNTOU_U_DISK_DIR, sub_file)
    sub_df.to_csv(sub_path, index=False)
    sub_df.to_csv(u_disk_sub_path, index=False)

    print("| {0} | diff position conversion | execute date = {1} | {2:>10s} | succeed |".format(dt.datetime.now(), this_exe_date, op))
    print(SEP_LINE_DS)

    split_xuntou_instruction(t_src_path=sub_path, t_n_batch=n_batch)
    split_xuntou_instruction(t_src_path=u_disk_sub_path, t_n_batch=n_batch)
