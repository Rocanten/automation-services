from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, validator

class Period(BaseModel):
	start: str
	end: str
	startdate: Optional[datetime]
	enddate: Optional[datetime]

	@validator('startdate', always=True)
	def validate_start(cls, value, values):
		if 'start' not in values:
			raise RuntimeError('Start date not provided')
		return datetime.strptime(values['start'], '%d.%m.%Y')

	@validator('enddate', always=True)
	def validate_end(cls, value, values):
		if 'end' not in values:
			raise RuntimeError('End date not provided')
		return datetime.strptime(values['end'], '%d.%m.%Y')