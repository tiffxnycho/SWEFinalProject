class BankAccount:
    bank_title = "Python Bank"

    def __init__(self, customer_name, current_balance, minimum_balance):
        self.customer_name = customer_name
        self.current_balance = current_balance
        self.minimum_balance = minimum_balance

    def deposit(self, amount):
        if amount > 0:
            self.current_balance += amount
            print(f"Deposited ${amount}. New Balance: ${self.current_balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount < 0:
            print("Withdraw amount must be positive.")
        elif self.current_balance - amount < self.minimum_balance:
            print("Withdraw amount exceeds minimum balance.")
        else:
            self.current_balance -= amount
            print(f"Withdrew ${amount}. New Balance: ${self.current_balance}")

    def print_customer_information(self):
        print(f"Bank: {BankAccount.bank_title}")
        print(f"Customer Name: {self.customer_name}")
        print(f"Current Balance: ${self.current_balance}")
        print(f"Minimum Balance: ${self.minimum_balance}")
        print("-" * 30)

account1 = BankAccount("Trace", 20000, 10000)
account2 = BankAccount("Savanna", 10000, 5000)

account1.print_customer_information()
account1.deposit(100)
account1.withdraw(11000)
account1.withdraw(10000)

account2.print_customer_information()
account2.deposit(10000)
account2.withdraw(10000)


