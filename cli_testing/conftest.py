""" File use for get command line arguments """
option = None


def pytest_addoption(parser):
    '''
    Method use for pytest_addoption
    parser: parse the command line argument
    '''
    parser.addoption("--excelname", action="store", default="", help="TestCase Groups")


def pytest_configure(config):
    '''
    Make cmdline arguments available to framework
    config: configure command line argument
    '''
    # pylint: disable=global-statement
    global option
    option = config.option