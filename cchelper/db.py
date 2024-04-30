from PySide6.QtSql import *
import os
from .logger import logger
import re
from typing import List, Type, Dict, Any, Tuple
import cchelper.paths as paths


def record_to_dict(record: QSqlRecord):
    return {record.fieldName(i): record.value(i) for i in range(record.count())}


class Database:
    def __init__(self) -> None:
        self.con = QSqlDatabase.addDatabase("QSQLITE")
        self.fn = paths.data("db", "cchelper.db")
        self.con.setDatabaseName(self.fn)
        if not self.con.open():
            logger.exception(f"Database Error: {self.con.lasTerror().text()}")
        self.ptr = QSqlQuery()
        sqls = self.parse_sqls(paths.data("db", "create.sql"))
        self.execute(sqls)

    def parse_sqls(self, fn: str) -> List[str]:
        buf = []
        sqls = []
        with open(fn, 'r') as r:
            for line in r:
                if line.strip() == '':
                    continue
                if line.startswith('--'):
                    if buf:
                        sqls.append(''.join(buf))
                        buf.clear()
                else:
                    buf.append(line)
        if buf:
            sqls.append(''.join(buf))
            buf.clear()
        return sqls

    def reset(self):
        self.con.close()
        os.remove(self.fn)
        self.con.setDatabaseName(self.fn)
        if not self.con.open():
            logger.exception(f"Database Error: {self.con.lastError().text()}")
        self.ptr = QSqlQuery()
        sqls = self.parse_sqls(paths.data("db", "create.sql"))
        self.execute(sqls)

    def execute(self, sqls: List[Tuple | str]) -> bool:
        if type(sqls) is not list:
            sqls = [sqls]
        self.con.transaction()
        for sql in sqls:
            if type(sql) is str:
                logger.debug(sql)
                if not self.ptr.exec(sql):
                    logger.error(self.ptr.lastError())
                    self.con.rollback()
                    return False
            else:
                sql, vals = sql
                self.ptr.prepare(sql)
                if type(vals) is tuple:
                    for idx, var in enumerate(vals):
                        self.ptr.bindValue(idx, var)
                else:  # dict
                    for k, v in vals.items():
                        self.ptr.bindValue(k, v)
                ret = self.ptr.exec()
                logger.debug(self.ptr.executedQuery())  # TODO
                logger.debug(self.ptr.boundValues())
                if not ret:
                    logger.error(self.ptr.lastError())
                    self.con.rollback()
                    return False
        self.con.commit()
        return True

    def query(self, sql: str | Tuple) -> List[Dict[str, Any]]:
        dats = []
        if type(sql) is str:
            logger.debug(sql)
            if not self.ptr.exec(sql):
                logger.error(self.ptr.lastError())
                return dats
        else:
            sql, vals = sql
            self.ptr.prepare(sql)
            if type(vals) is tuple:
                for idx, var in enumerate(vals):
                    self.ptr.bindValue(idx, var)
            else:  # dict
                for k, v in vals.items():
                    self.ptr.bindValue(k, v)
            ret = self.ptr.exec()
            logger.debug(self.ptr.executedQuery())  # TODO
            if not ret:
                logger.error(self.ptr.lastError())
                return dats
        while self.ptr.next():
            dats.append(record_to_dict(self.ptr.record()))
        return dats

    def terminate(self):
        pass

    def cloud_sync(self):
        pass


db = Database()
