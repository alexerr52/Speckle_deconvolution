from astropy.utils.iers import conf
conf.auto_max_age = None

from astroplan import Observer
from astropy.io import fits
import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord
from astropy.time import Time
from astropy.coordinates import ICRS
import numpy as np

data1 = fits.open("SP20230714185459.fits") #кадр со звездой

ra = data1[0].header['RAAPP']
dec = data1[0].header['DECAPP']
date = data1[0].header['DATE']

print(date)

coord_eq = SkyCoord(frame=ICRS, ra=float(ra), dec=float(dec), obstime=date, unit="deg")

longitude = data1[1].header['LONGITUD']
latitude = data1[1].header['LATITUDE']
loc = EarthLocation.from_geodetic(longitude,latitude)

utcoffset = 3*u.hour
time = Time(date)
#time = Time(date) + utcoffset

print(time)

coord_altaz = coord_eq.transform_to(AltAz(obstime=date, location=loc))
print(f"Altitude = {coord_altaz.alt:.2}")
print(f"Azimuth = {coord_altaz.az:.2}")

KGO = Observer(location=loc, name="KGO")

parall = KGO.parallactic_angle(time, coord_eq)

print(parall*(180/np.pi))
