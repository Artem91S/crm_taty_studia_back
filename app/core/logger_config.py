from loguru import logger
import sys

logger.remove()

SCREEN_FORMAT = (
    "<cyan>>>></cyan> {time:YYYY-MM-DD HH:mm:ss} | "
    "<level><bold>{level}</bold></level> | "
    "<cyan>Path</cyan>: {name} -> <cyan>Func</cyan>: {function} -> <cyan>Line</cyan>: {line} | "
    "<level>{message}</level>\n"
)

logger.add(sink=sys.stdout, format=SCREEN_FORMAT, colorize=True)
