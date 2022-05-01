import abc


class FileManager(abc.ABC):

    @abc.abstractmethod
    def write(self):
        pass


class TxtFileManager(FileManager):
    def __init__(self, objects, *, method='txt'):
        self.objects = objects
        self.method = method

    def write(self):
        with open('txt.txt','w') as file:
            file.write(self.objects)
