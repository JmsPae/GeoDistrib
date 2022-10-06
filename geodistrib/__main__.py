from nis import cat
import fiona
import typer
from geodistrib import distribute, interpretPipeline

app = typer.Typer()


@app.command()
def distribute(sourceDir: str = typer.Option(..., "-src", help="Source geodata file"),
               destDir: str = typer.Option(..., "-dst", help="Destination geodata file"), 
               attribute: str = typer.Option(..., "-srcAttrib", help="Source dataset attribute to be distributed among contained destination features"),
               weight: str = typer.Option(..., "-dstWeight", help="Destination dataset weights for source attribute distribution"), 
               outputDir: str = typer.Option(..., "-output", help="Output file")):
    src = fiona.open(sourceDir)
    dst = fiona.open(destDir)

    if (src.meta['crs'] != dst.meta['crs']):
        print("src and dst CRS don't match!")
        raise typer.Exit()

    distribute(src, dst, attribute, weight, outputDir)

    src.close()
    dst.close()

@app.command()
def pipeline(pipelineDir: str = typer.Option(..., "-i", help="Pipeline JSON file")):
    interpretPipeline(pipelineDir)
    
app()