import psycopg2
from tools.others import get_connect_db

dbname, user, password, host, port = get_connect_db()


class UserManager:
    def __init__(self, dbname: str, user: str, password: str, host: str, port: int) -> None:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        conn.autocommit = True
        self.__cur = conn.cursor()

        self.__cur.execute('''
            CREATE TABLE IF NOT EXISTS clients(
                client_id SERIAL PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                phone VARCHAR(15),
                city VARCHAR(50),
                birthday DATE,
                avito_profile TEXT,
                shoe_model VARCHAR(50),
                shoe_size NUMERIC,
                purchase_amount NUMERIC
            );
        ''')


    def add_client(self, first_name, last_name, phone, city, birthday, avito_profile, shoe_model, shoe_size, purchase_amount) -> None:
        last_client_id = self.get_last_client_id()
        if last_client_id is not None:
            new_client_id = last_client_id + 1
        else:
            new_client_id = 1
        self.__cur.execute('''
            INSERT INTO clients (client_id, first_name, last_name, phone, city, birthday, avito_profile, shoe_model, shoe_size, purchase_amount)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (new_client_id, first_name, last_name, phone, city, birthday, avito_profile, shoe_model, shoe_size, purchase_amount))


    def get_list_clients(self) -> str:
        self.__cur.execute("SELECT * FROM clients ORDER BY client_id")
        clients = self.__cur.fetchall()
        result = []
        for client in clients:
            client_data = {
                "id": client[0],
                "Имя": client[1],
                "Фамилия": client[2],
                "Номер": client[3],
                "Город": client[4],
                "ДР": client[5],
                "Профиль": client[6],
                "Модель": client[7],
                "Размер": client[8],
                "Сумма покупки": client[9]
            }
            result.append(client_data)
        return result
    

    def get_last_client_id(self) -> int:
        self.__cur.execute("SELECT MAX(client_id) FROM clients")
        max_id = self.__cur.fetchone()[0]
        return max_id if max_id is not None else 0


    def get_count_clients(self) -> bool:
        self.__cur.execute("SELECT COUNT(*) FROM clients")
        return self.__cur.fetchone()[0]


    def delete_client(self, client_id: int) -> int:
        self.__cur.execute(f'''
        DELETE FROM clients
        WHERE client_id = '{client_id}'
        ''')
        return self.__cur.rowcount
    
    
    def update_client_data(self, client_id: int, column: str, new_value) -> int:
        self.__cur.execute(f'''
            UPDATE clients
            SET {column} = %s
            WHERE client_id = %s
        ''', (new_value, client_id))
    

    def find_user(self, client_id: int) -> bool:
        self.__cur.execute("SELECT EXISTS(SELECT 1 FROM clients WHERE client_id = %s)", (client_id,))
        return self.__cur.fetchone()[0]



dbmanager = UserManager(dbname=dbname[0], user=user[0], password=password[0], host=host[0], port=int(port[0]))