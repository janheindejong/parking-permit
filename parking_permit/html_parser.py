import re

from parking_permit.agent import QueueEntry

from .queue_service import HtmlParserProtocol

PATTERN = re.compile(
    r"<h3 class=label>Uw parkeervergunning voor</h3>\n"
    r"<p class=value>(?P<license_plate>.*?)</p>"
    r".*"
    r"<h3 class=label>Huidige wachtlijstpositie</h3>\n"
    r"<p class=value>(?P<position>.*?)</p>"
    r".*"
    r"<h3 class=label>Vergunninggebied</h3>\n"
    r"<p class=value>(?P<area>.*?)</p>",
    re.DOTALL,
)


class HtmlParser(HtmlParserProtocol):
    """Parser the raw HTML response from the parking permit database"""

    def parse(self, html: str) -> QueueEntry:
        entry = QueueEntry(html=html, **self._get_named_groups_dict(html))
        return entry

    def _get_named_groups_dict(self, html: str) -> dict:
        match = PATTERN.search(html)
        if match:
            d = match.groupdict()
        else:
            raise Exception("Uh-oh; Regex failed")
        d["position"] = int(d["position"])
        return d
