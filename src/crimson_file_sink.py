from crimson_logger.src.crimson_log_config import CrimsonLogConfig
from crimson_logger.src.crimson_sink import CrimsonSink
import os
import shutil
import gzip
from crimson_logger.src.config_exception import ConfigException

class CrimsonFileSink(CrimsonSink):
    '''
    Write log to file
    - Can chain calls with instantiation 
    '''
    
    def __init__(self) -> None:
        super().__init__()
        self._type = "FILE"
        self._file_path = None
        self._max_file_size = 1_000_000  # (1MB)
        self._file = None
        self._is_valid = False
        
    def configure(self, config: CrimsonLogConfig, max_file_size: int = None):
        """
        Configure file path

        Args:
            config (CrimsonLogConfig): Pass config object to configure file path
            [optional] max_file_size: Set rotation file size
        
        Returns:
            instance of class
        """
        
        self._file_path = config.file_location
        
        dir_path = dir_path = os.path.dirname(self._file_path)
        os.makedirs(dir_path, exist_ok=True)
        
        self._file = open(self._file_path, 'a')
        
        if max_file_size:
            self._max_file_size = max_file_size
        
        return self
        
    
    def _rotate(self):
        '''
        rotates log file
        '''
        
        self._file.close()
        
        i = 1
        while os.path.exists(f"{self._file_path}.{i}.gz"):
            i += 1
            
        with (
            open(self._file_path, "rb") as logfile,
            gzip.open(f"{self._file_path}.{i}.gz", "wb") as compressed_log,
        ):
            shutil.copyfileobj(logfile, compressed_log)
            
        open(self._file_path, 'w').close()
        self._file = open(self._file_path, 'a')
    
    def _reached_size_limit(self):
        return os.path.getsize(self._file_path) > self._max_file_size
    
    def _validate_config(self):
        errors = []
        if not self._file_path:
            errors += "File Path was not configured"
            
        if not self._file:
            errors += "File was not opened"
        
        if errors:
            error_msg = "\n".join(errors)
            print(f"Found following errors: {error_msg}")
            raise ConfigException("File Sink has not been correctly configured")
        else :
            self._is_valid = True
        
    def write(self, message: str):
        """
        Write to file

        Args:
            message (str): formatted message to write to file
            
        Raises:
            Exception: in case error while writing to file
        """
        if not self._is_valid:
            self._validate_config() 
        
        try:  
            if self._reached_size_limit():
                self._rotate()
                
            self._file.write(message + "\n")
            self._file.flush()
            
        except Exception as e:
            print(f"[Error] Error while writing to file: {e}")
