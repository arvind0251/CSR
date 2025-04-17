import sys
import traceback

def setup_global_exception_logger():
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        print("=== UNCAUGHT EXCEPTION ===")
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print("==========================")

    sys.excepthook = handle_exception
