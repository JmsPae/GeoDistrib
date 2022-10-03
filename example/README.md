# Example
This example contains open data from Statistics Sweden (Statistiska Centralbyrån) and Gävle municipality. The data sources are in Swedish, so I've included a description of the files and their attributes.

The goal of this example is to distribute the field **BefTotalt** (total population) from **Population_1km_211231_3006** to the building polygons in **residential_buildings** weighted by the **AREA** attribute.

Navigate to this folder in your command line and enter the following command:

`python3 -m geodistrib -src Population_1km_211231_3006.gpkg -dst residential_buildings.gpkg -srcAttrib Beftotalt -dstWeight AREA -output out.gpkg`

# Files

## **basemap_buildings.gpkg**
Extract from Gävle Municipality's basemap reprojected from the local reference system (SWEREF99 1630) to the national SWEREF 99 TM (Transverse Mercator) containing building polygons.

### Attributes
* fid - Unique feature Id
* TYP - Building type. Industri = Industry, Bostadshus = Residential, Byggnad med verksamhet = Commercial, etc.
* UPDDATUM - Last updated. (?)
* FILDATUM - Last updated, entire database. (?)
* METOD - Polygon generation method. Typically digitalised (Digitaliserad) or geodetically surveyed (Geodetiskt inmätt) though some are unknown (Okänd).

## **residential_buildings.gpkg**
basemap_buildings filtered down to residential building type.

### Attributes
Same as basemap_buildings, with the addition of AREA which corresponds to building area.

## **Population_1km_211231_3006.gpkg**
Section of Statistics Sweden's 1x1km population statistics covering the study area from the end of 2021.

### Attributes
* fid - Unique feature Id.
* Rutstorl - Cell size in meters.
* Ruta - Statistics Sweden's own Cell ID.
* Man - Male population.
* Kvinna - Female population.
* BefTotalt - Total population.

# Data sources
* basemap_buildings - processed version of [baskarta_byggnader](https://www.gavle.se/kommunens-service/kommun-och-politik/statistik-fakta-och-oppna-data/oppna-data/datakatalog/data/#esc_entry=20&esc_context=1).

* Population_1km_211231_3006 - processed version of [Befolkning efter kön](https://www.scb.se/vara-tjanster/oppna-data/oppna-geodata/statistik-pa-rutor/).