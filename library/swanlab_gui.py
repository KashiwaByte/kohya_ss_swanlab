import os
import gradio as gr
from easygui import msgbox
import subprocess
import time
import webbrowser
from library.custom_logging import setup_logging
import swanlab



swanlab_proc = None
SWANLAB = 'swanlab watch' 

# Set the default SWANLAB port
DEFAULT_SWANLAB_PORT = 5092

def start_swanlab(headless, logging_dir, wait_time=5):
    global swanlab_proc
    
    headless_bool = True if headless.get('label') == 'True' else False

    # Read the SWANLAB_PORT from the environment, or use the default
    swanlab_port = os.environ.get('SWANLAB_PORT', DEFAULT_SWANLAB_PORT)

    if not os.listdir(logging_dir):
        swanlab.info('Error: log folder is empty')
        msgbox(msg='Error: log folder is empty')
        return
    

    
    run_cmd = [
        SWANLAB,
        '-l',
        logging_dir
        '--port',
        str(swanlab_port),
    ]

    swanlab.info(run_cmd)
    if swanlab_proc is not None:
        log.info(
            'Tensorboard is already running. Terminating existing process before starting new one...'
        )
        stop_swanlab()

    # Start background process
    swanlab.info('Starting Swanlab on port {}'.format(swanlab_port))
    try:
        swanlab_proc = subprocess.Popen(run_cmd)
    except Exception as e:
        swanlab.error('Failed to start Swanlab:', e)
        return

    if not headless_bool:
        # Wait for some time to allow Swanlab to start up
        time.sleep(wait_time)

        # Open the Swanlab URL in the default browser
        swanlab_url = f'http://localhost:{swanlab_port}'
        swanlab.info(f'Opening Swanlab URL in browser: {swanlab_url}')
        webbrowser.open(swanlab_url)


def stop_swanlab():
    global swanlab_proc
    if swanlab_proc is not None:
        swanlab.info('Stopping swanlab process...')
        try:
            swanlab.terminate()
            swanlab_proc = None
            swanlab.info('...process stopped')
        except Exception as e:
            swanlab.error('Failed to stop Swanlab:', e)
    else:
        swanlab.info('Swanlab is not running...')


def gradio_swanlab():
    with gr.Row():
        button_start_swanlab = gr.Button('Start swanlab')
        button_stop_swanlab = gr.Button('Stop swanlab')

    return (button_start_swanlab, button_stop_swanlab)
