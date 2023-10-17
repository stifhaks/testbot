import sqlite3
from aiocryptopay import AioCryptoPay, Networks
from config import cryptobot_test_net, cryptobot_main_net
from database.db_keys import user_table, k_user_id, k_locate, k_login, k_key, k_addres

cp = AioCryptoPay(token=cryptobot_main_net, network=Networks.MAIN_NET)



sql_create_users_table = f""" CREATE TABLE IF NOT EXISTS {user_table} (
                                        id integer PRIMARY KEY,
                                        {k_user_id} text NOT NULL,
                                        {k_login} text,
                                        {k_locate} text,
                                        {k_key} text,
                                        {k_addres} text,
                                        join_date datetime
                                    ); """

sql_create_record_table = f""" CREATE TABLE IF NOT EXISTS records (
                                        id integer PRIMARY KEY,
                                        {k_user_id} text NOT NULL,
                                        amount text,
                                        operation real
                                    ); """

sql_create_sequence_table = """ CREATE TABLE IF NOT EXISTS sqlite_sequence (
                                        name text NOT NULL,
                                        seq text
                                    ); """
sql_create_trans_table = f""" CREATE TABLE IF NOT EXISTS transactions (
                                        id integer PRIMARY KEY,
                                        {k_user_id} text NOT NULL,
                                        currency text NOT NULL,
                                        amount real
                                    ); """

