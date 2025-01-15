from loguru import logger
import sys

# Global debug flag
global DEBUG_MODE
DEBUG_MODE = False

def setup_logger():
    # Remove default handler
    logger.remove()
    
    if DEBUG_MODE:
        # Debug mode: console shows DEBUG and above
        logger.add(
            sys.stderr,
            level="DEBUG",
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | "
            "<blue>{message}</blue>",
            colorize=True
        )
        logger.debug("Debug logging enabled")
    else:
        # Normal mode: console shows INFO and above
        logger.add(
            sys.stderr,
            level="INFO",
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | "
            "<white>{message}</white>",
            colorize=True
        )
        logger.info("Debug logging disabled")

def example_logs():
	logger.debug("Debug message - only visible in debug mode")
	logger.info("Info message - always visible")
	logger.warning("Warning message - always visible")
	logger.error("Error message - always visible")

if __name__ == "__main__":
	# Test with debug off
	setup_logger()
	example_logs()
	
	# Test with debug on
	DEBUG_MODE = True
	setup_logger()
	example_logs()