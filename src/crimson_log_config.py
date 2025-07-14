from crimson_logger.src.log_level import LogLevel
from dataclasses import dataclass
from crimson_logger.src.write_mode import WriteMode
from crimson_logger.src.thread_model import ThreadModel


@dataclass
class CrimsonLogConfig:
    ts_format: str
    db_ip_address: str
    db_port: str
    log_level: LogLevel
    sink_type: str = "FILE"
    thread_model: ThreadModel = ThreadModel.SINGLE
    write_mode: WriteMode = WriteMode.SYNC
    file_location: str = "logs/application.log"

    @staticmethod
    def from_dict(cfg: dict[str, str]):
        """
        Create CrimsonLogConfig object from config dict
        """

        return CrimsonLogConfig(
            ts_format=cfg["ts_format"],
            log_level=LogLevel(cfg["log_level"]),
            sink_type=cfg["sink_type"],
            thread_model=ThreadModel(cfg.get("thread_model", "SINGLE")),
            write_mode=WriteMode(cfg.get("write_mode", "SYNC")),
            file_location=cfg.get("file_location", ""),
            db_ip_address=cfg.get("db_ip_address"),
            db_port=cfg.get("db_port", ""),
        )
