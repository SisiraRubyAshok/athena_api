import boto3
import time
import re

from app.config import (
    AWS_REGION,
    ATHENA_DATABASE,
    ATHENA_TABLE,
    ATHENA_OUTPUT
)


class AthenaService:

    def __init__(self):

        self.client = boto3.client(
            "athena",
            region_name=AWS_REGION
        )

    def get_vehicle_by_vin(self, vin):

        # Validate SQL identifiers from trusted configuration
        identifier_pattern = r"^[a-zA-Z0-9_]+$"

        if not re.fullmatch(identifier_pattern, ATHENA_DATABASE):
            raise ValueError("Invalid Athena database name")

        if not re.fullmatch(identifier_pattern, ATHENA_TABLE):
            raise ValueError("Invalid Athena table name")

        query = f"""
            SELECT *
            FROM {ATHENA_DATABASE}.{ATHENA_TABLE}
            WHERE vin = ?
            LIMIT 1
        """

        # Start Athena query
        response = self.client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                "Database": ATHENA_DATABASE
            },
            ResultConfiguration={
                "OutputLocation": ATHENA_OUTPUT
            },
            ExecutionParameters=[f"'{vin}'"]
        )

        query_execution_id = response["QueryExecutionId"]

        # Wait for query completion
        while True:

            result = self.client.get_query_execution(
                QueryExecutionId=query_execution_id
            )

            status = result["QueryExecution"]["Status"]["State"]

            if status == "SUCCEEDED":
                break

            elif status in ["FAILED", "CANCELLED"]:
                reason = result["QueryExecution"]["Status"].get(
                    "StateChangeReason", "Unknown Athena error"
                )
                raise RuntimeError(reason)

            time.sleep(1)

        # Retrieve query results
        result = self.client.get_query_results(
            QueryExecutionId=query_execution_id
        )

        rows = result["ResultSet"]["Rows"]

        # No vehicle found
        if len(rows) < 2:
            return None

        # Extract column names
        columns = [
            column["VarCharValue"]
            for column in rows[0]["Data"]
        ]

        # Extract vehicle values
        values = [
            cell.get("VarCharValue")
            for cell in rows[1]["Data"]
        ]

        vehicle = dict(zip(columns, values))

        return vehicle