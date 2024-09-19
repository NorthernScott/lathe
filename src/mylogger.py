# -*- coding: utf-8 -*-

# import core modules
import logging
from logging import Logger

# import external dependencies
from rich.console import Console

# Setup console and logging.

err_con = Console(stderr=True)
std_con = Console(stderr=False)

log: Logger = logging.getLogger(name="rich")
