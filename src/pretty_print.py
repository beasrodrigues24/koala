class PrettyPrint:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def template_error(msg, filepath, line):
        print(f'{PrettyPrint.FAIL}Error{PrettyPrint.ENDC}: {filepath}:{line}: {msg}')

    def error(msg):
        print(f'{PrettyPrint.FAIL}Error{PrettyPrint.ENDC}: {msg}')

    def template_warn(msg, filepath, line):
        print(f'{PrettyPrint.WARNING}Warning{PrettyPrint.ENDC}: {filepath}:{line}: {msg}')
