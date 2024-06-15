import lotto_repo
import lotto_crawler

def migrate_all():
    print("로또 당첨번호 전체 수집을 시작합니다")
    latest_round = lotto_crawler.get_latest_round()
    if latest_round == 0:
        print("초기화 중 오류가 발생했습니다. 프로그램을 종료합니다.")
        exit(1)

    saved_count = 0
    err_count = 0
    skip_count = 0

    try:
        lotto_repo.begin()
        for i in range(1, int(latest_round) + 1):
            try:
                if lotto_repo.get_round(i):
                    skip_count += 1
                    continue
                print(f"{i}회차 당첨번호 저장 중...")
                lotto = lotto_crawler.get_lotto_summary(i)
                if lotto:
                    lotto_repo.save_round(lotto)
                    saved_count += 1
            except Exception as e:
                print(f"{i}회차 당첨번호 저장 중 오류 발생: {e}")
                err_count += 1

        # 트랜잭션 종료
        lotto_repo.commit()
        lotto_repo.finish()
    except Exception as e:
        print(f"트랜잭션 중 오류 발생: {e}")
        exit(1)

    print("로또 당첨번호 전체 수집이 완료되었습니다")
    print(f"저장: {saved_count}회, 중복: {skip_count}회, 오류: {err_count}회")

if __name__ == '__main__':
    migrate_all()