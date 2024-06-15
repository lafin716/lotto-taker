from bs4 import BeautifulSoup
import lxml.etree as etree
import requests
import utils as u

base_url = "https://www.dhlottery.co.kr/gameResult.do?method=byWin"

def get_lotto_summary(num):
    resp = requests.post(base_url, data={"drwNo": num})
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'lxml')
        tree = etree.HTML(str(soup))
        try:
            pick_date = tree.xpath('/html/body/div[3]/section/div/div[2]/div/div[2]/p')[0].text
            round = tree.xpath('/html/body/div[3]/section/div/div[2]/div/div[2]/h4/strong')[0].text
            win_nums = tree.xpath('/html/body/div[3]/section/div/div[2]/div/div[2]/div/div[1]/p/span')
            wins = [num.text for num in win_nums]
            bonus_num = tree.xpath('/html/body/div[3]/section/div/div[2]/div/div[2]/div/div[2]/p/span')[0].text
            total_sell_amount = tree.xpath('/html/body/div[3]/section/div/div[2]/div/ul/li[2]/strong')[0].text
            first_prize_winners = tree.xpath('/html/body/div[3]/section/div/div[2]/div/table/tbody/tr[1]/td[3]')[0].text
            first_prize_amount = tree.xpath('/html/body/div[3]/section/div/div[2]/div/table/tbody/tr[1]/td[2]/strong')[0].text
            first_prize_each = tree.xpath('/html/body/div[3]/section/div/div[2]/div/table/tbody/tr[1]/td[4]')[0].text

            return {
                "pick_date": u.clean_date(pick_date),
                "round": u.clean_round(round),
                "num1": wins[0],
                "num2": wins[1],
                "num3": wins[2],
                "num4": wins[3],
                "num5": wins[4],
                "num6": wins[5],
                "bonus": bonus_num,
                "total_sell_amount": u.clean_number(total_sell_amount),
                "first_prize_winners": u.clean_number(first_prize_winners),
                "first_prize_amount": u.clean_number(first_prize_amount),
                "first_prize_each": u.clean_number(first_prize_each)
            }
        except Exception as e:
            print(f"HTML 파싱 중 Error: {e}")
            return {}
    return {}

def get_latest_round():
    resp = requests.get(base_url)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'html.parser')
        latest_round = soup.select('.win_result h4 strong')[0].text
        return int(latest_round.replace("회", ""))
    return 0

def get_latest_round_summary():
    latest_round = get_latest_round()
    return get_lotto_summary(latest_round)

if __name__ == '__main__':
    print(get_lotto_summary(1))
    print(get_latest_round())