import logging
from logging.handlers import RotatingFileHandler
import functools
from time import perf_counter, sleep
from itertools import count


class LogDecorator(object):
    _ids = count(0)

    def __init__(self, speed_test: bool = False):
        super().__init__()
        self.id = next(self._ids)
        self.logger = logging.getLogger(__name__)
        self.speed_test = speed_test
        formatter = "[%(asctime)s - %(name)s - %(levelname)s] %(message)s"
        logging.basicConfig(level=logging.DEBUG,
                            format=formatter,
                            handlers=[logging.StreamHandler()])
        # create a file handler
        handler_file = RotatingFileHandler(
            "QTorrent_Search.log", maxBytes=500000, backupCount=1)
        handler_file.setLevel(logging.DEBUG)

        # create a logging format
        formatter = logging.Formatter(
            '[%(asctime)s - %(name)s - %(levelname)s] %(message)s')
        handler_file.setFormatter(formatter)

        # add the file handler to the logger
        # IDK why self.logger.hasHandler() is True even when i don't have one.
        # self.logger.handlers = [] and hasHandler() is True..
        if not self.logger.handlers:
            print(f"Handler !  {self._ids}")
            self.logger.addHandler(handler_file)
        else:
            print(f"No handler atm {self._ids}")

    def __call__(self,  fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            try:
                args_repr = [repr(a) for a in args]
                kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
                signature = ", ".join(args_repr + kwargs_repr)
                self.logger.debug(
                    f"Function {fn.__name__}() called with args {signature}")
                if self.speed_test:
                    start_time = perf_counter()
                result = fn(*args, **kwargs)
                # return result
            except Exception as ex:
                if self.speed_test:
                    stop_time = perf_counter()
                self.logger.warning("Exception {0}".format(ex))
                raise ex
            if self.speed_test:
                stop_time = perf_counter()
                result_time = stop_time - start_time
            # FIXME: Do stuff when it's makeRequest cause result spam the log
            if isinstance(result, tuple):
                print("Do stuff")
            else:
                print("other stuff")
                self.logger.info(
                    f"Function {fn.__name__}() took {result_time:.2f}s")
            # self.logger.info(f"Function {fn.__name__}() return with :  {result}")
            self.logger.info(f"Function {fn.__name__}() return with :")
            self.logger.info(result)
            return result
        return decorated

# @LogDecorator(speed_test=False)
# logger = LogDecorator


# @logger(speed_test=False)
if __name__ == "__main__":
    @LogDecorator(speed_test=False)
    def sum(a, b, c=5):
        return a + b + c

    # @logger(speed_test=True)
    @LogDecorator(speed_test=True)
    def exp(a: int, b: int):
        sleep(2.5)
        x = a**b
        # print(f"{x} = {a}**{b}")
        return x

    # @logger(speed_test=True)
    @LogDecorator()
    def crash(a, b):
        raise ValueError(str(a))

    sum(1, b=3)

    exp(100, 100)

    try:
        crash(1, 3)
    except:
        pass
