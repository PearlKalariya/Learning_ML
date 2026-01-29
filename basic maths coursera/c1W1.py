import numpy as np

one_dimensional_arr = np.array([10, 12])
print(one_dimensional_arr)

a = np.array([1, 2, 3])
print(a)

b = np.arange(3)
print(b)

c = np.arange(1, 20, 3)
print(c)

lin_spaced_arr = np.linspace(0, 100, 5, dtype=int)
print(lin_spaced_arr)

char_arr = np.array(['Welcome to Math for ML!'])
print(char_arr)
print(char_arr.dtype)

ones_arr = np.ones(3)
print(ones_arr)

empt_arr = np.empty(3)
print(empt_arr)

rand_num = np.random.randint(0, 2, size=1000)
print(rand_num)

array = [10, 20, 30, 40]
random_choice = np.random.choice(array, size=1, replace=False)  
print(random_choice)