import json
import commons
import requests
import pandas as pd


def get_stock_info(cloud_sso_token):
    logger = commons.get_logger()
    code = 1

    # 合并两个 DataFrame，并覆盖前面的数据
    all_df = pd.DataFrame({})
    for i in range(10):
        logger.info("正在下载第{t}批".format(t=i + 1))
        url = "https://gw.datayes.com/rrp_adventure/web/stocks?size=10000&key={key}".format(key=i)

        payload = {}
        headers = {
            'Cookie': 'cloud-sso-token={token}'.format(token=cloud_sso_token)
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        text = response.text
        result = json.loads(text)
        data = result["data"]
        code = result["code"]
        if code == -403:
            return None, code

        df = pd.DataFrame(data)
        df = df[['tickerSymbol', 'stockName']]

        # 使用正则表达式匹配 tickerSymbol 开头为数字的行
        pattern = r'^\d'
        df = df[df['tickerSymbol'].str.match(pattern)]

        all_df = pd.concat([all_df, df], ignore_index=True).drop_duplicates(subset='tickerSymbol', keep='last')
        # 合并两个 DataFrame，并覆盖前面的数据

    # 按照 "id" 列进行排序
    all_df = all_df.sort_values('tickerSymbol')
    # 将列转换为字符串类型
    all_df['tickerSymbol'] = all_df['tickerSymbol'].astype(str)
    return all_df, code


if __name__ == "__main__":
    CLOUD_SSO_TOKEN = "47E109B86A046D8035827F262475B70B"
    s_df = get_stock_info(CLOUD_SSO_TOKEN)

    s_logger = commons.get_logger()
    s_logger.info(s_df)
    pass
