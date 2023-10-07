import json
import commons
import requests


def get_ticker(cloud_sso_token, symbol):
    logger = commons.get_logger()
    p_code = 1

    url = "https://gw.datayes.com/rrp_adventure/web/stock/info?&ticker={symbol}".format(symbol=symbol)

    payload = {}
    headers = {
        'Cookie': 'cloud-sso-token={token}'.format(token=cloud_sso_token)
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    text = response.text
    result = json.loads(text)
    data = result["data"]
    p_code = result["code"]
    if p_code == -403:
        return None, p_code

    open_price = data["openPrice"]
    close = data["lastPrice"]
    low = data["lowestPrice"]
    high = data["highestPrice"]
    p_ticker = {
        "open": open_price,
        "close": close,
        "low": low,
        "high": high,
    }
    return p_ticker, p_code


if __name__ == "__main__":
    CLOUD_SSO_TOKEN = "47E109B86A046D8035827F262475B70B"
    ticker, code = get_ticker(CLOUD_SSO_TOKEN, "000001")

    s_logger = commons.get_logger()
    s_logger.info(ticker)
    pass
