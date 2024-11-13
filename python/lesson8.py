def is_divisible(num_list: list) -> bool:
  sum = 0
  product = 1
  for num in num_list:
    sum += num
    product *= num
    
  # 0で割ることはできない
  if sum == 0:
    return False
  
  return product % sum == 0
  
print(is_divisible([3, 2, 1])) # True
print(is_divisible([0, 0, 0])) # False