import nbformat
import nbconvert
import logging
import sys
import time
# import wget

logger = logging.getLogger(__name__)

ep = nbconvert.preprocessors.ExecutePreprocessor(timeout=5000)
exporter = nbconvert.exporters.get_exporter('slides')()

# SLIDES_FILENAME_OUT = 'Report_slides.html'
SLIDES_FILENAME_OUT = '/data/outputs/Report_slides.html'
BASE_PATH = '/notebook'

def execute(country_filter=['US', 'Italy', 'China', 'Spain', 'Germany'], notebook_filename='notebook_stats.ipynb'):
    start = time.time()
#     notebook_url = 'https://raw.githubusercontent.com/santteegt/c2d-demos/master/notebook_stats.ipynb'
    notebook_filename = f'{BASE_PATH}/{notebook_filename}'
#     wget.download(notebook_url, out=notebook_filename)
    logger.warning(f'Notebook path: {notebook_filename}')
    with open(notebook_filename, 'r') as f:
        nb = nbformat.read(f, as_version=nbformat.NO_CONVERT)
        filter_cell = nb['cells'][2]
        logger.warning(f"Cell#2: {filter_cell['source']} / {country_filter}")
        filter_cell['source'] = f"countries = {country_filter}"
        data_path_cell = nb['cells'][3]
        logger.warning(f"Cell#3: {data_path_cell['source']} / '/data/inputs'")
        data_path_cell['source'] = f"BASE_PATH = '/data/inputs'"
    try:
        out = ep.preprocess(nb, {})
        logger.warning(f'Total time processing data: {time.time() - start} seconds')
    except nbconvert.preprocessors.CellExecutionError as e:
        logger.warning(f'Process failed: {e}')
        raise

    logger.warning('Storing results')
    (out_slides, resources) = nbconvert.exporters.export(exporter, nb)
    with open(SLIDES_FILENAME_OUT, 'w') as f:
        f.write(out_slides)
        f.close()
        logger.warning(f'Report generated at: {SLIDES_FILENAME_OUT}')

            
if __name__ == '__main__':
    print('Initializing with params:')
    print(sys.argv)
    execute()
#     if len(sys.argv) > 1:
#         execute(sys.argv[1].split(','))
#     else:
#         execute()