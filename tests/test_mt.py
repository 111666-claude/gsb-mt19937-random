import unittest

from mtrandom.mt import N, MTRandom, RandomError


class SeedTest(unittest.TestCase):
    def test_state_size(self):
        self.assertEqual(len(MTRandom(1).state), N)

    def test_same_seed_same_sequence(self):
        first = MTRandom(7)
        second = MTRandom(7)
        self.assertEqual([first.next_uint32() for _ in range(5)],
                         [second.next_uint32() for _ in range(5)])

    def test_different_seed_differs(self):
        self.assertNotEqual(MTRandom(1).next_uint32(), MTRandom(2).next_uint32())


class RangeTest(unittest.TestCase):
    def test_uint32_range(self):
        generator = MTRandom(3)
        for _ in range(20):
            value = generator.next_uint32()
            self.assertGreaterEqual(value, 0)
            self.assertLess(value, 2 ** 32)

    def test_uniform_range(self):
        generator = MTRandom(3)
        for _ in range(20):
            self.assertGreaterEqual(generator.uniform(), 0.0)
            self.assertLess(generator.uniform(), 1.0)


class StateTest(unittest.TestCase):
    def test_bad_state(self):
        with self.assertRaises(RandomError):
            MTRandom(1).set_state([0] * 10, 0)

    def test_state_restores_sequence(self):
        generator = MTRandom(11)
        generator.next_uint32()
        state, index = generator.get_state()
        expected = [generator.next_uint32() for _ in range(4)]
        generator.set_state(state, index)
        self.assertEqual([generator.next_uint32() for _ in range(4)], expected)


if __name__ == "__main__":
    unittest.main()
