class Category:
    def __init__(self, category_name):
        self.category = category_name
        self.ledger = []
        self.total = 0
    def check_funds(self, amount):
        if self.total < amount:
            return False
        else:
            return True
    def deposit(self, amount, description=None):
        if description is None:
            description = ''
        self.total += amount
        self.ledger.append({'amount': amount, 'description': description})
    def withdraw(self, amount, description=None):
        if description is None:
            description = ''
        if self.check_funds(amount):
            self.total -= amount
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        else:
            return False
    def get_balance(self):
        return self.total
    def transfer(self, amount, another_category):
        if self.withdraw(amount, 'Transfer to ' + another_category.category):
            another_category.deposit(amount, 'Transfer from ' + self.category)
            return True
        else:
            return False
    def __str__(self):
        result = '*' * ((30 - len(self.category)) // 2) + self.category
        result = result + '*' * (30 - len(result)) + '\n'
        for i in self.ledger:
            result += i['description'][:23].ljust(23) + str('{:.2f}'.format(i['amount']).rjust(7)) + '\n'
        result += 'Total: ' + str(self.total)
        return result
def round_down(n):
    if n < 10:
        return 0
    return round(n / 10.0) * 10
def create_spend_chart(categories):
    withdrawals = []
    category_length = 0
    result = 0
    for i in categories:
        withdraw_amount = 0
        for x in i.ledger:
            if x['amount'] < 0:
                withdraw_amount += -x['amount']
                result += (-x['amount'])
        if len(i.category) > category_length:
            category_length = len(i.category)
        withdrawals.append([i.category, withdraw_amount])
    for i in withdrawals:
        i.append(round_down((i[1] / result) * 100))
    result = ''
    result += 'Percentage spent by category\n'
    percentage = 100
    while percentage >= 0:
        result += str(percentage).rjust(3) + '|' + ' '
        for i in range(len(withdrawals)):
            if withdrawals[i][2] >= percentage:
                result += 'o' + '  '
            else:
                result += '   '
        percentage -= 10
        result += '\n'
    result += '    ' + ('-' * 10) + '\n'
    loop = 0
    for i in range(category_length):
        result += '     '
        for x in range(len(withdrawals)):
            if len(withdrawals[x][0]) - 1 < loop:
                result += '   '
            else:
                result += withdrawals[x][0][loop] + '  '
        loop += 1
        if i != category_length - 1:
            result += '\n'
    return result