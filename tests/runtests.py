import unittest
import argparse
import os


def load_tests(test_type: str = "all"):
    loader = unittest.TestLoader()

    suite = unittest.TestSuite()

    start_dir = os.path.dirname(__file__)

    if test_type in ("u", "unit"):
        suite.addTests(loader.discover(start_dir=start_dir, pattern="test_*_unit.py"))
    elif test_type in ("i", "integration"):
        suite.addTests(loader.discover(start_dir=start_dir, pattern="test_*_integration.py"))
    else:
        suite.addTests(loader.discover(start_dir=start_dir, pattern="test_*.py"))

    return suite

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run unittest tests")
    parser.add_argument(
        "--type", "-t",
        help="Specify which tests to run: unit, integration, or leave empty for all",
        choices=["unit", "u", "integration", "i"],
        default=None
    )
    args = parser.parse_args()

    # just in case we need to run unit/integration tests separately
    test_type = args.type

    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = load_tests(test_type)
    result = runner.run(test_suite)
    exit(not result.wasSuccessful())