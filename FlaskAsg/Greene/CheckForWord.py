from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor
import time

import sqlite3 as sql

def FindWord(x):
    numOfWords = 0

    # connect to Message db
    with sql.connect("Messages.db") as con:
        con.row_factory = sql.Row

        cur = con.cursor()

        # run SQL command
        sql_select_query = """SELECT COUNT(*) AS NumMsgs FROM Messages WHERE Message LIKE ? """
        cur.execute(sql_select_query, ("%" + x + "%",))
        row = cur.fetchone()
        CurNumber = int(row[0])

        # if we the word we're looking for
        if (numOfWords != CurNumber):
            numOfWords = CurNumber
            print("Number of messages that contain the word " + x + " is now " + str(CurNumber))

    con.close()
    return numOfWords


def main():

    # get current values
    Xproc = FindWord("Coffee")
    Yproc = FindWord("Chocolate")

    while (True):
        with ThreadPoolExecutor(max_workers=2) as executor:

            # executing the two tasks using ThreadPool
            TaskXproc = executor.submit(FindWord, "Coffee")
            TaskYproc = executor.submit(FindWord, "Chocolate")

            # if they're not equal (implying the previous process didn't update with the new one), we set the new result
            if (TaskXproc.result() != Xproc):
                Xproc = TaskXproc.result()
                print("Number of messages that contain the word Coffee " + str(Xproc))

            # the same condition is checked but for the word "Chocolate"
            if (TaskYproc.result() != Yproc):
                Yproc = TaskYproc.result()
                print("Number of messages that contain the word Chocolate " + str(Yproc))

            time.sleep(4)

if __name__ == '__main__':
    main()