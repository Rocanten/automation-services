from pydantic import BaseModel, validator
from typing import List, Optional

class User(BaseModel):
	email: str
	yandex_id: Optional[int]
	name: Optional[str]
	surname: Optional[str]
	display_name: Optional[str]
	department_id: Optional[int]

@validator('surname', always=True)
def validate_display_surname(cls, value, values):
		if 'name' in values:
			name = values['name']
			return f'{name} {value}'
		return f'Mr. {value}'
