import itertools

# Luhn 校验算法
def is_valid_luhn(card_number):
    total = 0
    reverse_digits = card_number[::-1]  # 反转卡号
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:  # 从倒数第二位开始每隔一位乘2
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0

# 生成卡号的程序（包括Luhn校验）
def generate_valid_card_numbers(bin_number, user_input_middle_number, user_input_tail, card_length):
    # 卡号长度应该是12到19位
    if card_length not in range(12, 20):
        print("错误：卡号长度无效。请选择12到19位之间的长度。")
        return []

    # 生成所有可能的中间和尾部数字
    possible_middle_numbers = generate_possible_numbers(user_input_middle_number)
    possible_tail_numbers = generate_possible_numbers(user_input_tail)

    card_numbers = []

    for middle in possible_middle_numbers:
        for tail in possible_tail_numbers:
            # 计算需要的填充长度
            current_length = len(bin_number) + len(middle) + len(tail)
            padding_length = card_length - current_length

            if padding_length < 0:
                continue  # 无法满足总长度要求

            # 生成所有可能的填充部分
            if padding_length == 0:
                paddings = ['']
            else:
                paddings = itertools.product('0123456789', repeat=padding_length)
                paddings = [''.join(p) for p in paddings]

            for padding in paddings:
                full_card = bin_number + middle + padding + tail
                if len(full_card) != card_length:
                    continue  # 确保长度正确
                if is_valid_luhn(full_card):
                    card_numbers.append(full_card)

    return card_numbers

# 生成所有可能的数字替代*号
def generate_possible_numbers(input_string):
    if '*' not in input_string:
        return [input_string]  # 如果没有*，直接返回输入
    num_stars = input_string.count('*')
    replacements = itertools.product('0123456789', repeat=num_stars)
    possible_combinations = []
    for replacement in replacements:
        new_str = input_string
        for digit in replacement:
            new_str = new_str.replace('*', digit, 1)
        possible_combinations.append(new_str)
    return possible_combinations

# 主程序
def run_card_number_generator():
    while True:
        print("自定义卡号工具\n")

        # 获取用户输入
        bin_number = input("请输入银行卡的BIN（前6位数字）：")
        if len(bin_number) != 6 or not bin_number.isdigit():
            print("错误：BIN必须是6位数字，请重新输入。")
            continue

        # 提示用户输入自选部分
        print("\n现在，请选择输入银行卡号中的自选部分（如果不填，默认不填）。\n如果希望生成多个组合，可以使用 * 作为占位符。")
        user_input_middle_number = input("请输入银行卡号的自选部分（可以是任意长度的数字或 *）：")
        if not all(c in '0123456789*' for c in user_input_middle_number):
            print("错误：自选部分必须是数字或 *，请重新输入。")
            continue

        # 提示用户输入卡号的最后部分
        print("\n接下来，您需要输入银行卡号的最后部分（4到6位数字或 *）：")
        user_input_tail = input("请输入银行卡号的最后部分（4到6位数字或 *）：")
        if not all(c in '0123456789*' for c in user_input_tail):
            print("错误：尾部自选部分必须是数字或 *，请重新输入。")
            continue
        if len(user_input_tail) < 4 or len(user_input_tail) > 6:
            print("错误：尾部部分长度必须在4到6位之间。")
            continue

        # 提示用户选择卡号长度
        print("\n最后，请选择您需要的银行卡号的总长度：")
        try:
            card_length = int(input("请输入卡号长度（12到19位）："))
        except ValueError:
            print("错误：请输入有效的数字。")
            continue
        if card_length not in range(12, 20):
            print("错误：卡号长度无效。请选择12到19位之间的长度。")
            continue

        # 生成所有有效卡号
        card_numbers = generate_valid_card_numbers(bin_number, user_input_middle_number, user_input_tail, card_length)

        if card_numbers:
            print(f"\n共生成了 {len(card_numbers)} 个有效卡号：")
            for card_number in card_numbers:
                print(card_number)
        else:
            print("没有生成任何有效卡号，可能是输入参数不符合要求，请检查。")
        
        # 询问用户是否重新执行程序
        repeat = input("\n是否重新执行程序？（y/n）：")
        if repeat.lower() != 'y':
            break

# 运行程序
if __name__ == "__main__":
    run_card_number_generator()