# MySQL Charset Converter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# MySQL Charset Converter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LoL Server Status. If not, see <http://www.gnu.org/licenses/>.
#
# Source: <https://github.com/LuqueDaniel/MySQLCharsetConverter>

__version__ = "0.1"


from __future__ import print_function

#MySQLdb import
import MySQLdb
# re imports
from re import match
from re import IGNORECASE
from re import sub

#SQL config
db_host = 'localhost'  # Host address and port
db_user = 'root'  # Database username
db_password = 'root'  # User password
db_name = 'wordpress2'  # Database name
#from_charset = 'latin1'  # Current database character set
from_collation = 'latin1_swedish_ci'  # Current database collation
to_charset = 'utf8'  # Future database character set

#Script Config
gen_script_filename = "output.sql"

#SQL Field types
valid_types = ('CHAR', 'TEXT', 'TINYTEXT', 'MEDIUMTEXT', 'LONGTEXT', 'VARCHAR',
               'ENUM')

#Binary types
types = {'CHAR(1)': 'BINARY', 'TEXT': 'BLOB', 'TINYTEXT': 'TINYBLOB',
         'MEDIUMTEXT': 'MEDIUMBLOB', 'LONGTEXT': 'LONGBLOB',}

#Queries
#q_db_charset = "SELECT @@character_set_database;"
q_db_set_charset = "ALTER DATABASE {0} CHARACTER SET {1};"
q_db_get_tables = "SHOW TABLE STATUS FROM {0};"
q_table_set_charset = "ALTER TABLE {0} CHARACTER SET {1};"
q_table_get_clumns = "SHOW FULL COLUMNS FROM {0};"
q_column_to_blob = "alter table {0} change {1} {1} {2};"
q_column_set_charset = "alter table {0} change {1} {1} {2} CHARACTER SET {3};"
q_column_set_charset_enum = "alter table {0} change {1} {1} ENUM({2}) CHARACTER SET {3} not null default {4};"


class DB_Handler():
    """DB Handler. Open and manage database.

    Init parameters:
        host:
            Database host.
        user:
            Database username.
        password:
            User password.
        db:
            Database name
    """
    def __init__(self, host, user, password, db):
        self.con = MySQLdb.connect(host=host, user=user, passwd=password, db=db)

    def execute(self, query):
        """Execute SQL queries."""
        with self.con:
            cursor = self.con.cursor()
            cursor.execute(query)
            return cursor.fetchall()


def file_write(text):
    with open(gen_script_filename, 'a+') as f:
        f.write(text + "\n")


#def get_db_charset():
#    query = db.execute(q_db_charset)
#    return query[0][0]


def get_all_tables():
    """Return all tables from database."""
    return db.execute(q_db_get_tables.format(db_name))


def get_all_columns(table_name):
    """Get all column from table."""
    return db.execute(q_table_get_clumns.format(table_name))


def generate_script():
    """Generate SQL script."""
    print("Writing SQL script...")
    file_write("# CHANGE DATABASE CHARACTER SET")
    file_write(q_db_set_charset.format(db_name, to_charset))

    for table in get_all_tables():
        if to_charset not in table[14]:
            file_write("")
            file_write("#"*80)
            file_write("# {0}".format(table[0]))
            file_write("#"*80)
            file_write("# CHANGE DEFAULT TABLE CHARACTER SET")
            file_write(q_table_set_charset.format(table[0], to_charset))

            for column in get_all_columns(table[0]):
                if match('^(?:{0})'.format("|".join(valid_types)), column[1], IGNORECASE):
                    file_write("# {0}".format(column[0]))
                    if match('^VARCHAR', column[1], IGNORECASE):
                        leng = sub('\D', '', column[1])
                        file_write(q_column_to_blob.format(table[0], column[0], "VARBINARY({})".format(leng)))
                        file_write(q_column_to_blob.format(table[0], column[0], "VARCHAR({})".format(leng), to_charset))
                    elif match('^ENUM', column[1], IGNORECASE):
                        #TODO get values and default value
                        pass
                    else:
                        file_write(q_column_to_blob.format(table[0], column[0], types[column[1].upper()]))
                        file_write(q_column_set_charset.format(table[0], column[0], column[1].upper(), to_charset))
    print("Don't forget to make a backup before running the query :)")

# Initialize
db = DB_Handler(db_host, db_user, db_password, db_name)
generate_script()
