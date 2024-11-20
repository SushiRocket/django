import os
from dotenv import load_dotenv

load_dotenv()

print(f"EMAIL_HOST_USER: {os.getenv('EMAIL_HOST_USER')}")
print(f"EMAIL_HOST_PASSWORD: {os.getenv('EMAIL_HOST_PASSWORD')}")
