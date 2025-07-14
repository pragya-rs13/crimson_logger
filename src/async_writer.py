from threading import Thread
from queue import Queue, Empty
from crimson_logger.src.crimson_writer import CrimsonWriter, CrimsonSink

class AsyncWriter(CrimsonWriter, Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self._queue = Queue()
        self._active = True
    
    def set_sink(self, sink: CrimsonSink):
        self._sink = sink
        return self
        
    def run(self) -> None:
        while self._active or not self._queue.empty():
            try:
                log = self._queue.get(timeout=1)
                self._sink.write(log)
            except Empty:
                continue
            
    def write_to_sink(self, message: str) -> None:
        self._queue.put(message)
    
    def stop(self):
        self._active = False
        
        