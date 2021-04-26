from pyproj.crs import CRS
import geopandas as gpd

from backendstorage.ShapelyCustomizations._FantasyCRS import _FantasyCRS

from shapely.geometry import Point,Polygon
import matplotlib.pyplot as plt

class FantasyCRS(CRS):
    def __init__(self, width, height, **kwargs):
        """
        Yes I did make my own coordinates shoosh u
        """
        self._fantasy_proj_string = self.make_proj_str()
        # self._fantasy_CRS = _FantasyCRS(proj_string=self._fantasy_proj_string)
        super(FantasyCRS, self).__init__(self._fantasy_proj_string,**kwargs)
        self.width = width
        self.height = height

    def make_proj_str(
            self,proj='cart',lat_0=0,lon_0=0,
            x_0=0,y_0=0,ellps='sphere',
            units='km'
    ):
        # self,proj='lcc',lat_1=51.16666723333333,lat_2=49.8333339,lat_0=90,lon_0=4.367486666666666,
        #             x_0=150000.013,y_0=5400088.438,ellps='intl',towgs84='106.869,-52.2978,103.724,-0.33657,0.456955,-1.84218,1',
        #             units='m'
        proj_str = "+proj={proj:} " \
                   "+lat_0={lat_0:} " \
                   "+lon_0={lon_0:} " \
                   "+x_0={x_0:} " \
                   "+y_0={y_0:} " \
                   "+ellps={ellps:} " \
                   "+units={units:} " \
                   "+no_defs".format(
            proj=proj, lat_0=lat_0, lon_0=lon_0, x_0=x_0, y_0=y_0, ellps=ellps,
            units=units)
        # proj_str = "+proj={proj:} " \
        #            "+lat_1={lat_1:} " \
        #            "+lat_2={lat_2:} " \
        #            "+lat_0={lat_0:} " \
        #            "+lon_0={lon_0:} " \
        #            "+x_0={x_0:} " \
        #            "+y_0={y_0:} " \
        #            "+ellps={ellps:} " \
        #            "+towgs84={towgs84:} " \
        #            "+units={units:} " \
        #            "+no_defs".format(
        #     proj=proj,lat_1=lat_1,lat_2=lat_2,lat_0=lat_0,lon_0=lon_0,x_0=x_0,y_0=y_0,ellps=ellps,towgs84=towgs84,units=units)
        # proj_str = "+proj=lcc +lat_1=51.16666723333333 +lat_2=49.8333339 +lat_0=90 +lon_0=4.367486666666666 +x_0=150000.013 +y_0=5400088.438 +ellps=intl +towgs84=106.869,-52.2978,103.724,-0.33657,0.456955,-1.84218,1 +units=m +no_defs"
        return proj_str


fcrs = FantasyCRS(10,10)
print("Custom CRS: {}".format(fcrs))

random_points = dict()
a_polygon = Polygon(([1000,5000],[-50000000,-50000000],[30000000,-30000000],[5000000000,5000000000]))
random_points['geometry'] = a_polygon
random_points['title'] = "a_point"
gdf = gpd.GeoDataFrame(geometry=[a_polygon],crs=fcrs)
gdf.set_crs(fcrs,allow_override=True,inplace=True)
# gdf = gdf.append(random_points,ignore_index=True)
print("gdf {}".format(gdf))
print("gdf crs {}".format(gdf.crs))

mercator_gdf = gpd.GeoDataFrame(columns=['geometry','title'],crs="epsg:3857")
mercator_gdf = mercator_gdf.append(random_points,ignore_index=True)


print("gdf crs get_geod {}".format(gdf.crs.get_geod()))
print("gdf crs source_crs {}".format(gdf.crs.source_crs))
print("gdf crs axis info {}".format(gdf.crs.axis_info))
print("gdf crs coordinate system {}".format(gdf.crs.coordinate_system))
print("gdf crs prime meridian {}".format(gdf.crs.prime_meridian))
print("gdf crs name {}".format(gdf.crs.name))
print("gdf crs type name {}".format(gdf.crs.type_name))
print("gdf boundary {}".format(gdf.boundary))

gdf.plot()
plt.savefig('pyplot')
plt.show()

print("gdf crs {}".format(gdf.crs))
round_crs = gdf.to_crs("EPSG:3395")
round_crs.plot()
print(round_crs)
for pt in round_crs.loc[0]['geometry'].exterior.coords.xy:
    print("pt {}".format(pt))
plt.savefig('pyplot')
plt.show()