def is_sorted(list: list) -> bool:
  is_asc = True
  for i in range(1, len(list)):
    if i == 1:
      if list[i] < list[i - 1]:
        is_asc = False
    if is_asc and list[i] < list[i - 1]:
      return False
    if not is_asc and list[i] > list[i - 1]:
      return False
  return True

print(is_sorted([1, 2, 3, 4, 5])) # True
print(is_sorted([5, 4, 3, 2, 1])) # True
print(is_sorted([1, 3, 2, 4, 5])) # False