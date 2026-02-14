class Security:

    max_attempts = 3
    attempts = 0

    def __init__(self, max_attempts=3,  attempts=0):
        self.max_attempts = max_attempts
        self.attempts = attempts

    def track_attempts(self, cert_no: str):
        print(f"attempts: {self.attempts}")
        print(f"max_attempts: {self.max_attempts}")
        print(f"cert_no: {cert_no}")
        while self.attempts < self.max_attempts:
            if cert_no:
                return True
        else:
            self.attempts += 1
            if self.attempts >= self.max_attempts:
                return False
            else:
                return {"message": f"Certificate number: {cert_no} is invalid. Attempt {self.attempts} of {self.max_attempts}."}
