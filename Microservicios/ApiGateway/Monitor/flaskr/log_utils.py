import datetime


class LogUtils:
    file_name = None
    @staticmethod
    def start(self):
        LogUtils.file_name = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S') + 'log.txt'
        with open(self.file_name, 'w') as f:
            f.write('Inicio Log\n')

    @staticmethod
    def write_message(self, message):
        with open(LogUtils.file_name, 'a') as f:
            f.write(
                '[' + datetime.datetime.utcnow().strftime('%H:%M:%S') + ']: ' + message + '\n'
            )
