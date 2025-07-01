word = "hello"
letters = [chr(i) for i in range(ord('a'), ord('z') + 1)]
sortedWord = sorted(list(word),key=lambda x : letters.index(x))
print(sortedWord)