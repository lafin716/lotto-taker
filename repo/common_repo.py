import sqlite3
import os

# 이 파일은 데이터베이스 연결과 트랜잭션을 관리하는 공통 클래스를 정의합니다.
class CommonRepo:
    def __init__(self):
        self.use_trans = False
        self.trans_conn = None
        self.db_path = os.path.join(os.path.dirname(__file__), "..", "lotto.db")

    def connect(self):
        if self.use_trans:
            return self.trans_conn
        else:
            return sqlite3.connect(self.db_path)
    
    def begin(self):
        if self.trans_conn is None:
            self.trans_conn = self.connect()
            self.use_trans = True
        else:
            print("이미 트랜잭션을 시작했습니다.")
    
    def commit(self):
        if self.use_trans and self.trans_conn is not None:
            self.trans_conn.commit()
        else:
            print("트랜잭션을 시작하지 않았습니다.")
    
    def rollback(self):
        if self.use_trans and self.trans_conn is not None:
            self.trans_conn.rollback()
        else:
            print("트랜잭션을 시작하지 않았습니다.")
    
    def finish(self):
        if self.use_trans and self.trans_conn is not None:
            self.trans_conn.close()
            self.trans_conn = None
            self.use_trans = False
        else:
            print("트랜잭션을 시작하지 않았습니다.")
            
if __name__ == '__main__':
    common_repo = CommonRepo()
    common_repo.begin()
    common_repo.commit()
    common_repo.rollback()
    common_repo.finish()
    common_repo.rollback()