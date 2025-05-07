from Logger.LogLevel import LogLevel
from Logger.Logger import Logger
from OutputHandler.FileOutputHandler import FileOPHandler
from OutputHandler.ConsoleOutputHandler import ConsoleOPHandler

if __name__ == '__main__':
    logger = Logger(ConsoleOPHandler(), LogLevel.DEBUG)
    logger.debug("Debug Message1")
    logger.info("Info Message1")
    logger.warn("Warn Message1")
    logger.error("Error Message1")

    print("------------------------------------")

    logger.set_log_level(LogLevel.WARN)
    logger.debug("Debug Message2")
    logger.info("Info Message2")
    logger.warn("Warn Message2")
    logger.error("Error Message2")

    print("------------------------------------")
    logger = Logger(ConsoleOPHandler(), LogLevel.INFO)
    logger = Logger(ConsoleOPHandler(), LogLevel.WARN)

    print("------------------------------------")

    logger.set_output_handler(FileOPHandler("log.txt"))
    logger.set_log_level(LogLevel.DEBUG)
    logger.debug("Debug Message3")
    logger.info("Info Message3")
    logger.warn("Warn Message3")
    logger.error("Error Message3")

    logger.set_log_level(LogLevel.WARN)
    logger.debug("Debug Message4")
    logger.info("Info Message4")
    logger.warn("Warn Message4")
    logger.error("Error Message4")

