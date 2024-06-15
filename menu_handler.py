import lotto_crawler
import lotto_mig
import lotto_repo
import lotto_stats
import utils as u

def handle(selected_menu):
    if selected_menu == "1":
        row = lotto_repo.get_latest_round()
        print("===================================")
        print("DB에 저장된 최신 회차 정보입니다.")
        u.pretty_print(row)
        print("===================================")

    elif selected_menu == "2":
        round = input("원하는 회차를 입력하세요: ")
        row = lotto_repo.get_round(round)
        if not row:
            print("해당 회차 정보가 없어 새로 수집합니다.")
            new_row = lotto_crawler.get_lotto_summary(round)
            if not new_row:
                print("로또 정보를 가져오는 데 실패했습니다. 다시 시도해주세요.")
                return True
            lotto_repo.save_round(new_row)
            row = lotto_repo.get_round(round)
            if not row:
                print("로또 정보를 저장하는데 실패했습니다. 다시 시도해주세요.")
                return True
        print("===================================")
        print(f"{round} 회차 정보입니다.")
        u.pretty_print(row)
        print("===================================")
    elif selected_menu == "3":
        lotto_mig.migrate_all()
    elif selected_menu == "4":
        all_data = lotto_repo.get_all()
        df = lotto_stats.make_df(all_data)
        print("===================================")
        print("전체 회차 간략 통계 분석 결과입니다.")
        print(df.describe())
        print("===================================")
    elif selected_menu == "0":
        print("인생역전 기원! Bye bye~")
        return False
    else:
        print("잘못된 입력입니다. 다시 입력해주세요.")
    print()
    return True
