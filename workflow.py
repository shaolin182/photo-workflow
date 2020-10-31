import click
from photo_workflow.rename import rename
#from import_images import process
from photo_workflow.sync import sync
from photo_workflow.exif import tag_process

@click.group()
def cli():
    """ Main group command"""
    pass


@cli.command("import")
@click.argument('source', type=click.Path(exists=True))
@click.argument('collection')
@click.option('--type', type=click.Choice(['RAW', 'JPG']), default="JPG", 
    help="Type of imported files")
@click.option('-r', '--recursive', is_flag=True, default=False)
@click.option('-f', '--filter', help='Regex used for matching files')
@click.option('-v', '--verbose', help='Display more details')
def import_images(source, collection, type, recursive, filter, verbose):
    """ 
    Copy images from SOURCE to destination repository into COLLECTION folder

    Also, import images into darktable and digikam tools
    """
    click.echo('Import images')


@cli.command("rename")
@click.argument('source', type=click.Path(exists=True))
@click.option('-s', '--suffix', help='Suffix applied to all images')
@click.option('-r', '--recursive', is_flag=True, default=False)
@click.option('-f', '--filter', help='Regex used for matching files')
@click.option('-v', '--verbose', is_flag=True, help='Display more details')
def rename_cli(source, suffix, recursive, filter, verbose):
    """ 
    Rename all images containing in 'SOURCE' directory
    
    Renaming process uses EXIF data of images and in particular, timestamp for
    renaming an image with the following format

    If no EXIF data are found, then prompt user for new filename
    """
    rename(source, suffix, recursive, filter, verbose)

@cli.command()
@click.argument('source', type=click.Path(exists=True))
@click.argument('tag')
@click.option('-d', '--delimiter', help='Delimiter for hierarchical tag', 
    default="|")
@click.option('--rm', help='If specified, remove tags from images')
@click.option('-v', '--verbose', is_flag=True, help='Display more details')
def tag(source, tag, delimiter, rm, verbose):
    """
    Catalog each images from SOURCE directory by applying custom TAG

    \b
    A tag can reference a simple string or a hierarchical structure
    Ex : 
    - Simple tag : "Vacances"
    - Hierarchical tag : "Vacances|2019|France|Rochelle"

    Those tags are persisted in EXIF data in order to be reused by some other 
    tools
    """
    tag_process(source, "Xmp.dc.Subject", tag, delimiter, rm, verbose)
    tag_process(source, "Xmp.lr.hierarchicalSubject", tag, delimiter, rm, verbose)
    click.echo('Tag an image')


@cli.command("sync")
@click.argument('collection')
@click.option('--source', type=click.Choice(['RAW', 'JPG']), default="JPG", 
    help="Source of sync files")
@click.option('-f', '--filter', help='Regex used for matching files')
@click.option('-v', '--verbose', help='Display more details')
def sync_cli(collection, source, filter, verbose):
    """ 
    Synchronize RAW and JPG directory
    
    Remove RAW file if no matching JPG file exists
    Remove JPG file if no matching RAW file exists
    """
    sync(collection, source, filter, verbose)
    

if __name__ == '__main__':
    cli()