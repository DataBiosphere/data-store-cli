from .config import DSSConfig, get_config, logger
from . import dss, upload, auth, query


def clear_dss_cache(args):
    """Clear the cached DSS API definitions. This can help resolve errors communicating with the API."""
    from dss.util import SwaggerClient
    for swagger_client in SwaggerClient.__subclasses__():
        swagger_client().clear_cache()
