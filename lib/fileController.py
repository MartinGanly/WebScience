from filelock import FileLock

# This manages writing to files for both processing of statistics
# and writing USER or TWEET ID's to file for processing with the REST API
class fileController():

    def get_and_remove_first_line(self, filename):
        lines = self.get_file_contents(filename)
        self.remove_first_line(filename, lines)
        if(len(lines) > 0):
            return lines[0].strip()
        return False

    def get_file_contents(self, filename):
        lock = FileLock(filename + ".lock")
        with lock:
            f = open(filename, 'r')
            lines = f.readlines()
            f.close()
        return lines

    def remove_first_line(self, filename, lines):
        lock = FileLock(filename + ".lock")
        with lock:
            f = open(filename, 'w+')
            f.write( ''.join( lines[1:] ) )
            f.close()

    def append_one_line(self, filename, data):
        lock = FileLock(filename + ".lock")
        with lock:
            f = open(filename, 'a')
            final = str(data) + '\n'
            f.write(final)
            f.close()

    def append_one_line_to_start(self, filename, data):
        lock = FileLock(filename + ".lock")
        lines = self.get_file_contents(filename)
        lines.insert(0, (data + "\n"))
        with lock:
            f = open(filename, 'w+')
            f.write(''.join(lines))
            f.close()

    def write_data_to_file(self, filename, data):
        f = open(filename, 'w+')
        f.write("".join(str(data)))
        f.close()

    def get_length_of_file(self, filename):
        with open(filename) as f:
            line_count = 0
            for line in f:
                line_count += 1
        return line_count
