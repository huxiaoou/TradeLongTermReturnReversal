import os
import pandas as pd


class CManagerMd(object):
    def __init__(self, t_src_data_dir: str, t_trade_date: str):
        md_dir = os.path.join(t_src_data_dir, t_trade_date[0:4], t_trade_date)
        md_dfs_list = []
        for md_file in os.listdir(md_dir):
            md_df = pd.read_csv(os.path.join(md_dir, md_file)).set_index("contract")
            md_dfs_list.append(md_df)
        self.m_md_df: pd.DataFrame = pd.concat(md_dfs_list, axis=0)
        self.m_trade_date = t_trade_date

    def get_price(self, t_contract: str, t_price_type: str):
        return self.m_md_df.at[t_contract, t_price_type]


def convert_mkt_code(x: str):
    if x == "SHF":
        return "SHFE"
    if x == "DCE":
        return "DCE"
    if x == "CZC":
        return "CZCE"
    return ""


def convert_contract_code(x: pd.Series):
    if x["市场"] == "CZCE":
        return x["代码"]
    else:
        return x["代码"].lower()


def split_quantity(t_qty: int, t_n_batch: int) -> list:
    # qty = m * n + r
    r = t_qty % t_n_batch
    m = t_qty // t_n_batch
    res = [m] * t_n_batch
    for i in range(r):
        res[i] += 1
    return res


def split_xuntou_instruction(t_src_path: str, t_n_batch: int) -> int:
    if os.path.exists(t_src_path):
        src_df = pd.read_csv(t_src_path)
        # split quantity
        split_data = {}
        for idx, quantity in zip(src_df.index, src_df["数量"]):
            split_data[idx] = split_quantity(t_qty=quantity, t_n_batch=t_n_batch)
        split_df = pd.DataFrame(split_data)
        # create batch instruction
        for bi in range(t_n_batch):
            batch_df = src_df.copy()
            batch_df["数量"] = split_df.loc[bi]
            batch_path = t_src_path.replace(".csv", "_BATCH{:02d}.csv".format(bi))
            batch_df.to_csv(batch_path, index=False)
    else:
        print("{} does not exist, program will skip this operation.".format(t_src_path))
    return 0
