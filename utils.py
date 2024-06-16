import datetime
import random

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

def color_green(text):
    start_color = "\033[1;32m"
    end_color = "\033[0m"
    return f"{start_color}{text}{end_color}"

def color_red(text):
    start_color = "\033[1;31m"
    end_color = "\033[0m"
    return f"{start_color}{text}{end_color}"

def get_rank(match_count, bonus_match_count):
    if match_count == 6:
        return 1
    elif match_count == 5 and bonus_match_count == 1:
        return 2
    elif match_count == 5 and bonus_match_count == 0:
        return 3
    elif match_count == 4:
        return 4
    elif match_count == 3:
        return 5
    else:
        return 0

def pretty_print_my_lotto_raw(row, win_info=None):
    if not row:
        print("해당 정보가 없습니다.")
        return
    try:
        print_rows = []

        pick_type_label = "자동" if row['pick_type'] == '1' else "수동"
        print_rows.append(f"{pick_type_label} ")

        match_count = 0
        bonus_match_count = 0
        if win_info:
            main_win_nums = [win_info['num1'], win_info['num2'], win_info['num3'], win_info['num4'], win_info['num5'], win_info['num6']]
            bonus_num = win_info['bonus']
        else:
            main_win_nums = []
            bonus_num = 0

        for i in range(1, 7):
            num = row[f'num{i}']
            if num in main_win_nums:
                match_count += 1
                print_rows.append(color_green(zero_padding(num)))
            elif num == bonus_num:
                bonus_match_count += 1
                print_rows.append(color_red(zero_padding(num)))
            else:
                print_rows.append(zero_padding(num))

        rank = get_rank(match_count, bonus_match_count)
        if rank == 0:
            print_rows.append("(낙첨)")
        else:
            print_rows.append(f"({rank}등)")

        print(" ".join(print_rows))
        return match_count, bonus_match_count
    except Exception as e:
        print(f"출력 중 오류 발생: {e}")
        print(row)

def pretty_print_my_lottos(rows):
    if not rows:
        print("해당 정보가 없습니다.")
        return
    try:
        # 출력
        for round in sorted(rows.keys()):
            paper = rows[str(round)]
            print(f"제 {paper['round']} 회")
            print(f"추첨일 : {clean_date(paper['pick_date'])}")
            if 'win_info' in paper:
                win_info = paper['win_info']
                win_num_prints = []
                for i in range(1, 7):
                    win_num_prints.append(zero_padding(win_info[f'num{i}']))
                print(f"당첨번호: {' '.join(win_num_prints)}")
                print(f"보너스 번호: {win_info['bonus']}")

            total_match_count = 0
            total_bonus_match_count = 0
            for row in paper['rows']:
                match_count, bonus_match_count = pretty_print_my_lotto_raw(row, win_info)
                total_match_count += match_count
                total_bonus_match_count += bonus_match_count

            print(f"총 {total_match_count}개 일치, {total_bonus_match_count}개 보너스 일치")
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
