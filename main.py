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

def main():
    is_continue = True
    handler = mh.MenuHandler()
    while is_continue:
        selected_menu = handler.ask_menu()
        is_continue = handler.handle(selected_menu)

if __name__ == '__main__':
    if welcome():
        main()

