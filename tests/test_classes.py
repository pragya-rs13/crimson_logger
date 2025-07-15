from crimson_logger.src.crimson_config_parser import CrimsonConfigParser
from crimson_logger.src.crimson_log_config import CrimsonLogConfig
from crimson_logger.src.crimson_file_sink import CrimsonFileSink
from crimson_logger.src.sync_writer import SyncWriter
from crimson_logger.src.async_writer import AsyncWriter
from crimson_logger.src.crimson_logger import CrimsonLoggerBuilder
import pytest
import datetime


@pytest.fixture
def config_dict():
    file_path = "crimson_logger/tests/file_config.txt"
    return CrimsonConfigParser.parse(file_path)


@pytest.fixture
def config_obj(config_dict):
    return CrimsonLogConfig.from_dict(config_dict)


@pytest.fixture
def file_sink(config_obj):
    return CrimsonFileSink().configure(config_obj)


def test_class_01_file_sink(config_obj, file_sink):
    msg = "This is a sample log."
    test_file = open(config_obj.file_location, "w")
    test_file.close()
    file_sink.write(msg)

    with open(config_obj.file_location, "r") as log_file:
        for line in log_file:
            assert line == (msg + "\n")


@pytest.fixture
def sync_writer(file_sink):
    return SyncWriter().set_sink(file_sink)


def test_class_02_sync_writer(sync_writer, config_obj):
    message = "Test Log message 2"
    test_file = open(config_obj.file_location, "w")
    test_file.close()
    sync_writer.write_to_sink(message=message)

    with open(config_obj.file_location, "r") as log_file:
        for line in log_file:
            assert line == (message + "\n")


@pytest.fixture
def async_writer(file_sink):
    writer = AsyncWriter().set_sink(file_sink)
    writer.start()
    return writer


def test_class_03_async_writer(async_writer, config_obj):
    msg = "Test Log message 3"
    test_file = open(config_obj.file_location, "w")
    test_file.close()

    async_writer.write_to_sink(msg)
    async_writer.stop()
    async_writer.join()

    with open(config_obj.file_location, "r") as log_file:
        for line in log_file:
            assert line == (msg + "\n")


def test_class_04_logger_building(config_obj, file_sink, sync_writer):
    logger = (
        CrimsonLoggerBuilder()
        .with_config("crimson_logger/tests/file_config.txt")
        .with_custom_sink(file_sink)  # using this because I'm providing instance
        .with_custom_writer(sync_writer)
        .set_formatter()
        .build()
    )

    assert logger._config == config_obj
    assert logger._writer == sync_writer
    assert logger._formatter._ts_format == "%d-%m-%Y %H:%M:%S"


def test_05_if_logger_works(config_obj):
    test_file = open(config_obj.file_location, "w")
    test_file.close()

    logger = (
        CrimsonLoggerBuilder()
        .with_config("crimson_logger/tests/file_config.txt")
        .set_formatter()
        .set_sink()
        .set_writer()
        .build()
    )

    logger.warn("Testing Logger", "test_case_5")
    test_ts = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    log_text = f"[test_case_5] WARN [{test_ts}] Testing Logger\n"

    with open(config_obj.file_location, "r") as log_file:
        for line in log_file:
            assert log_text == line
    
    logger.close()
