from crimson_logger.src.crimson_sink import CrimsonSink
from abc import ABC, abstractmethod

class CrimsonWriter(ABC):
    """Create Custom Writer for writing logs
    
    Must implement all methods
    """
    
    @abstractmethod
    def set_sink(self, sink: CrimsonSink):
        pass
    
    @abstractmethod
    def write_to_sink(self, message: str) -> None:
        pass