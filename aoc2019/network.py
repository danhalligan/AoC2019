from aoc2019.helpers import input_ints
from aoc2019.intcode2 import *


class Computer:
    def __init__(self, file, address, target, network):
        self.packet_queue = []
        self.vm = Intcode(input_ints(file)).input(address)
        self.address = address
        self.target = target
        self.network = network
        self.vm.run_until_input_or_done()
        self.vm.inputs = [-1]
        self.idle = False

    def run_until_io(self):
        xval = self.packet_queue[0][0] if self.packet_queue else -1
        self.vm.inputs = [xval]
        dest = self.vm.run_until_io_or_done()
        if self.vm.paused:
            if self.packet_queue:
                x, y = self.packet_queue.pop(0)
                self.vm.inputs = [y]
                self.vm.run_until_input_or_done()
            else:
                self.idle = True
        else:
            self.idle = False
            x = self.vm.run_until_io_or_done()
            y = self.vm.run_until_io_or_done()
            if dest == self.target:
                return dest, x, y
            self.network[dest].packet_queue.append((x, y))


class NAT:
    def __init__(self, network):
        self.network = network
        self.packet = None

    def idle(self):
        return all(x.idle for x in self.network)

    def send(self):
        self.network[0].packet_queue.append(self.packet)
        self.packet = None
