import struct

def undenormalise(sample):
    # 将浮点数转换为二进制表示
    binary = struct.unpack('!I', struct.pack('!f', sample))[0]
    # 检查指数部分是否为0
    if (binary & 0x7f800000) == 0:
        sample = 0.0
    return sample