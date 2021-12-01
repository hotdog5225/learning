class Company:
    def __init__(self, employees):
        self.employee_list = employees

    def __getitem__(self, item):
        return self.employee_list[item]

if __name__ == '__main__':
    c = Company(["foo", "bar"])
    for employee in c:
        print(employee)
