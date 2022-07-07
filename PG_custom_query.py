import argparse
from ast import parse
import psycopg2

parser = argparse.ArgumentParser(description='''OP5 custom query check
                                                query must return: 
                                                first row with exit code
                                                optional second row witch comment
                                                optional third row with perfdata''')
parser.add_argument('hostname')
parser.add_argument('database')
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('query')
parser.add_argument('-p', '--port', default='5432', help='Port number (default 5432)')

args = parser.parse_args()

conn = None

def end(exit_code):
    if exit_code > 3 or exit_code < 0:
        exit_code = 3
    exit(exit_code)

try:
    with psycopg2.connect(
        host = args.hostname,
        dbname = args.database,
        user = args.username,
        password = args.password,
        port = args.port
    ) as conn:

        with conn.cursor() as cur:

            query = args.query

            cur.execute(query)

            result = cur.fetchone()

except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()

try:
    exit_code = int(result[0])
except ValueError:
    print('First row must return int between 0-3')  
    end(0)      

### print output
if len(result) == 2:
    print(f'{result[1]}')
    end(exit_code)
elif len(result) == 3:
    print(f'{result[1]} |{result[2]}')
    end(exit_code)
else:
    print('Incorrect number of rows returned from query')

