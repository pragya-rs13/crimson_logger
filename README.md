# CrimsonLogger 🩸🧱

**CrimsonLogger** is a lightweight, extensible, and configurable logging library built in Python without using the built-in `logging` module. 
It supports writing logs to sinks (e.g., file), with configurable timestamp formats, log levels, thread models (SINGLE or MULTI), and write modes (SYNC or ASYNC).

> 🔐 **Note:** This project is licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/).  
> Commercial use, redistribution, or derivative works are **strictly prohibited**.

---

## 🔧 Features

- Simple `.txt` config file for logger setup
- Log rotation and `.gz` compression (file sink)
- Configurable log levels (`INFO`, `WARN`, `ERROR`, `DEBUG`, `FATAL`)
- Sync and Async writer support
- Thread model awareness (`SINGLE`, `MULTI`)
- Custom formatter with timestamp support
- Extensible with your own sinks
---

## 📦 Installation

```bash
git clone https://github.com/pragya-rs13/crimson_logger.git
cd crimson_logger

## Sample Config File
```
ts_format:dd-mm-yyyy hh:MM:ss 
log_level:INFO sink_type:FILE 
file_location:tmp/info.log
thread_model:SINGLE 
write_mode:SYNC
```

📄 Configuration File Format

Sample file_config.txt:

ts_format:dd-mm-yyyy hh:MM:ss
log_level:INFO
sink_type:FILE
file_location:/tmp/crimson.log
thread_model:SINGLE
write_mode:SYNC

🚀 Usage
1. Build the Logger using Builder Pattern

from crimson_logger.src.crimson_logger import CrimsonLoggerBuilder

logger = (
    CrimsonLoggerBuilder()
    .with_config("crimson_logger/tests/file_config.txt")
    .set_sink()
    .set_writer()
    .set_formatter()
    .build()
)

2. Log Messages

logger.info("App started", "main")
logger.warn("Something unusual", "auth")
logger.error("Unhandled exception", "worker")

🧪 Testing
Run tests using pytest:

pytest crimson_logger/tests/

Example test case (uses real file sink):

def test_logger_logs_correctly(config_obj):
    logger = (
        CrimsonLoggerBuilder()
        .with_config("crimson_logger/tests/file_config.txt")
        .set_sink()
        .set_writer()
        .set_formatter()
        .build()
    )
    logger.warn("Sample warning", "test")
    logger.close()

🔌 Extending with Custom Sink

from crimson_logger.src.crimson_sink import CrimsonSink

class MyCustomSink(CrimsonSink):
    def configure(self, config):
        ...
    
    def write(self, message: str):
        ...

Then use:

builder = CrimsonLoggerBuilder().with_custom_sink(MyCustomSink())

📚 Project Structure

crimson_logger/
├── src/
│   ├── crimson_logger.py
│   ├── crimson_config_parser.py
│   ├── crimson_file_sink.py
│   ├── sync_writer.py
│   ├── async_writer.py
│   └── ...
├── tests/
│   └── test_classes.py
├── LICENSE
└── README.md

### Author

Built by Pragya Sinha for educational and personal use.
For questions or improvements, raise an issue or PR — but remember, this is not licensed for production use.
