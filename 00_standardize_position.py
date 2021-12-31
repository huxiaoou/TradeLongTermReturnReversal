from setup import *
from configure import *
from class_custom import CManagerMd

"""
notes:
0.  2021-09-30 one day delayed, signals and execution orders are actually calculated
    at 2021-10-08.
"""

print(SEP_LINE_EQ)

# load raw calendar
execute_date = sys.argv[1]

# load calendar
cne_calendar = CCalendar(t_path=SKYRIM_CONST_CALENDAR_PATH)
prev_date = cne_calendar.get_next_date(t_this_date=execute_date, t_shift=-1)

# load prev_date
manager_md = CManagerMd(t_src_data_dir=src_md_dir, t_trade_date=prev_date)

# load general tools
instrument_info_tab = CInstrumentInfoTable(t_path=SKYRIM_CONST_INSTRUMENT_INFO_PATH, t_index_label="windCode")

# load input
input_file = "{}.{}.input.csv".format(gid, execute_date)
input_path = os.path.join(INPUT_DIR, input_file)
input_df = pd.read_csv(input_path)

# calculate position
input_df["instrument"] = input_df["contract"].map(parse_instrument_from_contract_wind)
input_df["multiplier"] = input_df["instrument"].map(lambda z: instrument_info_tab.get_multiplier(t_instrument_id=z))
input_df["prev_close"] = input_df["contract"].map(lambda z: manager_md.get_price(t_contract=z, t_price_type="close"))
input_df["quantity"] = input_df["available_amt"] / input_df["multiplier"] / input_df["prev_close"]
input_df["trade_quantity"] = input_df["quantity"].map(lambda z: int(np.round(z)))

# save
standardize_position_df = input_df
standardize_position_file = "{}.{}.standardize.position.csv".format(gid, execute_date)
standardize_position_path = os.path.join(STANDARDIZE_POSITION_DIR, standardize_position_file)
standardize_position_df.to_csv(standardize_position_path, index=False, float_format="%.2f")

print(standardize_position_df)
