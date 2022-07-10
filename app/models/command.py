from datetime import datetime

from pydantic import BaseModel, validator
from typing import List, Optional

from app.models.parameter import Parameter
from app.models.period import Period

class Command(BaseModel):
	raw: str
	name: Optional[str] = None
	parameters: List[Parameter] = []

	@validator("name", always=True)
	def validate_name(cls, value, values):
		if 'raw' in values:
			raw = values['raw']
			command = raw.split(' ')[0]
			if not command[0].isalpha():
				raise RuntimeError('Command must start with latin letter')
			return command
		raise ValueError("You haven't specified any command and parameter")

	@validator('parameters', always=True)
	def validate_parameters(cls, value, values):
		parameters = []
		if 'raw' in values:
			raw = values['raw']
			params = raw.split(' ')[1:]
			current_option = ''
			current_value = ''
			for item in params:
				if len(item) > 0 and item[0] == '-':
					if len(current_option) > 0:
						parameter = Parameter(name=current_option, value='')
						parameters.append(parameter)
					current_option = item[1:]
					continue
				current_value = item
				parameter = Parameter(name=current_option, value=current_value)
				parameters.append(parameter)
				current_option = ''
			if len(current_option) > 0:
				parameter = Parameter(name=current_option, value='')
				parameters.append(parameter)
		return parameters

	def get_option(self, option:str)->Parameter:
		result = next((param for param in self.parameters if param.name == option), None)
		return result

	def get_period(self)->Period:
		option = self.get_option('p')
		start = option.value.split('-')[0]
		end = option.value.split('-')[1]
		period = Period(start=start, end=end)
		return period

	def get_users(self) -> list:
		option = self.get_option('u')
		result = option.value.split(',')
		return result


