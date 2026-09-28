# mt19937-random

MT19937 伪随机数生成器（播种、twist、tempering、状态存取），只用 Python 标准库。

```
python3 -m mtrandom.cli --seed 42 --count 3 --compare
python3 -m mtrandom.cli --seed 0 --count 5 --compare
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **tempering 四步都要做**：`y ^= y >> 11`、`y ^= (y << 7) & 0x9D2C5680`、
  `y ^= (y << 15) & 0xEFC60000`、`y ^= y >> 18`。
  `--seed 42 --count 3 --compare` 现在 `match=false`，按口径要与标准库 `random.Random(42).getrandbits(32)`
  的前 3 个值逐位相同（`--seed 0 --count 5` 同样要求）。
- **twist 的下标要对**：`state[i] = state[(i+M) % N] ^ (y >> 1) ^ (y & 1 ? MATRIX_A : 0)`，
  下一项用 `state[i+1]` 拼高低位；现在写成 `(i + M + 1) % N`，整体偏了一位。
- 播种：`state[0] = seed`，之后 `state[i] = 1812433253 * (state[i-1] ^ (state[i-1] >> 30)) + i`（截 32 位）。
- 输出范围：`next_uint32` 落在 `[0, 2^32)`；`uniform` 落在 `[0, 1)`；`set_state` 要校验状态长度与下标。
- 不变量：同一种子给同一序列；状态存取后能续上原序列；跨过 624 个值的 twist 边界后序列依然与参考实现一致；
  取 1 万个值做卡方检验（10 个桶）落在可接受范围内。
- 规模：10^7 次取值 5 秒内完成，内存 O(624)；不许每个值都重新播种。

## 现在的行为

- `next_uint32` 的 tempering 只做了前两步，输出与标准 MT19937 不同。
- `twist` 的下一项下标是 `(i + M + 1) % N`，比标准实现偏一位。
- 因为两处都错，`--compare` 一直是 `match=false`；状态存取本身还有效（内部一致）。

## 计划新增的能力

```
--seed N            种子
--count N           输出多少个 32 位整数
--compare           与标准库 random 对照
--state-roundtrip   验证状态存取
```

## 输出

```
values=1608637542,3421126067,4083286876
expected=1608637542,3421126067,4083286876
match=true
```

## 目录

```
mtrandom/mt.py     MT19937
mtrandom/cli.py    命令行入口
tests/             unittest 用例
```
