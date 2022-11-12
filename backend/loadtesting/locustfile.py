import time
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def login(self):
        self.client.get(url = "/customer?service=login&username=customer1")
    @task
    def accountType(self):
        self.client.get(url = "/customer?service=account_type&account_type=business")
    @task
    def customerLoansByCustomer(self):
        self.client.get(url = "/customer-loans?service=byCustomer&customerID=1")
    @task
    def customerLoansByLoans(self):
        self.client.get(url = "/customer-loans?service=byLoan&loanID=1")
    @task
    def paymentByCustomer(self):
        self.client.get(url = "/payment?service=byCustomer&customerID=1")
    @task
    def paymentAddPayment(self):
        self.client.get(url = "/payment?service=addPayment&customerID=1&payment_id=1&loan_id=1&amount=100&date=2010-10-10&business_id=3")
    @task
    def walletByCustomer(self):
        self.client.get(url = "/wallet?service=byCustomer&customerID=1")
    @task
    def walletUpdateFunds(self):
        self.client.get(url = "/wallet?service=updateFunds&amount=-100&customerID=1")
    # @task
    # def loansByBusiness(self):
    #     self.client.get(url = "/loans?service=byBusiness&businessID=3")
    # @task
    # def loansByLoans(self):
    #     self.client.get(url = "/loans?service=byLoan&loanID=1")
        