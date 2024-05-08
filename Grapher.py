import subprocess
from abc import abstractmethod
from typing import Iterable, Optional, Protocol


class Writable(Protocol):
    @abstractmethod
    def write(self, s: str, /) -> int:
        ...
    
    @abstractmethod
    def writelines(self, lines: Iterable[str], /) -> None:
        ...

class Dot(Writable):
    def __init__(self, outfile: str, format: str, write_to_file: bool = False):
        '''
        outfile is just the file name without the extension. The extension is added in the `format` argument.
        '''
        self.format = format
        self.outfile = outfile
        self.write_to_file = write_to_file
        self._pipe: Optional[subprocess.Popen[bytes]] = None
    
    def __enter__(self):
        self._pipe = subprocess.Popen(['dot', f'-T{self.format}', '-o', f'{self.outfile}.{self.format}'], stdin=subprocess.PIPE)
        if self.write_to_file:
            self.file = open(f'{self.outfile}.dot', 'wb')
        return self
    
    def __exit__(self, *_):
        if self._pipe is None:
            raise Exception('Did not call __enter__() (`with` statement) to initialize file.')
        
        if self._pipe.stdin is None:
            raise Exception('stdin shouldn\'t ever be None')

        if self.write_to_file:
            self.file.close()
        self._pipe.stdin.close()
    
    def write(self, s: str, /) -> int:
        if self._pipe is None:
            raise Exception('Did not call __enter__() (`with` statement) to initialize file.')
        
        if self._pipe.stdin is None:
            raise Exception('stdin shouldn\'t ever be None')
        
        if self.write_to_file:
            self.file.write(s.encode())
        return self._pipe.stdin.write(s.encode())
    
    def writelines(self, lines: Iterable[str], /) -> None:
        if self._pipe is None:
            raise Exception('Did not call __enter__() (`with` statement) to initialize file.')
        
        if self._pipe.stdin is None:
            raise Exception('stdin shouldn\'t ever be None')
        
        if self.write_to_file:
            self.file.writelines(map(lambda x: x.encode(), lines))
        self._pipe.stdin.writelines(map(lambda x: x.encode(), lines))


if __name__ == '__main__':
    d = Dot('test', 'png')
    with d:
        d.write('digraph { a -> b }')