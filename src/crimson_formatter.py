from datetime import datetime
from crimson_logger.src.crimson_log_config import CrimsonLogConfig
from crimson_logger.src.config_exception import ConfigException

class Formatter:
    '''
    Configure formatter for logger
    '''
    
    def __init__(self) -> None:
        self._ts_format = None
        self._is_valid = False
        self.replacement_map = {
            "dd": "%d",
            "mm": "%m",
            "yyyy": "%Y",
            "hh": "%H",
            "MM": "%M",
            "ss": "%S",
        }
        
    def configure(self, config: CrimsonLogConfig):
        '''
            Convert given format to valid strftime format
            accepted ts items in format: 
                dd - date
                mm - month
                yyyy - year
                hh - hour
                MM - minutes
                ss - seconds
                
            Args:
                config (CrimsonLogConfig): set format from config
                
            Returns:
                instance
        '''
        
        formatter = config.ts_format
        
        for key in self.replacement_map:
            formatter = formatter.replace(key, self.replacement_map[key])

        self._ts_format = formatter
        
        return self
        
    def _is_valid_strftime_format(self) -> bool:
        try:
            datetime.now().strftime(self._ts_format)
            return True
        except ValueError:
            return False
        
    def _validate(self):
        errors = []        
        
        if not self._ts_format:
            errors += "Format was not provided"
        
        if not self._is_valid_strftime_format():
            errors += "Incorrect datetime format"
            
        error_list = "\n".join(errors)
        
        error_msg = f"Errors in Formatter: {error_list}"
        
        if errors:
            print(error_msg)
            raise ConfigException(error_msg)
        else:
            self._is_valid = True
    
    def format_message(self, log_level, message_content: str, namespace: str) -> str:
        '''Get formatted message with timestamp
        Args:
            log_level (str): log's lvl
            message_content (str): log message
            namespace (str): log source
        
        Raises:
            Exception: when formatting error occurs
        '''
        if not self._is_valid:
            self._validate()
            
        try:
            formatted_ts = datetime.now().strftime(self._ts_format)
            log_msg = f"[{namespace}] {log_level} [{formatted_ts}] {message_content}"
            return log_msg
        
        except Exception as e:
            print(f"[ERROR] Some error occurred: {e}")
        