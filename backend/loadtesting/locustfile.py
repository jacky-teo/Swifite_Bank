import time
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def login(self):
        self.client.get(url = "/customer?service=login&username=customer1")