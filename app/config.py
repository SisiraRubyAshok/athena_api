import os
from dotenv import load_dotenv

load_dotenv()


AWS_REGION = os.getenv("AWS_REGION")

ATHENA_DATABASE = os.getenv("ATHENA_DATABASE")
ATHENA_TABLE = os.getenv("ATHENA_TABLE")
ATHENA_OUTPUT = os.getenv("ATHENA_OUTPUT")