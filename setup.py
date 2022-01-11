import os
import sys
import numpy as np
import pandas as pd
import datetime as dt
from skyrim.whiterun import CInstrumentInfoTable, CCalendar, parse_instrument_from_contract_wind
from skyrim.configurationOffice import SKYRIM_CONST_CALENDAR_PATH, SKYRIM_CONST_INSTRUMENT_INFO_PATH
from skyrim.winterhold import check_and_mkdir

pd.set_option("display.width", 0)

src_md_dir = os.path.join("E:\\", "Database", "Futures", "instrument_mkt_data")
PROJECT_DATA_DIR = os.path.join(".", "data")
INPUT_DIR = os.path.join(PROJECT_DATA_DIR, "input")
STANDARDIZE_POSITION_DIR = os.path.join(PROJECT_DATA_DIR, "standardize_position")
position_diff_dir = os.path.join(PROJECT_DATA_DIR, "position_diff")
OPERATION_XUNTOU_DIR = os.path.join(PROJECT_DATA_DIR, "xuntou_group")
OPERATION_XUNTOU_U_DISK_DIR = os.path.join("H:", "Trade", "xuntou_group")
