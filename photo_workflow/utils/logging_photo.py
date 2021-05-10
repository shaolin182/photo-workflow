"""
Configure logging for photo-workflow tools
"""
import logging
import logging.config
import pkg_resources
import yaml

logging_conf_file = pkg_resources.resource_stream(__name__, "logging.yaml")
logging.config.dictConfig(yaml.safe_load(logging_conf_file))

logger = logging.getLogger()
