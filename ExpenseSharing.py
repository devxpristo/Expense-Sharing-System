import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ---------------- CLASS ---------------- #

class ExpenseSharing:

    def __init__(self, friends):
        self.friends = friends
        self.balances = {friend: 0 for friend in friends}
        self.missed_payments = []

    def addExpense(self, payer, amount, participants):

        # Track missed payments
        if amount == 0:
            self.missed_payments.append(payer)
            return

        split_amount = amount / len(participants)

        for participant in participants:
            self.balances[participant] -= split_amount

        self.balances[payer] += amount

    def calculateSettlement(self):

        debtors = []
        creditors = []

        # Separate debtors and creditors
        for friend, balance in self.balances.items():
            if balance > 0:
                creditors.append((friend, balance))
            elif balance < 0:
                debtors.append((friend, -balance))

        print("\n----- FINAL SETTLEMENT -----")

        # Settlement logic
        while creditors and debtors:
            debtor, debt_amount = debtors.pop()
            creditor, credit_amount = creditors.pop()

            payment = min(debt_amount, credit_amount)

            print(f"{debtor} should pay {creditor} Rs.{payment:.2f}")

            if debt_amount > payment:
                debtors.append((debtor, debt_amount - payment))

            if credit_amount > payment:
                creditors.append((creditor, credit_amount - payment))

        # Show missed payments
        if self.missed_payments:
            print("\nMissed Payments by:")
            print(", ".join(set(self.missed_payments)))

        # Show final balances
        print("\nFinal Balances:")
        for person, balance in self.balances.items():
            print(f"{person}: Rs.{balance:.2f}")


# ---------------- MAIN PROGRAM ---------------- #

if __name__ == "__main__":

    # Load dataset
    df = pd.read_csv("expense.csv")

    # Data cleaning
    df.columns = df.columns.str.strip().str.lower()
    df['participants'] = df['participants'].str.split(',')
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df['payer'] = df['payer'].str.strip()

    # NumPy Analysis
    print("\n----- NUMPY ANALYSIS -----")
    print("Average Expense:", np.mean(df['amount']))
    print("Maximum Expense:", np.max(df['amount']))
    print("Minimum Expense:", np.min(df['amount']))
    print("Standard Deviation:", np.std(df['amount']))

    # Expense sharing logic
    friends = list(set(df['payer']))
    expense_obj = ExpenseSharing(friends)

    for _, row in df.iterrows():
        expense_obj.addExpense(
            row['payer'],
            row['amount'],
            row['participants']
        )

    expense_obj.calculateSettlement()

    # Data Insights
    print("\n----- DATA INSIGHTS -----")

    total_spent = df.groupby('payer')['amount'].sum()
    print("\nTotal Spending per User:\n", total_spent)

    category_spent = df.groupby('category')['amount'].sum()
    print("\nCategory-wise Spending:\n", category_spent)

    date_spent = df.groupby('date')['amount'].sum()
    print("\nDate-wise Spending:\n", date_spent)

    print("\nTop Spender:", total_spent.idxmax())
    print("Highest spending category:", category_spent.idxmax())

    # Visualization
    total_spent.plot(kind='bar')
    plt.title("Total Spending per User")
    plt.xlabel("Users")
    plt.ylabel("Amount")
    plt.show()

    category_spent.plot(kind='pie', autopct='%1.1f%%')
    plt.title("Category Distribution")
    plt.ylabel("")
    plt.show()

    date_spent.plot(kind='line')
    plt.title("Spending Over Time")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.show()

    print("\nProgram executed successfully!")
