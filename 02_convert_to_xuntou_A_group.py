from setup import *
from configure import *
from class_custom import convert_mkt_code, convert_contract_code
from class_custom import split_xuntou_instruction

'''
created @ 2021-04-30
'''

print(SEP_LINE_EQ)

execute_date = sys.argv[1]
n_batch = int(sys.argv[2])

if not os.path.exists(OPERATION_XUNTOU_U_DISK_DIR):
    print("| {} | U disk is not ready! Please check again.|".format(dt.datetime.now()))
    sys.exit()

standardize_position_file = "{}.{}.standardize.position.csv".format(gid, execute_date)
standardize_position_path = os.path.join(STANDARDIZE_POSITION_DIR, standardize_position_file)
df = pd.read_csv(standardize_position_path)

# reformat
df["代码"], df["市场"] = zip(*df.apply(lambda z: z["contract"].split("."), axis=1))
df["市场"] = df["市场"].map(convert_mkt_code)
df["代码"] = df[["市场", "代码"]].apply(convert_contract_code, axis=1)
df["数量"] = np.abs(df["trade_quantity"])
df["相对权重"] = 1
print(df)

df_lng = df[["代码", "市场", "数量", "相对权重", "direction"]].copy()  # type:pd.DataFrame
df_srt = df[["代码", "市场", "数量", "相对权重", "direction"]].copy()  # type:pd.DataFrame
df_lng["方向"] = 0  # in xuntou system, 0 for long
df_srt["方向"] = 1  # in xuntou system, 1 for short
df_lng.loc[df_lng["direction"] <= 0, "数量"] = 0
df_srt.loc[df_srt["direction"] >= 0, "数量"] = 0
df_lng = df_lng.drop(labels="direction", axis=1)
df_srt = df_srt.drop(labels="direction", axis=1)
print(df_lng)
print(df_srt)

lng_file = "{}_LTRR_{}_买入开仓.csv".format(gid, execute_date)
srt_file = "{}_LTRR_{}_卖出开仓.csv".format(gid, execute_date)
lng_path = os.path.join(OPERATION_XUNTOU_DIR, lng_file)
srt_path = os.path.join(OPERATION_XUNTOU_DIR, srt_file)
u_disk_lng_path = os.path.join(OPERATION_XUNTOU_U_DISK_DIR, lng_file)
u_disk_srt_path = os.path.join(OPERATION_XUNTOU_U_DISK_DIR, srt_file)
df_lng.to_csv(lng_path, index=False)
df_srt.to_csv(srt_path, index=False)
df_lng.to_csv(u_disk_lng_path, index=False)
df_srt.to_csv(u_disk_srt_path, index=False)

print("| {0} | daily position conversion | execute date = {1} | succeed |".format(dt.datetime.now(), execute_date))

split_xuntou_instruction(t_src_path=lng_path, t_n_batch=n_batch)
split_xuntou_instruction(t_src_path=srt_path, t_n_batch=n_batch)
split_xuntou_instruction(t_src_path=u_disk_lng_path, t_n_batch=n_batch)
split_xuntou_instruction(t_src_path=u_disk_srt_path, t_n_batch=n_batch)
