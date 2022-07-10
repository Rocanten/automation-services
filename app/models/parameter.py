from pydantic import BaseModel
from typing import List, Optional

class Parameter(BaseModel):
	name: str
	value: str