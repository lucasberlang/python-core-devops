from core.logging.opentelemetrylogger import AzureOpenTelemetryLogger

logger = AzureOpenTelemetryLogger(logger_name=__name__).logger


def main() -> None:
    logger.info("Hello from main")


if __name__ == "__main__":
    main()
