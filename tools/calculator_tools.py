from pydantic import BaseModel, Field
from langchain.tools import tool

# Define a Pydantic model for the tool's input parameters
class CalculationInput(BaseModel):
    operation: str = Field(..., description="The mathematical operation to perform")
    factor: float = Field(..., description="A factor by which to multiply the result of the operation")

# Use the tool decorator with the args_schema parameter pointing to the Pydantic model
@tool("perform_calculation", args_schema=CalculationInput, return_direct=True)
def perform_calculation(operation: str, factor: float) -> str:
    """
    Performs a specified mathematical operation and multiplies the result by a given factor.

    Parameters:
    - operation (str): A string representing a mathematical operation (e.g., "10 + 5").
    - factor (float): A factor by which to multiply the result of the operation.

    Returns:
    - A string representation of the calculation result.
    """
    # Perform the calculation
    result = eval(operation) * factor

    # Return the result as a string
    return f"The result of '{operation}' multiplied by {factor} is {result}."