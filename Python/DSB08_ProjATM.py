#!/usr/bin/env python
# coding: utf-8

# ## HW01: Class ATM

# create at least 5 Methods
# - เช็คยอด balance
# - ถอน withdraw
# - ฝาก deposit
# - โอน transfer

# In[2]:


import random


# In[44]:


class ATM: 
    # initialization (create)
    def __init__(self, ac_name, ac_number, ac_balance): 
        self.ac_name = ac_name
        self.ac_number = ac_number
        self.ac_balance = ac_balance

    # string method
    def __str__(self):
        return "JNBC's ATM"

    # balance
    def check_balance(self):
        print(f"Your current balance is {self.ac_balance} THB")

    # deposit 
    def deposit(self, value):
        self.ac_balance += value
        print(f"Successfully deposited {value} THB.")

    # withdraw
    def withdraw(self, value):
        self.ac_balance -= value
        print(f"Successfully withdrew {value} THB.")

    # transfer out
    def transfer_out(self, value):
        self.ac_balance -= value
        print(f"Successfully transfer out {value} THB.")

    # transfer in
    def transfer_in(self, value):
        self.ac_balance += value

    # pay bill
    def pay_bill(self, value):
        self.ac_balance -= value
        print(f"Successfully debit {value} THB.")
        
# Dynamically create a variable using globals()
def create_variable(ac_name, ac_number, ac_balance):
    globals()[ac_name] = ATM(ac_name, ac_number, ac_balance)

my_list = [50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350]


# In[75]:


def create_ac():
    ac_name = input("Enter your account name:")
    ac_number = input("Enter your account number:")
    ac_balance = input("Your initial balance:")
    ac_balance = int(ac_balance)
    
    create_variable(ac_name, ac_number, ac_balance)
    ac = ac_name
    
    print(f"""Crated a new...\n
    Account name: {globals()[ac].ac_name}
    Account number: {globals()[ac].ac_number}
    Current balance: {globals()[ac].ac_balance} THB""")
    print("")


# In[86]:


def transaction():
    ac_nm = input("Insert your JNBC Card and enter your account:")
    
    if ac_nm in globals():
        print(f"Welcome back: {globals()[ac_nm].ac_name} . What would you like to do today?")
        print(f"""Please select your [number] options:\n
            - [1] check balance
            - [2] deposit
            - [3] withdraw
            - [4] transfer
            - [5] bill payment
        """)
        selected = input("Your option:")
    
        if selected == '1':
            globals()[ac_nm].check_balance()
            cf_accept = input("Go to Main menu [1] Yes:")
            print("")
            
        elif selected == '2':
            depo = input("Please insert your cash for deposit:")
            depo = int(depo)
            globals()[ac_nm].deposit(depo)
            globals()[ac_nm].check_balance()
            cf_accept = input("Go to Main menu [1] Yes:")
            print("")
            
        elif selected == '3':
            globals()[ac_nm].check_balance()
            wdra = input("Please enter the amount you wish to withdraw:")
            wdra = int(wdra)
            if wdra > globals()[ac_nm].ac_balance: 
                print("Insufficient funds for withdrawal")
            else: 
                globals()[ac_nm].withdraw(wdra)
                globals()[ac_nm].check_balance()
                cf_accept = input("Go to Main menu [1] Yes:")
                print("")
                
        elif selected == '4':
            ac_trans = input("Enter account that you wish to transfer:")
            
            if ac_trans in globals():
                trans = input("Please enter the amount you wish to transfer:")
                trans = int(trans)
                if trans > globals()[ac_nm].ac_balance: 
                    print("Insufficient funds for transfer")
                    cf_accept = input("Go to Main menu [1] Yes:")
                else:
                    # ถอนจากบัญชีตัวเอง 
                    globals()[ac_nm].transfer_out(trans)
                    globals()[ac_nm].check_balance()
                    print("")
                    # ฝากใส่บัญชีคนอื่น 
                    globals()[ac_trans].transfer_in(trans)
                    cf_accept = input("Go to Main menu [1] Yes:")
            else:
                print("Account not found for transfer")
                cf_accept = input("Go to Main menu [1] Yes:")
            
        elif selected == '5':
            print(f"""Please select the [number] biller:\n
            - [1] water bill
            - [2] electricity bill
            - [3] mobile bill
        """)
            opt_bill = input("Your option:")
            if opt_bill in ['1', '2', '3']:
                random_price = random.choice(my_list)
                print(f"The bill costs {random_price} baht.")
                globals()[ac_nm].check_balance()
                
                if random_price > globals()[ac_nm].ac_balance: 
                    print("Insufficient funds for pay this bill")
                    cf_accept = input("Go to Main menu [1] Yes:")
                else:
                    cf_bill = input("Would you like to pay the bill? [1] Yes [2] No:")
                    
                    if cf_bill == '2':
                        print("Dismiss process. Back to menu.")
                    else:
                        globals()[ac_nm].pay_bill(random_price)
                        globals()[ac_nm].check_balance()
                        cf_accept = input("Go to Main menu [1] Yes:")
                        print("")
            else:
                print("Please select available options.")
                print("Thank you for using our service.")
                    
        else:
            print("Please select available options.")
            print("Thank you for using our service.")
            
    else:
        print("Account not found.")
        print("Thank you for using our service.")


# In[81]:


session_ = True

while session_ == True:
    print("-" * 80)
    print("JNBC's ATM")
    print("""Please select your [number] options:\n
    - [1] crate new account 
    - [2] transactions
    - [3] exit
    """)
    opt_today = input("Would you like to do today?:")
    if opt_today == '1': 
        create_ac()
    elif opt_today == '2':
        transaction()
    elif opt_today == '3':
        print("Thank you for using our service.")
        session_ = False
    else:
        print("Please select available options.")

