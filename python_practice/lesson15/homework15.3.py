import logging
import xml.etree.ElementTree as ET
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("xml_search")

xml_file = Path(__file__).parent / "groups.xml"


def find_incoming(path, group_number):
    """Шукає group за <number> і повертає значення <timingExbytes>/<incoming>."""
    root = ET.parse(path).getroot()
    for group in root.findall("group"):
        if group.findtext("number", "").strip() == str(group_number):
            incoming = group.findtext("timingExbytes/incoming")
            if incoming is None:
                logger.info("Група %s знайдена, але timingExbytes/incoming відсутній", group_number)
                return None
            logger.info("Група %s: incoming = %s", group_number, incoming.strip())
            return incoming.strip()
    logger.info("Групу з number=%s не знайдено", group_number)
    return None


if __name__ == "__main__":
    for n in (0, 1, 2, 3, 4, 5):
        find_incoming(xml_file, n)