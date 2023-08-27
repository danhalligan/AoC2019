from aoc2019.network import Computer, NAT


def initialise(file):
    network = []
    for address in range(50):
        network.append(Computer(file, address, 255, network))
    return network


def part1(file):
    network = initialise(file)
    while True:
        for comp in network:
            packet = comp.run_until_io()
            if packet is not None and packet[0] == 255:
                return packet[2]


def part2(file):
    network = initialise(file)
    nat = NAT(network)
    lag = None
    while True:
        for comp in network:
            packet = comp.run_until_io()
            if packet is not None and packet[0] == 255:
                nat.packet = (packet[1], packet[2])
        if nat.idle() and nat.packet is not None:
            if lag is not None and lag == nat.packet[1]:
                return nat.packet[1]
            lag = nat.packet[1]
            nat.send()
