from crimson_logger.src.crimson_log_config import CrimsonLogConfig
from crimson_logger.src.crimson_config_parser import CrimsonConfigParser
from crimson_logger.src.crimson_writer import CrimsonWriter
from crimson_logger.src.crimson_sink import CrimsonSink
from crimson_logger.src.crimson_formatter import Formatter
from crimson_logger.src.log_level import LogLevel
from crimson_logger.src.sync_writer import SyncWriter
from crimson_logger.src.async_writer import AsyncWriter
from crimson_logger.src.crimson_file_sink import CrimsonFileSink
from crimson_logger.src.config_exception import ConfigException
from crimson_logger.src.write_mode import WriteMode
from crimson_logger.src.thread_model import ThreadModel
import threading


class CrimsonLogger:
    """
    Logger Class
    """

    def __init__(
        self, config: CrimsonLogConfig, writer: CrimsonWriter, formatter: Formatter
    ):
        self._config = config
        self._writer = writer
        self._formatter = formatter
        self._log_level = config.log_level
        self._main_thread = (
            threading.current_thread()
            if self._config.thread_model == ThreadModel.SINGLE
            else None
        )

    def write_log(self, log_level: LogLevel, content: str, namespace: str):
        """Writes log to configured sink

        Args:
            log_level (LogLevel): Log levels - INFO, DEBUG, WARN, ERROR, FATAL
            content (str): Log message to be written
            namespace (str): source of the log

        Returns:
            None

        Raises:
            ValueError: if format config is wrong
            Exception: For cases like lock issues etc
        """

        if log_level >= self._log_level:
            if self._config.thread_model == ThreadModel.SINGLE:
                # decoupled write mode from thread model
                # at this point we can only warn if thread mode is not respected by user
                if (
                    self._main_thread
                    and threading.current_thread() != self._main_thread
                ):
                    print("[WARN] Logger is configured for SINGLE thread")

            msg = self._formatter.format_message(log_level.value, content, namespace)
            self._writer.write_to_sink(msg)

    def debug(self, content: str, namespace: str):
        """Writes DEBUG log to configured sink

        Args:
            content (str): Log message to be written
            namespace (str): source of the log

        Returns:
            None

        Raises:
            ValueError: if format config is wrong
            Exception: For cases like lock issues etc
        """

        self.write_log(LogLevel.DEBUG, content=content, namespace=namespace)

    def info(self, content: str, namespace: str):
        """Writes INFO log to configured sink

        Args:
            content (str): Log message to be written
            namespace (str): source of the log

        Returns:
            None

        Raises:
            ValueError: if format config is wrong
            Exception: For cases like lock issues etc
        """
        self.write_log(LogLevel.INFO, content=content, namespace=namespace)

    def warn(self, content: str, namespace: str):
        """Writes WARN log to configured sink

        Args:
            content (str): Log message to be written
            namespace (str): source of the log

        Returns:
            None

        Raises:
            ValueError: if format config is wrong
            Exception: For cases like lock issues etc
        """
        self.write_log(LogLevel.WARN, content=content, namespace=namespace)

    def error(self, content: str, namespace: str):
        """Writes ERROR log to configured sink

        Args:
            content (str): Log message to be written
            namespace (str): source of the log

        Returns:
            None

        Raises:
            ValueError: if format config is wrong
            Exception: For cases like lock issues etc
        """
        self.write_log(LogLevel.ERROR, content=content, namespace=namespace)

    def fatal(self, content: str, namespace: str):
        """Writes FATAL log to configured sink

        Args:
            content (str): Log message to be written
            namespace (str): source of the log

        Returns:
            None

        Raises:
            ValueError: if format config is wrong
            Exception: For cases like lock issues etc
        """
        self.write_log(LogLevel.FATAL, content=content, namespace=namespace)

    def close(self):
        """
        Function to close logger in case it is ASYNC
        """
        if self._config.write_mode == WriteMode.ASYNC:
            self._writer.stop()
            self._writer.join()

        # in case of custom writers which is may be like async
        if hasattr(self._writer, "stop"):
            self._writer.stop()
        if hasattr(self._writer, "join"):
            self._writer.join()


