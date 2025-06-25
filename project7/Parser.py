class Parser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = []

    def parse(self):
        with open(self.file_path, 'r') as file:
            for line in file:
                if line.strip():  # Ignore empty lines
                    self.data.append(line.strip())
        return self.data

    def get_data(self):
        return self.data