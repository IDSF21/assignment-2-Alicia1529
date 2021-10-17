import pandas as pd
import numpy as np


district_mapping = {
    "静安": "Jingan",
    "长宁": "Changning",
    "徐汇": "Xuhui",
    "浦东": "Pudong",
    "黄浦": "Huangpu",
    "虹口": "Hongkou",
    "杨浦": "Yangpu",
    "闸北": "Zhabei",
    "普陀": "Putuo",
    "闵行": "Minhang",
    "宝山": "Baoshan",
    "嘉定": "Jiading",
    "松江": "Songjiang",
    "青浦": "Qingpu",
}

def parseArea(x):
    return float(x.strip("平米"))

def parseYear(x):
    try:
        return int(x[:4])
    except:
        return 0

def mapDistrict(x):
    return district_mapping.get(x, "NA")

def mapArea(x):
    return x // 5 * 5

# Index(["标题", "小区名称", "户型", "面积", "朝向", "装修", "电梯", "楼层", "层数", "年代", "板楼",
#        "成交时间", "成交价格", "单价", "方式", "城市", "区域", "板块", "地铁", "bdx", "bdy",
#        "gpsx", "gpsy"])
def load_data(filename):
    data = pd.read_csv(filename)[["面积", "成交价格", "成交时间", "单价", "区域", "gpsx", "gpsy"]]
    print(data.shape)

    data = data.drop_duplicates()
    data = data.dropna()

    data = data.rename({
        "面积": "Area", "成交时间": "Year", "成交价格": "TotalPrice",
        "单价": "UnitPrice", "区域": "District",
        "gpsx": "lon", "gpsy": "lat"}, axis="columns")
    
    # parse area
    data["Area"] = data["Area"].apply(parseArea)

    # parse year and remove columns with invalid year
    data["Year"] = data["Year"].apply(parseYear)
    data = data[data["Year"] != 0]

    # map District from Chinese to English and remove invalid ones
    data["District"] = data["District"].apply(mapDistrict)
    data = data[data["District"] != "NA"]

    return data

def get_avg_unit_price_by_district(df):
    unit_price_df = df.groupby('District')[["UnitPrice"]].mean()
    unit_price_df['District'] = unit_price_df.index
    unit_price_df["UnitPrice"] = unit_price_df["UnitPrice"].astype(int)
    return unit_price_df

def get_avg_unit_price_by_area_year(df):
    unit_price_df = df.copy()
    unit_price_df["Area"] = unit_price_df["Area"].apply(mapArea).astype(int)
    unit_price_df = unit_price_df.groupby(['Area', 'Year'])[["UnitPrice"]].mean()
    unit_price_df["UnitPrice"] = unit_price_df["UnitPrice"].astype(int)

    unit_price_df["Area"] = unit_price_df.index.get_level_values(0)
    unit_price_df["Year"] = unit_price_df.index.get_level_values(1)

    return unit_price_df


if __name__ == "__main__":
    filename = "house_data.csv"
    data = load_data(filename)
    print(data.columns)
    print(data.shape)
    print(data.head(5))

    unit_price_by_district = get_avg_unit_price_by_district(data)
    print(unit_price_by_district)
    
    unit_price_by_area_year = get_avg_unit_price_by_area_year(data)
