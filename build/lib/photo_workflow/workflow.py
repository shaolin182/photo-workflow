import click
from photo_workflow.sync import sync
from photo_workflow.utils.logging_photo import logger
from photo_workflow.workflow_process import TagProcess, RenameProcess, InitCollection, SyncProcess

@click.group()
def cli():
    """
    v1.0.0-beta1
    """
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
@click.option('-c', '--collection', help='Collection to work on, if empty runs on all collections')
@click.option('-f', '--force', help='Force renaming files', is_flag=True, default=False)
def rename_cli(collection, force):
    """
    Rename images from a collection

    Renaming process uses EXIF data of images for building a new filename
    """
    logger.info("CLI Command - Rename collection : %s, force flag : %s", collection, force)
    RenameProcess().run(collection, force)

@cli.command()
@click.option('-c', '--collection', help='Collection to work on, if empty runs on all collections')
@click.option('-f', '--force', help='Force tagging files', is_flag=True, default=False)
def tag(collection, force):
    """
    Catalog each image collection by applying tags from metadata

    Those tags are persisted in EXIF data in order to be reused by some other
    tools
    """
    logger.info("CLI Command - Tag collection : %s, force flag : %s", collection, force)
    TagProcess().run(collection, force)


@cli.command("init")
@click.option('-c', '--collection', help='Collection to init, if empty runs on all collections')
@click.option('-f', '--force', help='Force creating collections', is_flag=True, default=False)
def init_collection(collection, force):
    """
    Create metadata file for collection
    """
    logger.info("CLI Command - Init collection : %s, force flag : %s", collection, force)
    InitCollection(collection, force).process()


@cli.command("sync")
@click.option('-c', '--collection', help='Collection to work on, if empty runs on all collections')
@click.option('-f', '--force', help='Force renaming files', is_flag=True, default=False)
def sync_cli(collection, force):
    """
    Synchronize RAW and JPG directory

    Remove RAW file if no matching JPG file exists
    Remove JPG file if no matching RAW file exists
    """
    SyncProcess().run(collection, force)


if __name__ == '__main__':
    cli()
