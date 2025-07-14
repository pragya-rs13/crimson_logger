from crimson_logger.src.crimson_writer import CrimsonWriter
from crimson_logger.src.crimson_sink import CrimsonSink
from threading import Lock

class SyncWriter(CrimsonWriter):
    def __init__(self):
        super().__init__()
        self.lock = Lock()
        
    def set_sink(self, sink: CrimsonSink):
        self._sink = sink
        
        return self
        
    def write_to_sink(self, message: str):
        with self.lock:
            self._sink.write(message)