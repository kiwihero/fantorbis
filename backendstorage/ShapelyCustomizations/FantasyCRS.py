from pyproj.crs import CRS
import geopandas as gpd

from backendstorage.ShapelyCustomizations._FantasyCRS import _FantasyCRS

from shapely.geometry import Point,Polygon
import matplotlib.pyplot as plt
from shapely.affinity import affine_transform
import copy

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
a_polygon = Polygon(([1,1,1],[10,1,1],[10,10,-10],[1,10,-10]))#,([4,4,4],[6,4,4],[6,6,-6],[4,6,-6]))
# a_polygon = Polygon(([10,5],[5,-5],[-10,-5],[-5,5]))
random_points['geometry'] = a_polygon
random_points['title'] = "a_point"
gdf = gpd.GeoDataFrame(geometry=[a_polygon],crs=fcrs)
# gdf.set_crs(fcrs,allow_override=True,inplace=True)
gdf.set_crs(fcrs)
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

gdf_translate = copy.deepcopy(gdf)
print("gdf",gdf.loc[0])
gdf_translate.loc[0] = affine_transform(gdf_translate.loc[0]['geometry'], matrix=[1,0,0,0,1,0,0,0,1,0,9,0])
print("gdf",gdf.loc[0])
print("gdf translate",gdf_translate.loc[0])
gdf_translate.plot()
plt.savefig('pyplot')
plt.show()
fig, ax = plt.subplots()
gdf.plot(ax=ax,color='magenta')
gdf_translate.plot(ax=ax,color='gray')
ax.set_ylabel('X: (0,x,0)')
plt.show()
for pt in gdf.loc[0]['geometry'].exterior.coords:
    print("gdf round pt {}".format(pt))
for pt in gdf_translate.loc[0]['geometry'].exterior.coords:
    print("gdf trans round pt {}".format(pt))

print("gdf crs {}".format(gdf.crs))
round_crs = gdf.to_crs("EPSG:3395")
round_crs.plot()
print(round_crs)
for pt in round_crs.loc[0]['geometry'].exterior.coords:
    print("round pt {}".format(pt))
plt.savefig('pyplot')
plt.show()
fig, ax = plt.subplots()
shifted_round = copy.deepcopy(round_crs)
shifted_round.loc[0] = affine_transform(shifted_round.loc[0]['geometry'], matrix=(1,0,0,0,1,0,0,0,1,0,9000000,0))
shifted_round.plot(ax=ax,color='purple')
for pt in shifted_round.loc[0]['geometry'].exterior.coords:
    print("shifted pt {}".format(pt))
round_crs_trans = gdf_translate.to_crs("EPSG:3395")
for pt in round_crs_trans.loc[0]['geometry'].exterior.coords:
    print("trans round pt {}".format(pt))
round_crs.plot(ax=ax,color='red')
round_crs_trans.plot(ax=ax,color='green')
ax.set_ylabel('Y: (0,y,0)')
ax.set_xlabel('X: (x,0,0)')
print(round_crs)
plt.savefig('pyplot')
plt.show()