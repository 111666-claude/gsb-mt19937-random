"""MT19937 伪随机数生成器，只用标准库。

缺陷：tempering 只做了前两步（少了 (y << 15) & 0xEFC60000 与 y ^= y >> 18），
twist 里下一项的下标也偏了一位。
"""

N = 624
M = 397
MATRIX_A = 0x9908B0DF
UPPER = 0x80000000
LOWER = 0x7FFFFFFF
MASK = 0xFFFFFFFF


class RandomError(ValueError):
    """输入不合法。缺陷：不带原因。"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class MTRandom:
    """MT19937。"""

    def __init__(self, seed=5489):
        self.state = [0] * N
        self.index = N
        self.seed(seed)

    def seed(self, seed):
        self.state[0] = int(seed) & MASK
        for position in range(1, N):
            previous = self.state[position - 1]
            self.state[position] = (1812433253 * (previous ^ (previous >> 30)) + position) & MASK
        self.index = N

    def twist(self):
        """缺陷：下一项下标写成 (i + M + 1) % N，整体偏了一位。"""
        for position in range(N):
            value = (self.state[position] & UPPER) | (self.state[(position + 1) % N] & LOWER)
            mixed = self.state[(position + M + 1) % N] ^ (value >> 1)
            if value & 1:
                mixed ^= MATRIX_A
            self.state[position] = mixed & MASK
        self.index = 0

    def next_uint32(self):
        """缺陷：tempering 少了最后两步。"""
        if self.index >= N:
            self.twist()
        value = self.state[self.index]
        self.index += 1
        value ^= value >> 11
        value ^= (value << 7) & 0x9D2C5680
        return value & MASK

    def uniform(self):
        return self.next_uint32() / 4294967296.0

    def get_state(self):
        return list(self.state), self.index

    def set_state(self, state, index):
        if len(state) != N or not 0 <= index <= N:
            raise RandomError("状态不合法")
        self.state = list(state)
        self.index = index
