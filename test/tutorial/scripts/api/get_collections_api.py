from dbio import DataBiosphereConfig
from dbio.dss import DSSClient

dbio_config = DataBiosphereConfig()
dbio_config["DSSClient"].swagger_url = f"https://dss.dev.data.humancellatlas.org/v1/swagger.json"
dss = DSSClient(config=dbio_config)

print(dss.get_collections())
