class CodeWriter:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'w')

    def write(self, code):
        self.file.write(code + '\n')

    def close(self):
        self.file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()