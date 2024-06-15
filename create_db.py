import sqlite3

def create_table():
    conn = sqlite3.connect('lotto.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lotto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pick_date TEXT,
        round INTEGER,
        num1 INTEGER,
        num2 INTEGER,
        num3 INTEGER,
        num4 INTEGER,
        num5 INTEGER,
        num6 INTEGER,
        bonus INTEGER,
        total_sell_amount INTEGER,
        first_prize_winners INTEGER,
        first_prize_amount INTEGER,
        first_prize_each INTEGER
    )
    ''')

    conn.commit()
    conn.close()

def drop_table():
    conn = sqlite3.connect('lotto.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS lotto')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()
    print("테이블 생성 완료")