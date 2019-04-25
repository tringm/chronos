import argparse
import importlib
import sys
import unittest

from test.tests import get_suites, TestResultCompareFileMeld

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Chronos')
    test_group = parser.add_argument_group('Test', 'Test arguments')
    suites = get_suites()
    test_group.add_argument('--test',
                            help=f"Test {'|'.join(list(suites.keys()) + ['all'])} or a specific test cases",
                            type=str,
                            required=True)
    test_group.add_argument('--verbosity',
                            help=f"Test verbosity (1 or 2)",
                            type=int,
                            required=False,
                            default=2)
    test_group.add_argument('--meld',
                            help='Use meld to compare out and exp file. Default False',
                            action='store_true')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        exit()

    if args.meld:
        result_class = TestResultCompareFileMeld
    else:
        result_class = unittest.TextTestResult

    runner = unittest.TextTestRunner(verbosity=args.verbosity, resultclass=result_class)

    result = False
    if args.test:
        if args.test == 'all':
            results = set()
            for s in suites:
                results.add(runner.run(suites[s]).wasSuccessful())
            result = all(results)
        else:
            if args.test in list(suites.keys()):
                result = runner.run(suites[args.test]).wasSuccessful()
            else:
                try:
                    test_path = args.test.split('.')
                    module = importlib.import_module('.'.join(test_path[:-1]))
                    test_case_class = getattr(module, test_path[-1])
                    suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_case_class)
                    result = runner.run(suite).wasSuccessful()
                except ValueError:
                    print(f"Suite or test case {args.test} not found")
        if not result:
            sys.exit("Some tests failed")
