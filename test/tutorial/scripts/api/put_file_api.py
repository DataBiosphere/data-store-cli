from dbio import DataBiosphereConfig
from dbio.dss import DSSClient

dbio_config = DataBiosphereConfig()

dbio_config["DSSClient"].swagger_url = f"https://dss.dev.data.humancellatlas.org/v1/swagger.json"
dss = DSSClient(config=dbio_config)

print(
    dss.put_file(
        uuid="ead6434d-efb5-4554-98bc-027e160547c5",
        version="2019-07-30T174916.268875Z",
        creator_uid=0,
        source_url="s3://jeffwu-test/ead6434d-efb5-4554-98bc-027e160547c5/get_bundle.json",
    )
)
