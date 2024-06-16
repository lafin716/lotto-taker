import lotto_crawler
import utils as u
from repo.lotto_repo import LottoRepo
from repo.my_lotto_repo import MyLottoRepo


class SummaryService:
    def __init__(self):
        self.lotto_repo = LottoRepo()
        self.my_lotto_repo = MyLottoRepo()

    def get_future_round(self):
        latest_round = lotto_crawler.get_latest_round_summary()
        raw_date = u.escape_date(latest_round['pick_date'])
        # 날짜타입으로 변환 후 7일 더하기
        future_date = u.add_days(raw_date, 7)
        return {
            'round': latest_round['round'] + 1,
            'pick_date': future_date,
        }

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