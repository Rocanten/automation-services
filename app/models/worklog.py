from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

class Worklog(BaseModel):
	author_email: str
	created: datetime
	start: datetime
	duration: int
	issue_key: Optional[str] = None
	project: Optional[str] = None
	comment: Optional[str] = ''
	author_yandex_id: Optional[int] = None
	author_name: Optional[str] = None
	issue_summary: Optional[str] = None
	status: Optional[str] = None
	jira_issue_id: Optional[int] = None

	def to_dict(self):
		return {
			'author_email': self.author_email,
			'created': self.created,
			'start': self.start.date(),
			'start_date': self.start.strftime('%Y-%m-%d'),
			'issue_key': self.issue_key,
			'comment': self.comment,
			'author_id': self.author_yandex_id,
			'author_name': self.author_name,
			'project': self.project,
			'issue_summary': self.issue_summary,
			'status': self.status,
			'created': self.created,
			'duration': self.duration
		}
