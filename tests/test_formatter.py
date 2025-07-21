from crimson_logger.src.crimson_config_parser import CrimsonConfigParser
from crimson_logger.src.crimson_log_config import CrimsonLogConfig
from crimson_logger.src.crimson_formatter import Formatter
import datetime


def test_formatter_class():
    file_path = "/Users/pragya/ws/interviews/phonepe_machine_round/crimson_logger/tests/file_config.txt"
    config_dict = CrimsonConfigParser.parse(file_path)
    config_obj = CrimsonLogConfig.from_dict(config_dict)
    formatter = Formatter().configure(config_obj)
    msg = "This is a test log"
    log_level = "INFO"
    namespace = "test_formatter_class"

    formatted_text = formatter.format_message(
        log_level=log_level, message_content=msg, namespace=namespace
    )

    test_ts = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    assert formatted_text == f"[{namespace}] {log_level} [{test_ts}] {msg}"
