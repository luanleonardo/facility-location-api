import orjson
from shapely import GeometryCollection, MultiPolygon, Polygon, from_geojson

TYPE_ERROR_MSG = (
    "Not a valid GeoJSON dictionary or valid geometry. "
    "Check the validity of the GeoJSON, or whether the "
    "geometry contains polygons with at least three "
    "distinct points."
)


def _get_inner_polygon(geometry: Polygon | MultiPolygon) -> list[Polygon]:
    if isinstance(geometry, Polygon):
        return [geometry]
    elif isinstance(geometry, MultiPolygon):
        return [polygon for polygon in geometry.geoms]
    return []


def _geojson_dict_to_multipolygon(
    geojson_dict: dict,
) -> MultiPolygon:
    """Convert a GeoJSON dictionary to a shapely MultiPolygon"""

    geometry = from_geojson(orjson.dumps(geojson_dict), on_invalid="ignore")

    if geometry is None or not isinstance(
        geometry, (MultiPolygon, Polygon, GeometryCollection)
    ):
        raise ValueError(TYPE_ERROR_MSG)

    if isinstance(geometry, MultiPolygon):
        return geometry

    if isinstance(geometry, Polygon):
        return MultiPolygon([geometry])

    inner_polygons: list[Polygon] = sum(
        [_get_inner_polygon(geo) for geo in geometry.geoms], []
    )

    if not inner_polygons:
        raise ValueError(TYPE_ERROR_MSG)

    return MultiPolygon(inner_polygons)


def _field_to_multipolygon(field: dict | MultiPolygon) -> MultiPolygon:
    """Convert a field to a shapely MultiPolygon"""

    if not isinstance(field, (dict, MultiPolygon)):
        raise ValueError(TYPE_ERROR_MSG)

    if isinstance(field, dict):
        return _geojson_dict_to_multipolygon(field)

    return field


def _build_valid_polygon(
    coordinates: list[list[float]],
) -> Polygon | None:
    """Build valid polygon"""

    valid_coordinates = list(dict.fromkeys(coordinates))
    if len(valid_coordinates) > 2:
        valid_coordinates.append(valid_coordinates[0])
        return Polygon(valid_coordinates)

    return None


def field_to_valid_multipolygon(field: dict | MultiPolygon) -> MultiPolygon:
    """Convert a field to a valid MultiPolygon"""

    field_multipolygon = _field_to_multipolygon(field=field)

    if field_multipolygon.is_empty:
        return MultiPolygon()

    valid_polygons = list(
        filter(
            lambda p: p is not None,
            [
                _build_valid_polygon(coordinates=list(polygon.exterior.coords))
                for polygon in field_multipolygon.geoms
            ],
        )
    )

    if not valid_polygons:
        raise ValueError(TYPE_ERROR_MSG)

    return MultiPolygon(valid_polygons)
