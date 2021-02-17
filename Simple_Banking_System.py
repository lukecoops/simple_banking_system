from random import randint
import sqlite3
conn = sqlite3.connect("card.s3db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS card(id integer primary key, number TEXT, pin TEXT, balance INTEGER DEFAULT(0))")
conn.commit()
def luhn_check(card_number):
    card_number = [int(x) for x in card_number]
    for i in range(0, 14, 2):
        card_number[i] *= 2
    for i in range(15):
        if card_number[i] > 9:
            card_number[i] -= 9
    return True if sum(card_number) % 10 == 0 else False
auth_card_number = []
auth_pin = []
session = 1
while session == 1:
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    selection_1 = int(input())
    if selection_1 == 1:
        print("Your card has been created")
        card_number = [4, 0, 0, 0, 0, 0]
        for _ in range(9):
            card_number.append(randint(0,9))
        luhn = card_number.copy()
        for i in range(15):
            if i % 2 == 0:
                luhn[i] *= 2
            if luhn[i] > 9:
                luhn[i] -= 9
        checksum = (10 * ((sum(luhn) + 10) // 10) - sum(luhn))
        card_number.append(checksum)
        if card_number[15] == 10:
            card_number[15] = 0
        pin = str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9))
        card_number_string = [str(x) for x in card_number]
        card_number_int = int("".join(card_number_string))
        cur.execute("INSERT INTO card(number, pin) VALUES(?,?)",(str(card_number_int), pin))
        conn.commit()
        auth_card_number.append(card_number_int)
        auth_pin.append(pin)
        print("Your card number:")
        print(card_number_int)
        print("Your card PIN:")
        print(pin)
    elif selection_1 == 2:
        print("Enter your card number:")
        card_number_login = int(input())
        print("Enter your PIN:")
        pin_login = input()
        cur.execute("SELECT number, pin FROM card WHERE number = ? AND pin = ?;", (card_number_login, pin_login))
        auth = cur.fetchall()
        session = 2
        while session == 2:
            try:
                if len(auth):
                    print("You have successfully logged in!")
                    print("1. Balance")
                    print("2. Add income")
                    print("3. Do transfer")
                    print("4. Close account")
                    print("5. Log out")
                    print("0. Exit")
                    selection_2 = int(input())
                    if selection_2 == 1:
                        cur.execute("SELECT balance FROM card WHERE number = ?", (card_number_login,))
                        balance = int(cur.fetchone()[0])
                        print("Balance:", balance)
                    elif selection_2 == 2:
                        print("Enter income:")
                        income = input()
                        cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?", (income, card_number_login))
                        conn.commit()
                        print("Income was added!")
                    elif selection_2 == 3:
                        print("Transfer\nEnter card number:")
                        transfer_number = input()
                        cur.execute("SELECT number FROM card WHERE number = ?",(transfer_number,))
                        data = cur.fetchone()
                        cur.execute("SELECT balance FROM card WHERE number = ?", (card_number_login,))
                        balance = int(cur.fetchone()[0])
                        if data:
                            print("Enter how much money you want to transfer:")
                            transfer_amount = int(input())
                            if transfer_amount > balance:
                                print("Not enough money!")
                            else:
                                cur.execute("UPDATE card SET balance = balance - ? WHERE number = ?", (transfer_amount, card_number_login))
                                cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?", (transfer_amount, transfer_number))
                                conn.commit()
                                print("Success")
                        else:
                            if luhn_check(transfer_number) == False:
                                print("Probably you made a mistake in the card number. Please try again!")
                            else:
                                print("Such a card does not exist.")
                    elif selection_2 == 4:
                        cur.execute("DELETE FROM card WHERE number = ?", (card_number_login,))
                        conn.commit()
                        print("The account has been closed!")
                    elif selection_2 == 5:
                        session = 1
                    elif selection_2 == 0:
                        print("Bye!")
                        session = 0
                else:
                    print("Wrong card number or PIN!")
                    session = 1
            except:
                print("Wrong card number or PIN!")
    elif selection_1 == 0:
        print("Bye!")
        session = 0
