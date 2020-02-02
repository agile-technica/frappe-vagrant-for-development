"""
Clean index deletes "duplicated" indexes as required
Sometimes this can happen during development of frappe apps...
"""
import MySQLdb
import re

db_name = "_5b7dbb7d74e0a6e6"

db = MySQLdb.connect(host="localhost", user="root",
                     passwd="root", db=db_name)

cursor = db.cursor()
cursor.execute("""SHOW tables""")

for table in cursor:
    table_name = table[0]

    index_query = "SHOW INDEX from `" + table_name + "` FROM " + db_name
    cursor_index = db.cursor()
    cursor_index.execute(index_query)

    all_indexes = cursor_index.fetchall()

    # if there are more than 30 indexes...chances are something is wrong
    if len(all_indexes) > 12:
        for index in cursor_index:
            if re.match(".*_*[2-9]+", index[2]):
                # if duplicated match found, drop the index
                index_drop_sql = "ALTER TABLE `" + table_name + "` DROP INDEX `" + index[2] + "`;"

                print(index_drop_sql)

                cursor_drop = db.cursor()
                cursor_drop.execute(index_drop_sql)
