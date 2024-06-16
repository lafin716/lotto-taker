import utils as u
from repo.common_repo import CommonRepo

class LottoRepo:
    def __init__(self):
        self.common_repo = CommonRepo()

    def connect(self):
        return self.common_repo.connect()

    def close(self, conn):
        if not self.common_repo.use_trans:
            conn.commit()
            conn.close()

    def get_all(self):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM lotto ORDER BY round ASC")
            rows = cursor.fetchall()
            self.close(conn)
            return self.to_dict_all(rows) if rows else []
        except Exception as e:
            conn.close()
            return []

    def get_latest_round(self):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM lotto ORDER BY round DESC LIMIT 1")
            row = cursor.fetchone()
            self.close(conn)
            return self.to_dict(row) if row else []
        except Exception as e:
            conn.close()
            return False

    def get_round(self, round):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM lotto WHERE round = {round}")
            result = cursor.fetchone()
            self.close(conn)
            return self.to_dict(result)
        except Exception as e:
            conn.close()
            return False
    def save_round(self, row):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO lotto (round, pick_date, num1, num2, num3, num4, num5, num6, bonus, total_sell_amount, first_prize_winners, first_prize_amount, first_prize_each)
                VALUES ({row['round']}, '{row['pick_date']}', {row['num1']}, {row['num2']}, {row['num3']}, {row['num4']}, {row['num5']}, {row['num6']}, {row['bonus']}, {row['total_sell_amount']}, {row['first_prize_winners']}, {row['first_prize_amount']}, {row['first_prize_each']})
            """)

            self.close(conn)
        except Exception as e:
            conn.close()
            return False
    def delete_lotto_win(self, round):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM lotto WHERE round = {round}")

            self.close(conn)
        except Exception as e:
            conn.close()
            return False

    def to_dict(self, row):
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

    def to_dict_all(self, rows):
        return [self.to_dict(row) for row in rows]


if __name__ == "__main__":
    lotto_repo = LottoRepo()
    alllotto = lotto_repo.get_all()
    for lotto in alllotto:
        u.pretty_print(lotto)