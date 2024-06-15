
def format_price(price, decimal=0):
    format_str = '{:0,.%df}' % decimal
    return format_str.format(price)

def clean_date(date):
    return date.replace("(", "").replace(")", "").replace(" 추첨", "")

def clean_round(round):
    return int(round.replace("회", ""))

def clean_number(num):
    return int(num.replace(",", "").replace("원", ""))

def pretty_print(row):
    try:
        print_rows = []
        bought_row = row['total_sell_amount'] / 1000
        bought_paper = bought_row / 5
        print_rows.append(f"회차 : {row['round']}회")
        print_rows.append(f"추첨일 : {clean_date(row['pick_date'])}")
        print_rows.append(f"당첨번호: {row['num1']}, {row['num2']}, {row['num3']}, {row['num4']}, {row['num5']}, {row['num6']}")
        print_rows.append(f"보너스 번호: {row['bonus']}")
        print_rows.append(f"총 판매금액: {format_price(row['total_sell_amount'])}원")
        print_rows.append(f"총 판매량: {format_price(bought_paper)}매")
        print_rows.append(f"1등 당첨자 수: {row['first_prize_winners']}명")
        print_rows.append(f"1등 총 당첨금: {format_price(row['first_prize_amount'])}원")
        print_rows.append(f"1등 인당 수령액: {format_price(row['first_prize_each'])}원")
        print("\n".join(print_rows))
    except Exception as e:
        print(f"출력 중 오류 발생: {e}")
        print(row)

if __name__ == '__main__':
    print(format_price(1234567.123))
    print(format_price(1234567))
    print(format_price(0))
    print(format_price(10000))
    print(format_price(112))
    print(format_price(1123))
