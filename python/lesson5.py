def get_mask_str(value: str, show_last_digit: int) -> str:
  return '*' * (len(value) - show_last_digit) + value[-show_last_digit:]

def mask_last_4_digit(num: int) -> str:
  num_str = str(num)
  return get_mask_str(num_str, 4)

print(mask_last_4_digit(1234567812345678))