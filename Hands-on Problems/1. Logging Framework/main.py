import time

from Logger.LogLevel import LogLevel
from Logger.Logger import Logger
from Logger.LoggerWithQueue import LoggerQueueBased
from OutputHandler.FileOutputHandler import FileOPHandler
from OutputHandler.ConsoleOutputHandler import ConsoleOPHandler

def test_console_output_with_updates():
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

def test_file_output():
    # Below should not initialise logger again.
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

def test_log_rotate():
    logger = Logger(ConsoleOPHandler(), LogLevel.WARN)
    logger.set_output_handler(FileOPHandler("log.txt", rotation_check_interval=2))
    counter = 0
    while True:
        counter += 1
        logger.debug("Debug Message{}".format(counter))
        logger.info("Info Message{}".format(counter))
        logger.warn("Warn Message{}".format(counter))
        logger.error("Error Message{}".format(counter))

def test_log_with_queue():
    counter = 999
    logger = LoggerQueueBased(FileOPHandler("log_with_queue.txt", rotation_check_interval=2))
    logger.debug("Debug Message{}".format(counter))
    logger.info("Info Message{}".format(counter))
    logger.warn("Warn Message{}".format(counter))
    logger.error("Error Message{}".format(counter))

    time.sleep(2)
    logger.shutdown()

def test_log_with_queue_100times():
    counter = 1000
    logger = LoggerQueueBased(ConsoleOPHandler())
    while counter < 1100:
        logger.debug("Debug Message{}".format(counter))
        logger.info("Info Message{}".format(counter))
        logger.warn("Warn Message{}".format(counter))
        logger.error("Error Message{}".format(counter))
        counter += 1

    print("Queue Size before sleep: {}".format(logger._queue.qsize()))

    time.sleep(1)

    print("Queue Size after sleep: {}".format(logger._queue.qsize()))

    logger.shutdown()

    print("Queue Size after shutdown: {}".format(logger._queue.qsize()))

if __name__ == '__main__':
    # Test 1
    test_console_output_with_updates()

    # Test 2
    test_file_output()

    # Test 3
    test_log_rotate()

    # Test 4
    test_log_with_queue()

    # Test 5
    test_log_with_queue_100times()