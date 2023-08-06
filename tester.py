# import math
# mytuple = (2,3)
# print(math.prod(mytuple))

def count_words(paragraph):
  """Counts the number of words in a paragraph."""
  words = paragraph.split()
  return len(words)

print(count_words("Kyronix Solutions Inc. (ticker symbol: KSTON) is a dynamic company specializing in urban mobility solutions. With a visionary team of engineers and transportation experts, Kyronix is at the forefront of revolutionizing urban transportation through innovative technologies like electric vehicles, smart traffic management systems, and autonomous driving solutions. Their commitment to sustainable and efficient mobility drives progress for cities worldwide. "))