class db:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql_create_trans_table)
            # self.cursor.execute(sql_create_sequence_table)
            self.cursor.execute(sql_create_record_table)
            self.cursor.execute(sql_create_users_table)
        except Exception as e:
            print(e)

    def row_exist(self, table, id):
        #Проверяем, есть ли юзер в базе
        result = self.cursor.execute(f"SELECT `id` FROM `{table}` WHERE `{k_user_id}` = ?", (id,))
        return bool(len(result.fetchall()))

    def user_exists(self, user_id):
        #Проверяем, есть ли юзер в базе
        result = self.cursor.execute(f"SELECT `id` FROM `users` WHERE `{k_user_id}` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def cell_exist(self,table,f_id,coll):
        result = self.cursor.execute(f"SELECT `{coll}` FROM `{table}` WHERE `{k_user_id}` = ?", (f_id,))
        f_res = result.fetchone()[0]
        return bool(f_res)

    def get_cell(self,table,coll,id):
        SQL = f"SELECT `{coll}` FROM `{table}` WHERE `{k_user_id}` = {id}"
        result = self.cursor.execute(SQL)
        return result.fetchone()[0]
    def get_row(self,table, id):
        #Достаем id юзера в базе по его user_id
        result = self.cursor.execute(f"SELECT `id` FROM `{table}` WHERE `{k_user_id}` = `{id}`",)
        return result.fetchone()[0]

    def get_user_id(self, user_id):
        #Достаем id юзера в базе по его user_id
        result = self.cursor.execute(f"SELECT `id` FROM `users` WHERE `{k_user_id}` = ?", (user_id,))
        return result.fetchone()[0]

    def get_used_locate(self, user_id):
        result = self.cursor.execute(f"SELECT `{k_locate}` FROM `{user_table}` WHERE `{k_user_id}` = ?", (user_id,))
        return result.fetchone()[0]

    def add_row(self,table,data):
        f_sql = f'INSERT INTO "{table}" ('
        f_values = ''
        for q_key in data.keys():
            f_sql += f'"{q_key}", '
            f_values += f'"{data[q_key]}",'
        f_sql = f_sql.removesuffix(', ')
        f_values = f_values.removesuffix(',')
        f_sql += f") VALUES ({f_values})"
        self.cursor.execute(f_sql)
        return self.conn.commit()

    def add_cell(self,table,f_id,coll,data):
        # data = '0x' + data
        data = data.removeprefix("0x")
        self.cursor.execute(f"UPDATE `{table}` SET `{coll}` = '%s' WHERE `{k_user_id}` = {f_id}" % data)
        return self.conn.commit()

    def add_user(self, user_id,f_key):
        #Добавляем юзера в базу
        self.cursor.execute(f"INSERT INTO `users` (`{k_user_id}`, `{k_locate}`) VALUES (?,?)", (user_id,f_key))
        return self.conn.commit()

    # def add_user(self, user_id):
    #     #Добавляем юзера в базу
    #     self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
    #     return self.conn.commit()

    def add_records(self, user_id, operation, amount):
        #Создаем записи о депозитах и выводах
        self.cursor.execute(f"INSERT INTO 'records'('{k_user_id}', 'operation', 'amount') VALUES (?, ?, ?)", (self.get_user_id(user_id),
                                                                                                          operation,
                                                                                                          amount))
        return self.conn.commit()

    def get_balance(self, user_id):
        #Счетаем баланс пользователя
        c = self.cursor.execute(f'SELECT COALESCE(SUM(CASE WHEN operation = "+" THEN amount ELSE -amount END), 0) AS balance FROM records WHERE {k_user_id} = ?', (self.get_user_id(user_id),))
        return c.fetchall()

    # def add_record(self, user_id, currency, amount):
    #     #Создаем запись о депозите
    #     self.cursor.execute("INSERT INTO `transactions` (`users_id`,'currency', 'amount') VALUES (?, ?, ?)", (self.get_user_id(user_id),
    #                                                                                                         currency,
    #                                                                                                         amount))
    #     return self.conn.commit()
    #
    # async def get_balance(self, user_id):
    #     #Считаем баланс пользователя
    #     c = self.cursor.execute("SELECT currency, SUM(amount) FROM transactions WHERE users_id=? GROUP BY currency", (self.get_user_id(user_id),))
    #     run_equivalent = 0.0
    #     rub_equivalent = 0.0
    #     rates = await cp.get_exchange_rates()
    #     results = c.fetchall()
    #     arr ='\n'
    #     for row in results:
    #         currency, balance = row
    #         match currency:
    #             case ("USDT"):
    #                 run_equivalent += balance * rates[0].rate
    #                 rub_equivalent = balance * rates[0].rate
    #             case ("TON"):
    #                 run_equivalent += balance * rates[18].rate
    #                 rub_equivalent = balance * rates[18].rate
    #             case ("ETH"):
    #                 run_equivalent += balance * rates[54].rate
    #                 rub_equivalent = balance * rates[54].rate
    #             case ("BNB"):
    #                 run_equivalent += balance * rates[72].rate
    #                 rub_equivalent = balance * rates[72].rate
    #             case ("BUSD"):
    #                 run_equivalent += balance * rates[90].rate
    #                 rub_equivalent = balance * rates[90].rate
    #             case ("USDC"):
    #                 run_equivalent += balance * rates[108].rate
    #                 rub_equivalent = balance * rates[108].rate
    #
    #         arr += f"{currency}: {balance}    <=>   {rub_equivalent} руб\n"
    #     arr += f"\n Ваш баланс : {run_equivalent} руб"
    #     return arr
    #
    # async def rub_balance(self, user_id):
    #     #Считаем баланс пользователя в рублях
    #     c = self.cursor.execute("SELECT currency, SUM(amount) FROM transactions WHERE users_id=? GROUP BY currency",
    #                             (self.get_user_id(user_id),))
    #     balance = 0.0
    #     rates = await cp.get_exchange_rates()
    #     results = c.fetchall()
    #     for row in results:
    #         currency, b = row
    #         match currency:
    #             case ("USDT"):
    #                 balance += b * rates[0].rate
    #             case ("TON"):
    #                 balance += b * rates[18].rate
    #             case ("ETH"):
    #                 balance += b * rates[54].rate
    #             case ("BNB"):
    #                 balance += b * rates[72].rate
    #             case ("BUSD"):
    #                 balance += b * rates[90].rate
    #             case ("USDC"):
    #                 balance += b * rates[108].rate
    #     return balance





