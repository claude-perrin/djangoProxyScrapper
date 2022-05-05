import abc


class FileManager(abc.ABC):

    @abc.abstractmethod
    def write(self):
        pass


class TxtFileManager(FileManager):
    def __init__(self, objects):
        self.objects = objects

    def write(self):
        with open('txt.txt', 'w') as file:
            file.write(self.objects)


class CsvFileManager(FileManager):
    def __init__(self, objects):
        self.objects = objects

    def write(self):
        with open('txt.txt', 'w') as file:
            [file.write(i) for i in self.objects]

