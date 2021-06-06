# Python game of life implementation
----
Pygame version:

"P" for pause/unpause (you can draw cells on pause)

![img](https://user-images.githubusercontent.com/47245582/120940729-5c3bb180-c727-11eb-9beb-f2b4650cd6cd.png)

----

Console version 

``` py
>>> life = GameOfLife.from_file('glider.txt')
>>> life.curr_generation
[[0, 1, 0, 0, 0],
 [0, 0, 1, 0, 0],
 [1, 1, 1, 0, 0],
 [0, 0, 0, 0, 0],
 [0, 0, 0, 0, 0]]
>>> for _ in range(4):
...    life.step()
>>> life.curr_generation
[[0, 0, 0, 0, 0],
 [0, 0, 1, 0, 0],
 [0, 0, 0, 1, 0],
 [0, 1, 1, 1, 0],
 [0, 0, 0, 0, 0]]
>>> life.save(pathlib.Path('glider-4-steps.txt'))
```
