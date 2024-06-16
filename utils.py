import datetime

def format_price(price, decimal=0):
    format_str = '{:0,.%df}' % decimal
    return format_str.format(price)

def clean_date(date):
    return date.replace("(", "").replace(")", "").replace(" 추첨", "")

def escape_date(date):
    return date.replace(" ", "").replace("년", "-").replace("월", "-").replace("일", "")

def format_date(date):
    return date.replace("-", "년 ").replace("-", "월 ") + "일"

def clean_round(round):
    return int(round.replace("회", ""))

def clean_number(num):
    return int(num.replace(",", "").replace("원", ""))

def zero_padding(num):
    return f"{num:02}"

def pretty_print(row):
    if not row:
        print("해당 정보가 없습니다.")
        return
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

def pretty_print_my_lotto(row):
    if not row:
        print("해당 정보가 없습니다.")
        return
    try:
        print_rows = []
        print_rows.append(f"회차 : {row['round']}회")
        print_rows.append(f"추첨일 : {clean_date(row['pick_date'])}")
        print_rows.append(f"구입 방법: {'자동' if row['pick_type'] == '1' else '수동'}")
        print_rows.append(f"내 번호: {row['num1']}, {row['num2']}, {row['num3']}, {row['num4']}, {row['num5']}, {row['num6']}")
        print("\n".join(print_rows))
    except Exception as e:
        print(f"출력 중 오류 발생: {e}")
        print(row)

def pretty_print_my_lotto_raw(row):
    if not row:
        print("해당 정보가 없습니다.")
        return
    try:
        print_rows = []
        print_rows.append(f"{'자동' if row['pick_type'] == '1' else '수동'} [{row['num1']}] [{row['num2']}] [{row['num3']}] [{row['num4']}] [{row['num5']}] [{row['num6']}]")
        print("\n".join(print_rows))
    except Exception as e:
        print(f"출력 중 오류 발생: {e}")
        print(row)

def pretty_print_my_lottos(rows):
    if not rows:
        print("해당 정보가 없습니다.")
        return
    try:
        # 회차별로 묶어서 출력
        lotto_map = {}
        for row in rows:
            if str(row['round']) not in lotto_map:
                lotto_map[str(row['round'])] = {
                    'round': row['round'],
                    'pick_date': row['pick_date']
                }
            if 'rows' not in lotto_map[str(row['round'])]:
                lotto_map[str(row['round'])]['rows'] = []
            lotto_map[str(row['round'])]['rows'].append(row)

        # 출력
        for round in sorted(lotto_map.keys()):
            paper = lotto_map[str(round)]
            print(f"제 {paper['round']} 회")
            print(f"추첨일 : {clean_date(paper['pick_date'])}")
            for row in paper['rows']:
                pretty_print_my_lotto_raw(row)
            print("===================================")
    except Exception as e:
        print(f"출력 중 오류 발생: {e}")
        print(row)

def input_lotto_num_row():
    valid_count = 0
    result = []
    while valid_count < 6:
        num = input(f"{valid_count + 1}번째 번호를 입력하세요: ")
        if not num.isdigit() or int(num) < 1 or int(num) > 45:
            print("1부터 45 사이의 숫자를 입력해주세요.")
            continue
        if num in result:
            print("이미 입력한 번호입니다.")
            continue
        result.append(num)
        valid_count += 1

    return result

def add_days(raw_date, days):
    datetime_obj = datetime.datetime.strptime(raw_date, '%Y-%m-%d')
    datetime_obj += datetime.timedelta(days=days)
    return datetime_obj.strftime('%Y-%m-%d')

if __name__ == "__main__":
    print(zero_padding(1))
    print(zero_padding(10))