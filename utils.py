def input_int(prompt: str | None = None, allow_list: list[int] | None = None):
    while True:
        try:
            input_val = int(input(prompt))
            if allow_list and input_val not in allow_list:
                raise ValueError("入力された値が不正です")
            return input_val

        except ValueError as e:
            print(e.args[0])
