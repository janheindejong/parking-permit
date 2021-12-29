from parking_permit.agent import QueueEntry


class HtmlParser:
    """Parser the raw HTML response from the parking permit database"""

    def parse(self, html: str) -> QueueEntry:
        ...
