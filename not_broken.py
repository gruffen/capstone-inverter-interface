import sys
def main():
	sys.stdout = sys.__stdout__
	sys.stdout.write("hi")

main()