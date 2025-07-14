from crimson_logger.src.crimson_log_config import CrimsonLogConfig
from abc import ABC, abstractmethod

class CrimsonSink(ABC):
    """Create Custom Sink for sending log output
    DB sinks must use db_ip_address and db_port from config
    
    All the classes must be implemented for sink to work
    """
    
    @abstractmethod
    def configure(self, config: CrimsonLogConfig):
        pass
    
    @abstractmethod
    def write(self, message: str):
        pass