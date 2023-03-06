
# array of  bytes that can accessed using valid address
# data is name of array, base address is starting address of memory device

class RAM:
    def __init__(self, baseAddr, sizeInK):
        self.baseAddr = baseAddr
        self.data = [0]*sizeInK*1024 # array of sizeInk*1024 elements

    def Read(self, addr):
        return self.data[addr-self.baseAddr] # addr-self.baseAddr gives index of data

    def Write(self, addr, data):
        self.data[addr-self.baseAddr] = data

    # shows whole memory in format address: data
    def Show(self):
        addr = self.baseAddr
        for i in self.data:
            if i!=0:
                print(hex(addr)+": "+hex(i))
            addr+=1

    # shows memory contents of req range
    def ShowRange(self, start, end):
        addr = start
        while addr <= end:
            print(hex(addr)+": "+hex(self.Read(addr)))
            addr+=1