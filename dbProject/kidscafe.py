import pymysql
import os
import time
import datetime

#Database
con = pymysql.connect(host="localhost", user="root",password="q1w2e3r4",db='kidscafe',charset='utf8')
cur= con.cursor()


# Login
def login():
    print("1. 키즈 로그인")
    print("2. 매니저 로그인")
    print("3. 종료")
    IsManager = input("-> ");
    os.system('clear')
    if IsManager == 3:
        exit()
    while True:
        id = input("ID: ")
        password = input("Password: ")
        if IsManager == '1':
            sql="""
            SELECT password
            FROM kids
            WHERE (kid_id = %s)
            """
        else:
            sql="""
            SELECT password
            FROM manager
            WHERE (manager_id = %s)
            """
        cur.execute(sql,id)
        con.commit()
        row = cur.fetchone()
        if row[0] == password:
            break
        print("비밀번호가 틀렸습니다.")
    print("로그인 성공!")
    if IsManager == '1':
        kidsmenu(id)
    else:
        managermenu(id)

#Kidsmenu
def kidsmenu(id):

    time.sleep(0.5)
    os.system('clear')

    print("1. 입장하기")
    print("2. 퇴장하기")
    command = input("->")
    if command== '1':
        enter_kid(id)
    elif command == '2':
        exit_kid(id)
        exit()

    while True:
        time.sleep(1)
        os.system('clear')

        sql = '''
        SELECT kids.name, kids.phone_number
        FROM kids
        WHERE kid_id = %s
        '''
        cur.execute(sql,id)
        con.commit()
        row = cur.fetchone()
        print(row[0]+ "의 Kids Menu")
        print("핸드폰번호 : "+ str(row[1])+"\n")

        print("1. 입장 시각 보기")
        print("2. 과거 이용 내역 보기")
        print("3. 교구 검색하기")
        print("4. 교구 사용하기")
        print("5. 퇴장하기")
        print("6. 퇴장하지 않고 종료하기")
        command = input("-> ")

        if command == "1":
            sql ='''
            SELECT ent_time, TIMESTAMPDIFF(MINUTE, ent_time, NOW())
            FROM ent_history
            WHERE is_here = 1 and kid_id = %s
            '''
            cur.execute(sql,id)
            con.commit()
            row = cur.fetchone()
            print("입장한 시각은" + str(row[0]) + "입니다")
            print("입장한 후, " + str(row[1]) + "분이 지났습니다")
            time.sleep(1)
        elif command == "2":
            sql = '''
            SELECT ent_time, end_time, TIMESTAMPDIFF(MINUTE, ent_time, end_time)
            FROM ent_history
            WHERE kid_id = %s and is_here =0
            ORDER BY end_time DESC
            '''
            cur.execute(sql,id)
            con.commit()
            rows = cur.fetchall()
            print("\t입장시각\t퇴장시각")
            for row in rows:
                print(str(row[0])+" "+str(row[1]))
            time.sleep(1)
        elif command == "3":
            search_art()
        elif command == "4":
            #교구 사용하기
            name = input('사용할 교구 이름-> ')
            sql='''
            INSERT INTO art_history
            VALUES (NOW(),%s, %s)
            '''
            cur.execute(sql,(id, name))
            con.commit()
            print("사용 등록 되었습니다")
            time.sleep(1)
        elif command == "5":
            exit_kid(id)
        else:
            exit()


def enter_kid(id):
    #enter 기록이 있다면
    sql='''
    SELECT ent_time
    FROM ent_history
    WHERE 1 IN (SELECT is_here
               FROM ent_history
                WHERE kid_id = %s)
    '''
    cur.execute(sql, id)
    con.commit()
    row = cur.fetchone()
    if row == None:
        sql='''
        INSERT INTO ent_history
        VALUES (%s, NOW(), NULL, 1)
        '''
        cur.execute(sql, id)
        con.commit()
    print("입장하셨습니다!")



def exit_kid(id):
    sql = '''
    UPDATE ent_history
    SET end_time = NOW(), is_here = 0
    WHERE kid_id = %s and is_here = 1
    '''
    cur.execute(sql, id)
    con.commit()
    os.system('clear')
    sql = '''
    SELECT TIMESTAMPDIFF(MINUTE,ent_time, end_time)
    FROM ent_history
    WHERE kid_id = %s
    ORDER BY end_time DESC
    '''
    cur.execute(sql,id)
    row = cur.fetchone()
    print("이용시간은 " + str(row[0])+ "분 입니다")
    time.sleep(1)
    exit()

