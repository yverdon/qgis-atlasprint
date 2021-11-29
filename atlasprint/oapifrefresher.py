from qgis.core import (
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsDataProvider,
)


class OAPIFRefresher:
    def __init__(self):
        self.plugin = "AtlasPrint"

    def refresh_geocity_oapif_layers_for_current_atlas_feature(atlas_pk):

        project = QgsProject.instance()
        crs = QgsCoordinateReferenceSystem("EPSG:2056")
        project.setCrs(crs)

        for layer in QgsProject.instance().mapLayers().values():
            if layer.dataProvider().name() == "OAPIF":
                uri = layer.dataProvider().uri()
                if uri.hasParam("url") and uri.hasParam("typename"):
                    if uri.param("typename") in [
                        "permits",
                        "permits_poly",
                        "permits_line",
                        "permits_point",
                    ]:
                        layer = project.mapLayersByName(uri.param("typename"))[0]
                        layer.setCrs(crs)
                        layer.updateFields()
                        provider = layer.dataProvider()
                        uri = provider.uri()
                        uri.setKeyColumn("permit_request_id")
                        uri.removeParam("url")
                        uri.setSrid("EPSG:2056")
                        # TODO: set url correctly for composition and current atlas PK
                        uri.setParam(
                            "url", "http://localhost:9095/wfs3/?permit_request_id=4"
                        )
                        layer.setDataSource(
                            uri.uri(expandAuthConfig=False),
                            uri.param("typename"),
                            "OAPIF",
                            QgsDataProvider.ProviderOptions(),
                        )
                        layer.dataProvider().updateExtents()
                        layer.dataProvider().reloadData()
                        layer.triggerRepaint()
