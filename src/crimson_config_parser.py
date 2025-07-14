import os


class CrimsonConfigParser:
    """
    Parser for reading config files
    supports .txt

    Returns:
        a dict of parsed key,value pairs from config file
    """

    @staticmethod
    def parse(config_file: str) -> dict[str, str]:
        config = {}
        if not os.path.exists(config_file):
            raise Exception("[Parse Error] Config file does not exist")

        with open(config_file, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    if line.startswith("ts_format"):
                        key, val = line.split(":", 1)
                        config[key.strip()] = val.strip()

                    else:
                        properties = line.split()

                        for item in properties:
                            key, val = item.split(":")
                            key = key.strip()
                            val = val.strip()
                            if key in [
                                "log_level",
                                "sink_type",
                                "thread_model",
                                "write_mode",
                            ]:
                                config[key] = val.upper()
                            else:
                                config[key] = val

        return config
