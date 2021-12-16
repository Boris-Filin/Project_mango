import math

def isPrime(n):
	for i in range(int(math.sqrt(n)) + 1):
		if not n % i:
			return False
	return True

while True:
	n = int(input("Number: "))
	if n <= 1:
		print("Not greater than one")
	else:
		if isPrime(n):
			print("Is prime")
		else:
			print("Is not prime")