import logging
from datetime import datetime

KEY = "Key TSTFEED0300|7E3E|0400"
LOG_FILE = "hb_test.log"
TIME_FORMAT = "%H:%M:%S"


def read_filtered_lines(path, key=KEY):
    """Читає файл по рядках і лишає тільки рядки з потрібним ключем."""
    filtered_log = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            if key in line:
                filtered_log.append(line.rstrip("\r\n"))
    return filtered_log


def extract_time(line):
    """Знаходить 'Timestamp ' і повертає наступні 8 символів як datetime."""
    pos = line.find("Timestamp ")
    if pos == -1:
        return None
    start = pos + len("Timestamp ")
    try:
        return datetime.strptime(line[start:start + 8], TIME_FORMAT)
    except ValueError:
        return None


def analyze_heartbeat(path, key=KEY, log_file=LOG_FILE):
    logger = logging.getLogger("hb_test")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(handler)

    lines = read_filtered_lines(path, key)
    times = [t for t in (extract_time(l) for l in lines) if t is not None]

    warnings = errors = 0
    # Лог іде у зворотному порядку: від поточного віднімаємо наступне.
    for t_cur, t_next in zip(times, times[1:]):
        delta = int((t_cur - t_next).total_seconds()) % 86400  # перехід через північ
        if delta >= 33:
            errors += 1
            logger.error("Heartbeat %s sec (>=33) | gap between %s and %s",
                         delta, t_next.strftime(TIME_FORMAT), t_cur.strftime(TIME_FORMAT))
        elif delta > 31:
            warnings += 1
            logger.warning("Heartbeat %s sec (>31 and <33) | gap between %s and %s",
                           delta, t_next.strftime(TIME_FORMAT), t_cur.strftime(TIME_FORMAT))

    logger.info("Analyzed %d heartbeats, WARNING: %d, ERROR: %d",
                len(times), warnings, errors)
    handler.close()
    return log_file


if __name__ == "__main__":
    print("Результат у файлі:", analyze_heartbeat("hblog.txt"))