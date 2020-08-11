import socket
import json

from margot.config import settings
from margot.signals import BackTest
from margot import BaseAlgo

import importlib, inspect

def ipc_request(msg, logger):
    # requst the manager for something
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(settings.sys.get('socket'))
        sock.sendall(msg.encode())  
        logger.debug('Message sent')
        data = sock.recv(4096)
        sock.close()
        reply = data.decode()
        logger.debug('Received {}'.format(reply))
        return json.loads(reply)

    except FileNotFoundError:
        logger.error('Unable to connect to server. Is it running?')
        raise OSError('Unable to connect to {}'.format(settings.sys.get('socket')))

def init(algo_name, settings, logger):
    algo = ipc_request('GETALGO {} \n'.format(algo_name), logger)

    logger.info('Backtesting {}'.format(algo.get('algorithm').get('name')))

    for name, cls in inspect.getmembers(
            importlib.import_module(algo.get('python').get('file')), 
            inspect.isclass):

        if issubclass(cls, BaseAlgo) and cls != BaseAlgo:
            logger.debug('Found algo {}'.format(cls))
            algo = cls()
            bt = BackTest(algo=algo)
            rets = bt.run(periods=30)

    # need to store the backtests for each algo so that we have volatility etc.
    