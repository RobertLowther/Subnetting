import os
import random


privateRangeA = (0b00001010000000000000000000000000, 0b00001010111111111111111111111111)
privateRangeB = (0b10101100000100000000000000000000, 0b10101100000111111111111111111111)
privateRangeC = (0b11000000101010000000000000000000, 0b11000000101010001111111111111111)


aMask = 0b11111111000000000000000000000000
bMask = 0b11111111111111110000000000000000
cMask = 0b11111111111111111111111100000000
fullMask = 0b11111111111111111111111111111111


def getRandomIpFromRange(range):
    return random.randint(range[0] + 1, range[1] - 1)


def binToIPv4(ipBin):
    ipStr = format(ipBin, '032b')
    ip = [int(ipStr[0:8], 2), int(ipStr[8:16], 2), int(ipStr[16:24], 2), int(ipStr[24:32], 2)]
    return ip


def iPv4ToBin(iPv4):
    ip = "".join([format(val, '08b') for val in iPv4])
    ip = int(ip, 2)
    return ip


def cidrToSubnet(cidr):
    subnetBinStr = '1'*cidr + '0'*(32-cidr)
    return binToIPv4(int(subnetBinStr, 2))


def prettyIPv4(iPv4):
    return ".".join([str(val) for val in iPv4])


def printNetworkStats(ip, cidr, showCidr):
    print("Ip: " + prettyIPv4(ip), end="/" if showCidr else "\n")
    print(cidr if showCidr else f"Subnet Mask: {prettyIPv4(cidrToSubnet(cidr))}")


def main():
    showCidr = random.randint(0, 1) == True
    ipClass = chr(random.randint(65, 67))
    ipBin = getRandomIpFromRange(privateRangeA if ipClass == 'A' else (privateRangeB if ipClass == 'B' else privateRangeC))
    ipv4 = binToIPv4(ipBin)
    cidrMask = random.randint(8, 15) if ipClass == 'A' else (random.randint(16, 23) if ipClass == 'B' else random.randint(24, 30))
    subnetMask = cidrToSubnet(cidrMask)
    hostMask = (32 - cidrMask) % 8
    if hostMask == 0: hostMask = 8
    blockSize = 2**(hostMask)
    
    networkAddress = [val for val in ipv4]
    targetIndex = int(cidrMask / 8)    
    for i in range(targetIndex, 4):
        if i == targetIndex:
            networkAddress[i] = int(networkAddress[i] / blockSize) * blockSize
        else:
            networkAddress[i] = 0
    
    broadcastAddress = [val for val in networkAddress]
    for i in range(targetIndex, 4):
        if i == targetIndex:
            broadcastAddress[i] = broadcastAddress[i] + blockSize - 1
        else:
            broadcastAddress[i] = 255

    if ipv4[3] == broadcastAddress[3]:
        ipv4[3] -= 1

    firstValidIP = [val for val in networkAddress]
    firstValidIP[-1] += 1
    lastValidIP = [val for val in broadcastAddress]
    lastValidIP[-1] -= 1
    
    correctNetAddress = prettyIPv4(networkAddress)
    correctBroadAddress = prettyIPv4(broadcastAddress)
    correctRange = prettyIPv4(firstValidIP) + " - " + prettyIPv4(lastValidIP)

    firstAsk = True
    inputNetAddress = ""
    while inputNetAddress != correctNetAddress:
        os.system('cls')
        # print(f"{prettyIPv4(ipv4)}/{cidrMask}")
        # print(prettyIPv4(subnetMask))
        printNetworkStats(ipv4, cidrMask, showCidr)
        print()

        if not firstAsk:
            print("More info here")
            print()

        inputNetAddress = input("What network does the above address belong to? ")
        firstAsk = False

    print("Correct!\n")

    firstAsk = True
    inputBroadAddress = ""
    while inputBroadAddress != correctBroadAddress:
        os.system('cls')
        #print(f"{prettyIPv4(ipv4)}/{cidrMask}")
        #print(prettyIPv4(subnetMask))
        printNetworkStats(ipv4, cidrMask, showCidr)
        print()
        print(f"What network does the above address belong to? {correctNetAddress}")
        print("Correct!\n")

        if not firstAsk:
            print("More info here")
            print()

        inputBroadAddress = input("What is the broadcast address for this network? ")
        firstAsk = False

    print("Correct!\n")

    firstAsk = True
    inputRange = ""
    while inputRange != correctRange:
        os.system('cls')
        print(f"{prettyIPv4(ipv4)}/{cidrMask}")
        print(prettyIPv4(subnetMask))
        print()
        print(f"What network does the above address belong to? {correctNetAddress}")
        print("Correct!\n")
        print(f"What is the broadcast address for this network? {correctBroadAddress}")
        print("Correct\n")

        if not firstAsk:
            print("More info here")
            print()

        inputRange = input("What is the valid ip range for this network? ")
        firstAsk = False

    print("Correct!\n")


if __name__ == "__main__":
    firstRun = True
    while(True):
        if firstRun:
            firstRun = False
        else:
            again = input("Would you like to try another (y, n)? ")
            if len(again) > 0 and again[0] != "y":
                break

        main()