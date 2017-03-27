## Tiny Mahjong

### Requirements
* Python3 (tested on Python 3.4)
* Numpy
* sklearn
* pymp
  * install by:
    ```
    python3 -m pip install pymp-pypi
    ```
* (Optional) matplotlib

### Quick Start
```
python3 play.py
```

### Rule

#### Core Idea
This game is about achieve a winning hand by picking and discarding cards.

#### Tile Set
You got 2 sets of tiles: A and B, each set has number 1 to 9, each unique card has 4 duplicated cards. i.e. A1, A1, A1, A1, ~ A9, A9, A9, A9, B1, B1, B1, B1, ~ B9, B9, B9, B9.

That's 72 tiles in total.

#### Game Procedure
There are 4 players. In the beginning, each player is assigned with 4 tiles randomly picked from the tile pile. Then start from a random player, picking 1 tile from the card pile, then discard 1 tile, after that, move on to the next player until the game ends (one player calls win or the tile pile is drained).

So after each round, the players always have 4 cards in hand.

#### How to win
After each time a player picked a tile, he has 5 tiles in hand, if it is a winning hand, then he can call win.

#### Winning hand rule
You need to have a pair(2 tiles) AND a combo(3 tiles) to achieve a winning hand. A pair is two same tiles(same set, same number, e.g. B2, B2). A combo can be in two forms: 3 same tiles(same set, same number, e.g. B7, B7, B7) or 3 continuous tiles(same set, continuous numbers, e.g. A3, A4, A5).

#### Examples
* Winning hands examples:
  * A1, A1, A2, A3, A4
  * A1, A1, A1, A2, A3
  * B1, B1, B9, B9, B9
* NOT winning hands:
  * A1, A2, A3, A4, A5
  * B2, B2, B2, B2, B3
