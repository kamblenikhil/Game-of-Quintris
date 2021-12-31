# Game of Quintris using AI

#### Abstraction - 

1. <b>State Space - </b> All the possible blank cells on the game board and possible moves made by an individual block

2. <b>Initial State - </b> First random block ready to filled in the vast empty board

3. <b>Successor Function - </b> The function takes all the possible moves for the current block and the current state of board. This function will decide where (ie. which row and which column) the current block is to be moved.

4. <b>Evaluation Function - </b> The evaluation function is used to perform rule based calculations using all the iterations (possible moves on the given state of board) for the current block. This function has multiple heuristics like -
<ul>
<li><b>Complete Line - </b> This is probably the most intuitive heuristic among all. It is simply the the number of complete lines in a grid. We’ll want to maximize the number of complete lines, because clearing lines is the goal of the AI, and clearing lines will give us more space for more pieces.</li>
<li><b>Column/Height - </b> This heuristic will tell us about how high the column is. To compute this, we take the sum of the height of each column (the distance from the highest tile in each column to the bottom of the grid). We’ll want to minimize this value, because a lower height means that we can drop more pieces into that column and perhaps in the whole board before hitting the top of the grid.</li>
<li><b>Checking Holes - </b> A hole is an empty space such that there is at least one tile in the same column above it. These holes are harder to clear, because we’ll have to clear all the lines above it before we can reach the hole and fill it up. So we’ll have to minimize these holes.</li>
</ul>

5. <b>Goal State - </b> To meet this goal, our AI will decide the best move for a given block by trying out all the possible moves (rotation, horizontal-flip and direction position).

#### Approach - 

1. Implementation using Min-Max Algorithm: 
<ul>
<li> At first Min-Max was our go to algorithm. As Quintris is a game and creating a gametree using backtracking all possible moves make sense. However, we realised Min-Max considers two-players (computer (our program) and the opponent) where min will always pick up minimum value score from the game and max will always pick up maximum value score and the score will be based on some heuristics. After understanding the implementation and taking several days to implement Min-Max, we found out that this is not the right direction we are going into. </li>
</ul>

2. Implementation using Local Search:
<ul>
<li>The Local Search approach scans the first level of the tree search, selecting the position representing the move that during the simulation would have returned the highest score obtaining an excellent local state.</li>
<li>Since, Local Search does not guarantee the achievement of an excellent overall and its use is often used in situations where the individual paths are very long, in our use it proves to be particularly inefficient and not very productive. After testing our approach for several times, we end up with a maximum score of five. This occurs because, the paths of the search's are very short and the optimal location achieved does not guarantee the performance on the result.</li>
</ul>

#### Challenges - 

1. Our first challenge was to figure out which algorithm fits the best for Quintris AI implementation, which consumed a lot of time.

2. Working on strings (in a lists of list) was difficult when we tried to create the game tree. We were able to make our own functions like left/right/rotate. However, they had many bugs and the implementation was not giving reliable answers. So, to avoid this we start a new game for every move while taking the current state of board and scans the first level of the tree search using David's functional code. <br>