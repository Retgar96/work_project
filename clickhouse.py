import pandas as pd
from clickhouse_driver import Client


RENTA_DATABASE = 'renta'

SEARCH_DATABASE = 'search'


SOURCE_TABLE_SESSIONS = 'UA_32484123_1_sessions'

SOURCE_TABLE_HITS = 'UA_32484123_1'

TABLE_SEARCH_LOGS = 'search_log'

TABLE_AVG_SUGGEST_CLICK = 'avg_suggest_click'


SEARCH_TABLE = 'top_metrics'



CLICKHOUSE_RENTA_CFG = {'host': '192.168.0.145',
                        'port': 9000,
                        'user': 'devml',
                        'password': 'VRBWWXQ7',
                        'database': RENTA_DATABASE}


CLICKHOUSE_ML_CFG = {'host': '192.168.0.191',
                     'port': '9000',
                     'user': 'devml',
                     'password': 'devml123',
                     'database': SEARCH_DATABASE}

SETTINGS = {'max_memory_usage': 128000000000}

def sql_search_queries(date: str) -> str:
    return f"""
        SELECT *
        From {RENTA_DATABASE}.{TABLE_SEARCH_LOGS}
        when date = {date}
        limit = 1000
        """



class Clickhouse:

    def __init__(self, cfg: dict):
        self.client = Client(
            host=cfg['host'],
            port=cfg['port'],
            user=cfg['user'],
            password=cfg['password'],
            database=cfg['database']
        )

    def execute(self, sql: str):
        self.client.execute(sql)

    def select(self, sql: str) -> pd.DataFrame:
        data = self.client.execute(sql, with_column_types=True, settings=SETTINGS)
        columns = [tuple_[0] for tuple_ in data[1]]
        df = pd.DataFrame(data[0], columns=columns)
        return df

    def insert(self, data: pd.DataFrame):
        sql_insert = f'INSERT INTO {SEARCH_DATABASE}.{SEARCH_TABLE} VALUES'
        self.client.execute(sql_insert, data.to_dict(orient='records'))


