from repo.lotto_repo import LottoRepo
from repo.my_lotto_repo import MyLottoRepo
from service.summary_service import SummaryService
import utils as u
import random

class SuggestService:
    def __init__(self):
        self.ratio = 13
        self.algorithm = 1
        self.lotto_repo = LottoRepo()
        self.my_lotto_repo = MyLottoRepo()
        self.summary_service = SummaryService()

    def get_suggest(self, round=None):
        round_info = self.summary_service.get_future_round()
        if round:
            round_info = self.lotto_repo.get_round(round)

        print(f"회차 : {round_info['round']}회차")
        print(f"추첨일 : {u.format_date(u.escape_date(round_info['pick_date']))}")

        bought_lottos = self.my_lotto_repo.get_round_all(round_info['round'])
        if not bought_lottos:
            nums = []
            for _ in range(5):
                nums.append(self.generate_lotto_nums())
            print("===================================")
            print("구매 이력이 없어 랜덤으로 생성합니다.")
            print("추천 번호입니다.")
            for num in nums:
                print(" ".join(u.zero_padding(n) for n in num))
            print("===================================")
            return True

        print("===================================")
        print("구매한 로또 정보를 기반으로 추천번호를 생성합니다.")
        # 테스트용 출력
        print(f"당첨번호 : {round_info['num1']} {round_info['num2']} {round_info['num3']} {round_info['num4']} {round_info['num5']} {round_info['num6']}")

        print("구매한 로또 번호")
        for lotto in bought_lottos:
            bought_lottos_text = []
            bought_lottos_text.append(f"{u.zero_padding(lotto['num1'])}")
            bought_lottos_text.append(f"{u.zero_padding(lotto['num2'])}")
            bought_lottos_text.append(f"{u.zero_padding(lotto['num3'])}")
            bought_lottos_text.append(f"{u.zero_padding(lotto['num4'])}")
            bought_lottos_text.append(f"{u.zero_padding(lotto['num5'])}")
            bought_lottos_text.append(f"{u.zero_padding(lotto['num6'])}")
            print(" ".join(bought_lottos_text))

        return self.get_suggest_by_algo(bought_lottos)

    def get_suggest_by_algo(self, bought_lottos):
        if self.algorithm == 1:
            return self.algorithm1(bought_lottos)
        else:
            return self.algorithm2(bought_lottos)

    # 첫번째 알고리즘
    def algorithm1(self, bought_lottos):
        used_lotto_idx = []
        suggest_results = []
        while len(suggest_results) < 5:
            rand = random.randint(0, len(bought_lottos) - 1)
            if rand in used_lotto_idx:
                continue
            base_lottos = bought_lottos[rand]
            used_lotto_idx.append(rand)

            suggest_nums = []
            for i in range(1, 7):
                suggest_nums.append(base_lottos[f'num{i}'])

            for i in range(6):
                suggest_nums[i] = self.calc_suggest_num(suggest_nums[i], suggest_nums)

            suggest_nums = sorted(suggest_nums)
            suggest_results.append(suggest_nums)
        return suggest_results

    def algorithm2(self, bought_lottos):
        suggest_results = []
        while len(suggest_results) < 5:
            suggest_nums = []
            while len(suggest_nums) < 6:
                rand = random.randint(0, len(bought_lottos) - 1)
                base_lottos = bought_lottos[rand]
                idx = random.randint(1, 6)
                num = base_lottos[f'num{idx}']
                if num not in suggest_nums:
                    suggest_nums.append(num)

            suggest_nums = sorted(suggest_nums)
            suggest_results.append(suggest_nums)
        print(suggest_results)
        return suggest_results

    def get_win_count(self, suggest_results, round_info):
        win_nums = [round_info[f'num{i}'] for i in range(1, 7)]
        bonus_num = round_info['bonus']
        rank_map = {}
        for suggest in suggest_results:
            match_count = 0
            bonus_match_count = 0
            for i in range(1, 7):
                if suggest[i - 1] in win_nums:
                    match_count += 1
                elif suggest[i - 1] == bonus_num:
                    bonus_match_count += 1
            rank = u.get_rank(match_count, bonus_match_count)
            if rank > 0:
                if rank not in rank_map:
                    rank_map[rank] = 0
                rank_map[rank] += 1

        return rank_map

    def calc_suggest_num(self, val, nums):
        fail_count = 0
        while True:
            if fail_count > 10:
                break
            tmp = val
            calc_type = self.get_random_calc()
            rand = self.get_random_ratio()
            if calc_type:
                if tmp != 45:
                    tmp += rand
            else:
                if tmp != 1:
                    tmp -= rand
            if tmp != val and tmp in nums:
                fail_count += 1
                continue
            if tmp > 45:
                fail_count += 1
                continue
            if tmp < 1:
                fail_count += 1
                continue
            val = tmp
            break

        return val

    def generate_lotto_nums(self):
        nums = []
        while len(nums) < 6:
            num = random.randint(1, 45)
            if num not in nums:
                nums.append(num)
        return sorted(nums)

    def get_random_ratio(self):
        return random.randint(0, self.ratio)

    def get_random_calc(self):
        r = random.randint(1, 2)
        if r == 1:
            return True
        else:
            return False

    def algo1_test(self):
        self.algorithm = 1
        bought_lottos = self.my_lotto_repo.get_round_all(1124)
        bought_lottos = bought_lottos[:5]
        win_info = self.lotto_repo.get_round(1123)

        prime_result = {}
        for r in range(8, 15):
            print("===================================")
            self.ratio = r
            print(f"ratio : {self.ratio}")
            total_map = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            for i in range(50000):
                suggest_results = self.get_suggest_by_algo(bought_lottos)
                win_count = self.get_win_count(suggest_results, win_info)
                for k, v in win_count.items():
                    total_map[k] += v
                if i > 0 and i % 10000 == 0:
                    print(f"{i}회차")

            for k, v in total_map.items():
                if k <= 2 and v > 0:
                    if self.ratio not in prime_result:
                        prime_result[self.ratio] = {}

                    if k not in prime_result[self.ratio]:
                        prime_result[self.ratio][k] = 0

                    prime_result[self.ratio][k] = v
                print(f"{k}등 : {v}회")
        print("===================================")
        for k, v in prime_result.items():
            print(f"ratio : {k}", end=" ")
            for k2, v2 in v.items():
                print(f"{k2}등 : {v2}회", end=" ")
            print()

    def algo2_test(self):
        self.algorithm = 2
        bought_lottos = self.my_lotto_repo.get_round_all(1124)
        bought_lottos = bought_lottos[:5]
        win_info = self.lotto_repo.get_round(1124)
        total_map = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for i in range(100000):
            suggest_results = self.get_suggest_by_algo(bought_lottos)
            win_count = self.get_win_count(suggest_results, win_info)
            for k, v in win_count.items():
                total_map[k] += v
            if i > 0 and i % 50000 == 0:
                print(f"{i}회차")

        for k, v in total_map.items():
            print(f"{k}등 : {v}회")


if __name__ == "__main__":
    suggest_service = SuggestService()
    suggest_service.algo1_test()
    #suggest_service.algo2_test()

    print("===================================")