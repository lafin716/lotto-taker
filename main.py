import lotto_crawler
import utils as u
import menu_handler as mh

def welcome():
    latest_round = lotto_crawler.get_latest_round_summary()
    if not latest_round:
        print("로또 정보를 가져오는 데 실패했습니다. 다시 시도해주세요.")
        return False

    print("로또 분석기에 오신 것을 환영합니다")
    print("===================================")
    u.pretty_print(latest_round)
    print("===================================")
    return True

def menu():
    print("===================================")
    print("원하는 기능을 입력해주세요.")
    print("1. 최신 저장 회차 확인")
    print("2. 원하는 회차 당첨번호 조회")
    print("3. 전체 회차 당첨번호 수집")
    print("4. 전체 회차 간략 통계 분석")
    print("0. 끝내기")
    print("===================================")
    return input("번호를 입력하세요: ")

def main():
    is_continue = True
    while is_continue:
        selected_menu = menu()
        is_continue = mh.handle(selected_menu)

if __name__ == '__main__':
    if welcome():
        main()

