"""
RobotXT Parser - A Python library for parsing and analyzing robots.txt files.
"""

from .parser.robot_parser import RobotParser
from .parser.exceptions import RobotException

__version__ = "1.0.0"
__all__ = ["RobotParser", "RobotException"] 