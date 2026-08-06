from typing import Any

# ===========================
# Basic Type Hints
# ===========================

text: str = "string"
pert: int = 90
temp: float = 9.09

# Can store either an int or a float
num: int | float = 12


# ===========================
# Class Example
# ===========================

class City:
    
    # It doesn't return anything, so its return type is None.
    def __init__(self, name: str, location: int) -> None:
        self.name: str = name
        self.location: int = location


# ===========================
# Function Example
# ===========================

# Accepts either an int or a float.
# Always returns a float.
def root(num: float) -> float:
    return pow(num, 0.5)

root_25 = root(25)
print(root_25)


# ===========================
# List Type Hint
# ===========================

# A list containing only integers.
digits: list[int] = [1, 2, 3, 4, 5]


# ===========================
# Tuple Type Hints
# ===========================

# A tuple containing any number of integers.
# The ... (ellipsis) means:
# "This tuple can contain as many int values as needed."
table_5: tuple[int, ...] = (1, 2, 3, 4, 5)


# Create a City object
london = City("London", 678547554)

# Tuple containing:
#   - a City object
#   - a float (temperature)
city_temp: tuple[City, float] = (london, 34.5)


# ===========================
# Dictionary Type Hint
# ===========================

# Dictionary where:
#   Keys are strings.
#   Values can be ANY type.
shipment: dict[str, Any] = {
    "id": 657880,             # int
    "content": "wooden box",  # str
    "status": "in transit",   # str
    "weight": 96.4            # float
}