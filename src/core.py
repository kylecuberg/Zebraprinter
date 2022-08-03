# Standard library
import logging

logging.basicConfig(
    filename="reports/all.log",
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO,
)  # put this only in main core.py file

logger = logging.getLogger(__name__)  # put this in each file


def main():
    # Main function

    try:
        True
    except Exception as E:
        print(type(E).__name__, __file__, E.__traceback__.tb_lineno, "\n", E)
        logger.warning(type(E).__name__, __file__, E.__traceback__.tb_lineno, "\n", E)
        raise


if __name__ == "__main__":
    """[summary]"""
    main()
