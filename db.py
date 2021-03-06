# db.py
# Handle MySQL database connection and queries
# Author: Adam Mitchell
# Email:  adamstuartmitchell@gmail.com
#
# mysql> SHOW columns FROM mfcc_training_data;
# +--------------+------------+------+-----+---------+-------+
# | Field        | Type       | Null | Key | Default | Extra |
# +--------------+------------+------+-----+---------+-------+
# | id           | int(5)     | NO   | PRI | NULL    |       |
# | filename     | mediumtext | YES  |     | NULL    |       |
# | filepath     | mediumtext | YES  |     | NULL    |       |
# | num_value    | int(2)     | YES  |     | NULL    |       |
# | word_value   | tinytext   | YES  |     | NULL    |       |
# | vector       | blob       | YES  |     | NULL    |       |
# | sex          | tinytext   | YES  |     | NULL    |       |
# | vector_shape | tinytext   | YES  |     | NULL    |       |
# +--------------+------------+------+-----+---------+-------+

import traceback
import MySQLdb as mysql


class DbHandler(object):
    def __init__(self, pw, user='root', host='localhost', db='mfcc_training_data'):
        self.cnxn = mysql.connect(host=host, user=user, passwd=pw, db=db)
        self.curs = self.cnxn.cursor()

    def construct_write_query(self, table, id, filename, filepath, num_value, word_value, sex, vector_shape):
        self.query = """INSERT INTO {0}(id,filename,filepath,""" \
                     """num_value,word_value,vector,sex,vector_shape) VALUES""" \
                     """("{1}","{2}","{3}","{4}","{5}","{8}","{6}", "{7}");""".format(table, id,
                                                                              filename, filepath,
                                                                              num_value, word_value,
                                                                              sex, vector_shape,'%s'
                                                                             )

        return self.query

    def execute_query(self, query, *args):
        try:
            if len(args) > 0:
                self.curs.execute(query, (args[0], ))
            else:
                self.curs.execute(query)
            self.cnxn.commit()
        except:
            print traceback.format_exc()
            self.cnxn.rollback()
        finally:
            return self.curs.fetchall()

    def destroy_cnxn(self):
        self.cnxn.close()
