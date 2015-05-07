import spidev
import time

def ReverseBits(byte):
	byte = ((byte & 0xF0) >> 4) | ((byte & 0x0F) << 4)
	byte = ((byte & 0xCC) >> 2) | ((byte & 0x33) << 2)
	byte = ((byte & 0xAA) >> 1) | ((byte & 0x55) << 1)
	return byte



spi = spidev.SpiDev()
spi.open(0,0)
#spi.max_speed_hz = 500000
#spi.bits_per_word = 8
spi.mode=0b00
print(spi.lsbfirst)
print(spi.cshigh)
spi.cshigh = True

while True:
	to_send = [ReverseBits(0x00), ReverseBits(0x00), ReverseBits(0x00), ReverseBits(0x00), ReverseBits(0x00), ReverseBits(0x00)]
	resp = spi.xfer2(to_send)

	time.sleep(1)
	to_send = [ReverseBits(0x3F), ReverseBits(0x3F), ReverseBits(0x3F), ReverseBits(0x3F), ReverseBits(0x3F), ReverseBits(0x3F)]
	resp = spi.xfer2(to_send)
	time.sleep(1)

