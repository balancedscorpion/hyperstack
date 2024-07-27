import os
import requests

class Hyperstack:
    def __init__(self):
        self.api_key = os.environ.get("HYPERSTACK_API_KEY")
        if not self.api_key:
            raise EnvironmentError("HYPERSTACK_API_KEY environment variable not set. Please set it to continue.")
        self.base_url = "https://infrahub-api.nexgencloud.com/v1/"
        self.headers = {
            "Content-Type": "application/json",
            "api_key": self.api_key
        }
        self.valid_regions = ["NORWAY-1", "CANADA-1"]
        self.environment = None

    def set_environment(self, environment):
        self.environment = environment
        print(f"Environment set to: {self.environment}")

    def _check_environment_set(self):
        if self.environment is None:
            raise EnvironmentError("Environment is not set. Please set the environment using set_environment().")
        print(f"Current environment: {self.environment}")

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response