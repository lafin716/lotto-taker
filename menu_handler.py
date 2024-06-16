import lotto_crawler
import lotto_mig
import lotto_stats
import utils as u
from repo.lotto_repo import LottoRepo
from repo.my_lotto_repo import MyLottoRepo


class MenuHandler:
    def __init__(self):
        self.lotto_repo = LottoRepo()
        self.my_lotto_repo = MyLottoRepo()

    def latest_saved_round(self):
        row = self.lotto_repo.get_latest_round()
        print("===================================")
        print("DB에 저장된 최신 회차 정보입니다.")
        u.pretty_print(row)
        print("===================================")

    def specific_round(self):
        round = input("원하는 회차를 입력하세요: ")
        row = self.get_specific_round(round)
        if not row:
            return True
        print("===================================")
        print(f"{round} 회차 정보입니다.")
        u.pretty_print(row)
        print("===================================")

    def get_specific_round(self, round):
        row = self.lotto_repo.get_round(round)
        if not row:
            print("해당 회차 정보가 없어 새로 수집합니다.")
            new_row = lotto_crawler.get_lotto_summary(round)
            if not new_row:
                print("해당 회차 정보가 없습니다.")
                return False
            self.lotto_repo.save_round(new_row)
            row = self.lotto_repo.get_round(round)
            if not row:
                print("로또 정보를 저장하는데 실패했습니다. 다시 시도해주세요.")
                return False
        return row

    def simple_summary(self):
        all_data = self.lotto_repo.get_all()
        df = lotto_stats.make_df(all_data)
        print("===================================")
        print("전체 회차 간략 통계 분석 결과입니다.")
        print(df.describe())
        print("===================================")

    def get_future_round(self):
        latest_round = lotto_crawler.get_latest_round_summary()
        raw_date = u.escape_date(latest_round['pick_date'])
        # 날짜타입으로 변환 후 7일 더하기
        future_date = u.add_days(raw_date, 7)
        return {
            'round': latest_round['round'] + 1,
            'pick_date': future_date,
        }

    def bulk_add_my_lotto(self):
        count = input("몇 개의 로또를 추가하시겠습니까? ")
        for _ in range(int(count)):
            self.add_my_lotto()
        print(f"{count}개의 로또 정보가 저장되었습니다.")

    def bulk_add_before_my_lotto(self):
        round = input("원하는 회차를 입력하세요: ")
        count = input("몇 개의 로또를 추가하시겠습니까? ")
        for _ in range(int(count)):
            self.add_my_lotto(round=round)
        print(f"{count}개의 로또 정보가 저장되었습니다.")

    def add_my_lotto(self, round=None):
        pick_type = input("구입 방법을 입력하세요 (1. 자동, 2. 수동): ")
        nums = u.input_lotto_num_row()
        nums.sort()
        num1, num2, num3, num4, num5, num6 = nums

        if not round:
            future_round = self.get_future_round()
            round = future_round['round']
            pick_date = future_round['pick_date']
        else:
            round = round
            pick_date = lotto_crawler.get_lotto_summary(round)['pick_date']

        row = {
            'round': round,
            'pick_date': pick_date,
            'pick_type': pick_type,
            'num1': num1,
            'num2': num2,
            'num3': num3,
            'num4': num4,
            'num5': num5,
            'num6': num6,
        }
        self.my_lotto_repo.save_round(row)
        print("내 로또 정보가 저장되었습니다.")

    def show_all_my_lotto(self):
        rows = self.my_lotto_repo.get_all()
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

        # 라운드별 당첨번호 조회
        for round in sorted(lotto_map.keys()):
            win_info = self.get_specific_round(round)
            if not win_info:
                continue
            lotto_map[str(round)]["win_info"] = win_info

        print("===================================")
        print("구매한 전체 로또 정보입니다.")
        u.pretty_print_my_lottos(lotto_map)
        print("===================================")

    def show_round_my_lotto(self):
        round = input("원하는 회차를 입력하세요: ")
        rows = self.my_lotto_repo.get_round_all(round)
        if not rows:
            print("해당 회차에 구매한 정보가 없습니다.")
            return True

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

        # 라운드별 당첨번호 조회
        for round in sorted(lotto_map.keys()):
            win_info = self.get_specific_round(round)
            if not win_info:
                continue
            lotto_map[str(round)]["win_info"] = win_info

        print("===================================")
        print(f"{round} 회차 로또 정보입니다.")
        u.pretty_print_my_lottos(lotto_map)
        print("===================================")

    def find_my_lotto_been_corrected(self):
        print("내가 구매한 모든 로또 번호가 역대 당첨번호와 일치하는지 확인합니다.")
        all_wins = self.lotto_repo.get_all()
        all_my_lottos = self.my_lotto_repo.get_all()
        match_stats = {}
        for win in all_wins:
            win_nums = [win[f'num{i}'] for i in range(1, 7)]
            bonus_num = win['bonus']
            match_count = 0
            bonus_match_count = 0
            for my_lotto in all_my_lottos:
                for i in range(1, 7):
                    num = my_lotto[f'num{i}']
                    if num in win_nums:
                        match_count += 1
                    elif num == bonus_num:
                        bonus_match_count += 1
                rank = u.get_rank(match_count, bonus_match_count)
                if rank > 0:
                    if str(rank) not in match_stats:
                        match_stats[str(rank)] = 0
                    match_stats[str(rank)] += 1
                    if rank == 1:
                        print(f"구매 : {my_lotto['round']}회차, 추첨 : {win['round']} 회차 {my_lotto['num1']} {my_lotto['num2']} {my_lotto['num3']} {my_lotto['num4']} {my_lotto['num5']} {my_lotto['num6']} {rank}등 당첨")
                match_count = 0
                bonus_match_count = 0
        print("===================================")
        for rank, count in sorted(match_stats.items()):
            print(f"{rank}등 당첨 : {count}회")
        print("모든 로또를 확인했습니다.")


    def get_menu_data(self):
        return [
            {'label': "내 로또 추가", 'action': self.bulk_add_my_lotto},
            {'label': "특정 회차 구매 로또 추가", 'action': self.bulk_add_before_my_lotto},
            {'label': "구매한 전체 로또 당첨여부 조회", 'action': self.show_all_my_lotto},
            {'label': "특정 회차 로또 당첨여부 조회", 'action': self.show_round_my_lotto},
            {'label': "예전 회차 전체 로또 당첨 확인", 'action': self.find_my_lotto_been_corrected},
            {'label': "최신 저장 회차 확인", 'action': self.latest_saved_round},
            {'label': "원하는 회차 당첨번호 조회", 'action': self.specific_round},
            {'label': "전체 회차 당첨번호 수집", 'action': lotto_mig.migrate_all},
            {'label': "전체 회차 간략 통계 분석", 'action': self.simple_summary},
        ]

    def ask_menu(self):
        print("===================================")
        print("원하는 기능을 입력해주세요.")
        menu_data = self.get_menu_data()
        for idx, menu in enumerate(menu_data):
            print(f"{idx + 1}. {menu['label']}")
        print("0. 종료")
        print("===================================")
        return input("번호를 입력하세요: ")

    def contains_menu(self, selected_menu):
        menu_data = self.get_menu_data()
        return menu_data[selected_menu]

    def handle(self, selected_menu):
        menu_data = self.get_menu_data()
        selected = int(selected_menu)
        if selected_menu == '0':
            print("인생역전 기회! 다음에 또 만나요.")
            return False

        if not self.contains_menu(selected - 1):
            print("잘못된 번호를 입력하셨습니다. 다시 입력해주세요.")
            return True

        menu_data[selected - 1]['action']()
        return True