class CrimsonLoggerBuilder:
    """
    Builder class for logger
    """

    def __init__(self, name: str = "CrimsonLogger"):
        """Inits Builder

        Args:
            name (str): Logger name, defaults to CrimsonLogger
        """
        self._name = name

    def with_custom_sink(self, sink: CrimsonSink):
        """Set custom sink

        Args:
            sink (CrimsonSink): Provide your own implementation of CrimsonSink here

        Raises:
            ConfigException: if config has not been set before this step
        """

        if not self._config:
            raise ConfigException(
                "[ERROR] Config init is the first step, please use `with_config(__config_path))` method first"
            )

        self._sink = sink
        self._sink.configure(config=self._config)

        return self

    def set_sink(self):
        """Set Library provided sink (FileSink)

        Raises:
            ConfigException: if config has not been set before this step
        """
        if not self._config:
            raise ConfigException(
                "[ERROR] Config init is the first step, please use `with_config(__config_path))` method first"
            )

        if self._config.sink_type == "FILE":
            self._sink = CrimsonFileSink().configure(self._config)
        else:
            raise ConfigException(
                "[ERROR] Configuration is not for file type sink \n"
                + "Please use `with_custom_sink` method"
            )
        return self

    def set_writer(self):
        """Sets writer based on write_mode in config

        Raises:
            ConfigException: if config or writer has not been set before this step
        """
        if not self._config:
            raise ConfigException(
                "[ERROR] Config init is the first step, please use `with_config(__config_path))` method first"
            )

        if self._config.write_mode == WriteMode.SYNC:
            self._writer = SyncWriter().set_sink(self._sink)
            if self._config.thread_model == ThreadModel.MULTI:
                print(
                    "[WARN] thread_model MULTI with Sync Writer may block calling threads"
                )

        elif self._config.write_mode == WriteMode.ASYNC:
            self._writer = AsyncWriter().set_sink(self._sink)
            self._writer.start()
            if self._config.thread_model == ThreadModel.SINGLE:
                print(
                    "[WARN] thread_model SINGLE with Async Writer may delay logs until close() is called"
                )
        else:
            raise ConfigException(
                "[ERROR] Unknown writer type passed, please use `with_custom_writer` while building"
            )

        return self

    def with_custom_writer(self, writer: CrimsonWriter):
        """Set custom writer

        Args:
            sink (CrimsonWriter): Provide your own implementation of CrimsonWriter here

        Raises:
            ConfigException: if config or sink has not been set before this step
        """

        if not self._config:
            raise ConfigException(
                "[ERROR] Config init is the first step, please use `with_config(__config_path))` method first"
            )

        if not self._sink:
            raise ConfigException(
                "[ERROR] Sink set up is required before this step, please use set_sink or use_custom_sink method"
            )

        self._writer = writer
        self._writer.set_sink(self._sink)

        if hasattr(self._writer, "start"):
            self._writer.start()

        return self

    def set_formatter(self):
        """Set Formatter

        Raises:
            ConfigException: if config has not been set before this step
        """
        if not self._config:
            raise ConfigException(
                "[ERROR] Config init is the first step, please use `with_config(__config_path))` method first"
            )

        self._formatter = Formatter()
        self._formatter.configure(config=self._config)

        return self

    def with_config(self, config_file: str, custom_config=None):
        """Set config

        Args:
            config_file (str): Provide your config file
            custom_config (optional, CrimsonLogConfig): custom config obj here (Should inherit CrimsonLogConfig class)

        Raises:
            Exception: if config file does not exist

        """
        if custom_config:
            self._config = custom_config
            return self
        
        cfg = CrimsonConfigParser.parse(config_file=config_file)
        self._config = CrimsonLogConfig.from_dict(cfg)

        return self

    def build(self):
        """Builds Crimson logger after validating attributes

        Args:
            None

        Raises:
            ConfigException: if configuration step was missed
        """

        # validation
        if not all(
            [self._config, self._formatter, self._sink, self._writer, self._name]
        ):
            raise ConfigException(
                "LoggerBuilder not fully initialized. Missing Attributes"
            )

        return CrimsonLogger(
            config=self._config, writer=self._writer, formatter=self._formatter
        )
