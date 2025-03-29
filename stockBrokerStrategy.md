# How this more than dumb strategy works
We analise the result of the previous round which can have two outcomes
- We won
- We lost or there was a tie

# First round of a game

    In the first round we will select a random word from indexes 20 to 40, and inbetween games we can fine tune it

# How do we interpret winning

    If we won we analyse the difference of the total cost, and we will put a word that is less than the previous, the difference being based of the absolute cost difference

# How de we interpret losing or tieing

    If we lost we increase the price of our next word, but no more than the difference of our absolute cost difference IF we are leading
