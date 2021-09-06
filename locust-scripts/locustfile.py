import math
from locust import HttpUser, TaskSet, task, constant
from locust import LoadTestShape


class UserTasks(TaskSet):
    @task
    def get_root(self):
        self.client.get("/uuid-gen/generate")


class WebsiteUser(HttpUser):
    wait_time = constant(0.25)
    tasks = [UserTasks]


class DoubleWave(LoadTestShape):
    """
    A shape to immitate some specific user behaviour. In this example, midday
    and evening meal times. First peak of users appear at time_limit/3 and
    second peak appears at 2*time_limit/3

    Settings:
        min_users -- minimum users
        peak_one_users -- users in first peak
        peak_two_users -- users in second peak
        time_limit -- total length of test
    """

    min_users = 50
    peak_users = [320, 380, 720, 800, 390, 460, 740, 790, 460, 540, 700, 840]
    time_limit = 7200
    peak_count = 12

    def tick(self):
        run_time = round(self.get_run_time())

        if run_time < self.time_limit:
            user_count = 0
            if run_time >= (self.time_limit*0.25) and run_time <= (self.time_limit*0.26):
                user_count = 950
            elif run_time > (self.time_limit*0.33) and run_time <= (self.time_limit*0.34):
                user_count = 1100
            elif run_time > (self.time_limit*0.42) and run_time <= (self.time_limit*0.425):
                user_count = 1000
            elif run_time > (self.time_limit*0.61) and run_time <= (self.time_limit*0.62):
                user_count = 1050
            elif run_time > (self.time_limit*0.82) and run_time <= (self.time_limit*0.83):
                user_count = 1100
            elif run_time > (self.time_limit*0.75) and run_time <= (self.time_limit*0.765):
                user_count = 950
            else:
                user_count = self.min_users
                for i in range(self.peak_count):
                    user_count += (self.peak_users[i] - self.min_users) * math.e ** -(((run_time / (self.time_limit / (5*self.peak_count) * self.peak_count / (self.peak_count + 1))) - 5*(i + 1)) ** 2)
            return (round(user_count), round(user_count))
        else:
            return None