def search_art():
    print("1. 이름으로 검색하기")
    print("2. 위치로 검색하기")
    command = input("-> ")

    if command == "1":
        name = input('이름을 입력해주세요 -> ')
        sql = '''
        SELECT a.name, location, cost, m.name
        FROM art_and_craft as a, manager as m
        WHERE a.name = m.manage_artname
            AND (a.name = %s)
        '''
        cur.execute(sql,name)
        rows = cur.fetchall()
        print("교구이름, 위치, 비용, 담당선생님이름")
        for row in rows:
            print(str(row[0])+" "+str(row[1])+" "+str(row[2])+" "+str(row[3]))
    elif command == "2":
        location = input('위치를 입력해주세요 -> ')
        sql = '''
        SELECT a.name, location, cost, m.name
        FROM art_and_craft as a, manager as m
        WHERE a.name = m.manage_artname
            AND (a.location = %s)
        '''
        cur.execute(sql,location)
        rows = cur.fetchall()
        print("교구이름, 위치, 비용, 담당선생님이름")
        for row in rows:
            print(str(row[0])+" "+str(row[1])+" "+str(row[2])+" "+str(row[3]))
    time.sleep(1)

#managermenu
def managermenu(id):
    while True:
        time.sleep(0.5)
        os.system('clear')
        sql = '''
        SELECT name
        FROM manager
        WHERE manager_id = %s
        '''
        cur.execute(sql,id)
        con.commit()
        row = cur.fetchone()
        print(row[0]+ "의 Manager Menu\n")
        print("1. 현재 입장 중인 고객 모두 보기")
        print("2. 이름으로 고객 기록 찾기")
        print("3. 일자별 다녀온 고객 기록 찾기")
        print("4. 교구 검색하기")
        print("0. 종료하기")
        command = input("-> ")

        if command == "1":
            sql = '''
            SELECT kids.name, kids.phone_number
            FROM ent_history as h
            LEFT JOIN kids ON h.kid_id = kids.kid_id
            WHERE is_here =1
            '''
            cur.execute(sql)
            con.commit()
            rows = cur.fetchall()
            print("고객이름 고객번호")
            for row in rows:
                print(str(row[0])+" "+str(row[1]))

        elif command == "2":
            name = input("검색할 이름을 입력해주세요-> ")
            sql='''
            SELECT kid_id, name, phone_number
            FROM kids
            WHERE name = %s
            '''
            cur.execute(sql,name)
            con.commit()
            rows = cur.fetchall()
            print("아이디 이름  번호")
            for row in rows:
                print(str(row[0])+" "+str(row[1])+" "+str(row[2]))
        elif command == "3":
            os.system('clear')
            print("1. 한 시간 전 고객 찾기")
            print("2. 하루 전 고객 찾기")
            print("3. 일주일 전까지의 고객 찾기")
            c_command = input("-> ")
            if c_command == "1":
                sql = '''
                SELECT h.ent_time, kids.kid_id, kids.name, kids.phone_number
                FROM ent_history as h
                LEFT JOIN kids ON h.kid_id = kids.kid_id
                WHERE h.ent_time BETWEEN (SELECT DATE_SUB(NOW(), INTERVAL 1 HOUR)) AND NOW()
                '''
                cur.execute(sql)
                con.commit()
                rows = cur.fetchall()
                print("시간\t아이디 이름  번호")
                for row in rows:
                    print(str(row[0])+" "+str(row[1])+" "+str(row[2])+" "+str(row[3]))
            elif c_command == "2":
                sql = '''
                SELECT h.ent_time, kids.kid_id, kids.name, kids.phone_number
                FROM ent_history as h
                LEFT JOIN kids ON h.kid_id = kids.kid_id
                WHERE h.ent_time BETWEEN (SELECT DATE_SUB(NOW(), INTERVAL 1 DAY)) AND NOW()
                '''
                cur.execute(sql)
                con.commit()
                rows = cur.fetchall()
                print("시간\t\t 아이디 이름\t 번호")
                for row in rows:
                    print(str(row[0])+" "+str(row[1])+" "+str(row[2])+" "+str(row[3]))

            else:
                sql = '''
                SELECT h.ent_time, kids.kid_id, kids.name, kids.phone_number
                FROM ent_history as h
                LEFT JOIN kids ON h.kid_id = kids.kid_id
                WHERE h.ent_time BETWEEN (SELECT DATE_SUB(NOW(), INTERVAL 1 MONTH)) AND NOW()
                '''
                cur.execute(sql)
                con.commit()
                rows = cur.fetchall()
                print("시간\t아이디 이름  번호")
                for row in rows:
                    print(str(row[0])+" "+str(row[1])+" "+str(row[2])+" "+str(row[3]))
        elif command == "4":
            search_art()

        else:
            exit()
        time.sleep(2)



if __name__ == "__main__":
    login()
    con.close()
