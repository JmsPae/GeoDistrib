import fiona
import typer
from shapely.geometry import shape, Point
from geodistrib import distribute

def main(sourceDir: str = typer.Option(..., "-src"),
         destDir: str = typer.Option(..., "-dst"), 
         attribute: str = typer.Option(..., "-srcAttrib"),
         weight: str = typer.Option(..., "-dstWeight"), 
         outputDir: str = typer.Option(..., "-output")):
    src = fiona.open(sourceDir)
    dst = fiona.open(destDir)

    distribute(src, dst, attribute, weight, outputDir)

    src.close()
    dst.close()
    
typer.run(main)