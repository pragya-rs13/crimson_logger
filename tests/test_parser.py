from crimson_logger.src.crimson_config_parser import CrimsonConfigParser
from crimson_logger.src.crimson_log_config import CrimsonLogConfig

def test_parser():
    file_path = "crimson_logger/tests/file_config.txt"
    config = CrimsonConfigParser.parse(file_path)
    assert config == {
        'ts_format': 'dd-mm-yyyy hh:MM:ss',
        "log_level": "INFO",
        "sink_type": "FILE",
        "file_location": "tmp/info.log",
        "thread_model": "SINGLE",
        "write_mode": "SYNC",
    }

def test_config_obj():
    file_path = "crimson_logger/tests/file_config.txt"
    config_dict = CrimsonConfigParser.parse(file_path)
    config_obj = CrimsonLogConfig.from_dict(config_dict)

    assert config_obj.file_location == "tmp/info.log"
    assert config_obj.write_mode.value == "SYNC"
    assert config_obj.thread_model.value == "SINGLE"
    assert config_obj.log_level.value == "INFO"
    assert config_obj.sink_type == "FILE"
    assert config_obj.ts_format == "dd-mm-yyyy hh:MM:ss"
    
    
