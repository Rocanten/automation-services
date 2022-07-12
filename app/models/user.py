from pydantic import BaseModel, validator
from typing import List, Optional

class User(BaseModel):
	email: str
	yandex_id: Optional[int]
	name: Optional[str]
	surname: Optional[str]
	display_name: Optional[str]
	department_id: Optional[int]
