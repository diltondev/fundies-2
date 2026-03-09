from collections.abc import Iterable
def flatten_list(inList: list) -> list:
    ret: list = []
    for item in inList:
        if isinstance(item, Iterable):
            ret += flatten_list(item)
        else:
            ret.append(item)
    return ret

def ways(n: int, memo: dict[int: int] = dict()) -> int:
    if n in memo:
        return memo[n]
    ret: int = 0
    if n >= 5:
        tmp = ways(n-5, memo)
        memo[n-5] = tmp
        ret += tmp
    if n >= 2:
        tmp = ways(n-2, memo)
        memo[n-2] = tmp
        ret += tmp
    if n >= 1:
        tmp = ways(n-1, memo)
        memo[n-1] = tmp
        ret += tmp
    if n == 0:
        return 1
    return ret


if __name__ == "__main__":
    print(flatten_list([[1, 2], [3, [4, 5]], 6, [[[[[3]]]]]]))
    print(f'ways with 5p {ways(50)}')