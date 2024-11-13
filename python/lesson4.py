def calc_tribonacci(n):
  if n == 0:
    return 0
  elif n == 1 or n == 2:
    return 1
  else:
    return calc_tribonacci(n - 1) + calc_tribonacci(n - 2) + calc_tribonacci(n - 3)
  
print(calc_tribonacci(0)) # 0
print(calc_tribonacci(5)) # 7