import sqlite3
import utils as u

use_trans = False
trans_conn = None

def get_all():
    global use_trans
    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lotto ORDER BY round ASC")
        rows = cursor.fetchall()
        if not use_trans:
            conn.close()
        return to_dict_all(rows) if rows else []
    except Exception as e:
        conn.close()
        return False

def get_latest_round():
    global use_trans
    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lotto ORDER BY round DESC LIMIT 1")
        row = cursor.fetchone()

        if not use_trans:
            conn.close()
        return to_dict(row) if row else []
    except Exception as e:
        conn.close()
        return False

def get_round(round):
    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM lotto WHERE round = {round}")
        result = cursor.fetchone()
        if not use_trans:
            conn.close()
        return to_dict(result)
    except Exception as e:
        conn.close()
        return False

def save_round(row):
    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute(f"""
            INSERT INTO lotto (round, pick_date, num1, num2, num3, num4, num5, num6, bonus, total_sell_amount, first_prize_winners, first_prize_amount, first_prize_each)
            VALUES ({row['round']}, '{row['pick_date']}', {row['num1']}, {row['num2']}, {row['num3']}, {row['num4']}, {row['num5']}, {row['num6']}, {row['bonus']}, {row['total_sell_amount']}, {row['first_prize_winners']}, {row['first_prize_amount']}, {row['first_prize_each']})
        """)

        if not use_trans:
            conn.commit()
            conn.close()
    except Exception as e:
        conn.close()
        return False

def delete_lotto_win(round):
    global use_trans
    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM lotto WHERE round = {round}")

        if not use_trans:
            conn.commit()
            conn.close()
    except Exception as e:
        conn.close()
        return False

def to_dict(row):
    return {
        "id": row[0],
        "pick_date": row[1],
        "round": row[2],
        "num1": row[3],
        "num2": row[4],
        "num3": row[5],
        "num4": row[6],
        "num5": row[7],
        "num6": row[8],
        "bonus": row[9],
        "total_sell_amount": row[10],
        "first_prize_winners": row[11],
        "first_prize_amount": row[12],
        "first_prize_each": row[13]
    }

def to_dict_all(rows):
    return [to_dict(row) for row in rows]

def connect():
    global use_trans, trans_conn
    if use_trans:
        return trans_conn
    else:
        return sqlite3.connect('lotto.db')

def begin():
    global use_trans, trans_conn
    if trans_conn is None:
        trans_conn = connect()
        use_trans = True
    else:
        print("이미 트랜잭션을 시작했습니다.")

def commit():
    global use_trans, trans_conn
    if use_trans and trans_conn is not None:
        trans_conn.commit()
    else:
        print("트랜잭션을 시작하지 않았습니다.")

def rollback():
    global use_trans, trans_conn
    if use_trans and trans_conn is not None:
        trans_conn.rollback()
    else:
        print("트랜잭션을 시작하지 않았습니다.")

def finish():
    global use_trans, trans_conn
    if use_trans and trans_conn is not None:
        trans_conn.close()
        trans_conn = None
        use_trans = False
    else:
        print("트랜잭션을 시작하지 않았습니다.")


if __name__ == "__main__":
    alllotto = get_all()
    for lotto in alllotto:
        print(u.pretty_print(lotto))