import time
import pygame
from Defs import fontlist


def render_string(input_string):
    # Code to render the input string goes here
    mytext = fontlist[40].render(f' {input_string}',(0,0,0))[0]
    return mytext

def test_rendering_time(input_string):
    total_time = 0
    for _ in range(1000):
        start_time = time.perf_counter()
        render_string(input_string)
        end_time = time.perf_counter()
        rendering_time = end_time - start_time
        total_time += rendering_time
    average_time = total_time / 100
    # print(f"Average rendering time for input string : {average_time} seconds")
    return str(average_time)+" "+input_string

# Test cases
print(test_rendering_time("Price 1925"))
print(test_rendering_time("Price 1925.15"))
print(test_rendering_time("Price 1925")+test_rendering_time(".15"))
print(test_rendering_time(".15"))
print(test_rendering_time("1925.15"))
print(test_rendering_time("Price 1925"))
# print(test_rendering_time("1234567890" * 1000))
