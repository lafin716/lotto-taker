import utils as u
from repo.common_repo import CommonRepo

class MyLottoRepo:
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
            cursor.execute("SELECT * FROM my_lotto ORDER BY round ASC")
            rows = cursor.fetchall()
            self.close(conn)
            return self.to_dict_all(rows) if rows else []
        except Exception as e:
            conn.close()
            return []

    def get_round_all(self, round):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM my_lotto WHERE round = {round}")
            result = cursor.fetchall()
            self.close(conn)
            return self.to_dict_all(result)
        except Exception as e:
            conn.close()
            return False

    def save_round(self, row):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO my_lotto (round, pick_date, pick_type, num1, num2, num3, num4, num5, num6)
                VALUES ({row['round']}, '{row['pick_date']}', '{row['pick_type']}', {row['num1']}, {row['num2']}, {row['num3']}, {row['num4']}, {row['num5']}, {row['num6']})
            """)

            self.close(conn)
        except Exception as e:
            conn.close()
            return False

    def delete_round(self, round):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM my_lotto WHERE round = {round}")
            self.close(conn)
            return True
        except Exception as e:
            conn.close()
            return False

    def to_dict_all(self, rows):
        return [self.to_dict(row) for row in rows]

    def to_dict(self, row):
        if not row:
            return {}
        return {
            'id': row[0],
            'pick_date': row[1],
            'pick_type': row[2],
            'round': row[3],
            'num1': row[4],
            'num2': row[5],
            'num3': row[6],
            'num4': row[7],
            'num5': row[8],
            'num6': row[9],
        }

