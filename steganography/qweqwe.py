def er(num: int):
    """
    расширитель строки. до числа бинарных символов кратных 8.
    вход num - сумма символов в ASCII
    выход string - строка бинарных символов длиной кратной 8.
    """
    string = str(bin(num)).replace('0b', '')
    counter = 8 - len(string)
    for i in range(counter):
        string = '0' + string
    return string


if __name__ == '__main__':
    ...
