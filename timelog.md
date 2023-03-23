# Timelog

* Bayesian Reinforcement Leraning
* Barbora Barancikova
* 2439071b
* John H. Williamson

## Week 2

### 26 Sep 2022
* *3 hours* RL Deepming course - Introduction to RL, Markov Decision Processes, Bellman Equations

### 27 Sep 2022
* *2 hours* RL Deepming course - Dynamic Programming, Policy Iteration, Value Iteration

### 28 Sep 2022
* *2 hours* Research of Battlesnake and stock market prediction as potential Bayesian RL topics

### 30 Sep 2022
* *0.5 hours* Supervisor meeting

## Week 3

### 3 Oct 2022
* *2 hours* Deepmind RL course - Deep Q learning, experience replay

### 4 Oct 2022
* *2 hours* Deepmind RL course - value function approximation, TD lambda, Monte Carlo methods
* *1 hour* Hall of Fame papers reading

### 5 Oct 2022
* *4 hours* Deepmind RL course and Battlesnake design considerations, pessimism in the face of uncertainty

### 6 Oct 2022
* *2 hours* Value function approximation literature review

### 7 Oct 2022
* *0.5 hours* Supervisor meeting

## Week 4

### 10 Oct 2022
* *1 hour* Deepmind RL course
* *2 hours* Researching Bayes-adaptive tree search

### 11 Oct 2022
* *2 hours* Reseching Gaussian Processes and conjugate prior updates as a choice for the battlesnake architecture
* *3 hours* Tree search and feature design research and architecture write-up

### 14 Oct 2022
* *0.5 hours* Supervisor meeting

## Week 5

### 18 Oct 2022
* *1.5 hours* Created a random player and a death-avoiding random player

### 19 Oct 2022
* *2 hours* Designed heuristics for a non-bayesian battlesnake player
* *1 hour* Implemented a non-bayesian battlesnake heuristic player

### 20 Oct 2022
* *1 hour* Reaserched Battlesnake training gym repository
* *0.5 hours* Found and looked through a battlesnake ruleset repository

### 21 Oct 2022
* *0.5 hours* Supervisor meeting

## Week 6

### 24 Oct 2022
* *2.5 hours* Creating a new state representation
* *1.5 hours* Creating a future state generating function
* *1 hour* Redesigning value and reward functions

### 25 Oct 2022
* *1 hour* Implementing a one step lookahead player using the new state representation
* *1 hour* Setting up for tree search implementation

### 28 Oct 2022
* *0.5 hours* Supervisor meeting

## Week 7

### 1 Nov 2022
* *4 hours* Implementing a non-Bayesian tree search with increasing depth
* *1 hour* Reusing tree nodes to avoid always generating nw ones
* *1 hour* Debugging timeout issues

### 3 Nov 2022
* *2 hours* Timeout prevention by multi-threading the tree search response and tracking time while searching

### 4 Nov 2022
* *0.5 hours* Supervisor meeting

## Week 8

### 9 Nov 2022
* *3.5 hours* Fixed tree search timeout issue by adding an exit condition, restricting state generation, and deleting multi-threading

### 10 Nov 2022
* *2 hours* Switching tree search values to distributions, researching and setting up conjugate prior updates for them
* *2 hours* Implementing mini-max thompson sampling and tree search traversal in a Bayesian tree search

### 11 Nov 2022
* *0.5 hours* Supervisor meeting

## Week 9

### 16 Nov 2022
* *1 hour* Switching the tree search node udates to the Kalman filter
* *4 hours* Builidng the go project to run games n locally and creating a game-playing pipeline

### 17 Nov 2022
* *2.5 hours* Debugging local game-playing pipeline timeout issue

### 18 Nov 2022
* *0.5 hours* Supervisor meeting

## Week 10

### 20 Nov 2022
* *1 hours* Plotting tree search value normal distributions

### 22 Nov 2022
* *3 hours* Fixing a bug in the local pipeline for running games
* *1 hours* Studying gamma-normal conjugate priors
* *1 hours* Implementing conjugate prior updates for tree search nodes

### 23 Nov 2022
* *2 hours* Setting up paremeter tuning variables

### 24 Nov 2022
* *0.5 hours* Supervisor meeting

## Week 11

### 30 Nov 2022
* *3 hours* Implementing multi-threaded parameter tuning for the tree search

### 1 Dec 2022
* *1 hour* Analysing tree search results and producing qq plots

### 2 Dec 2022
* *0.5 hours* Supervisor meeting

## Week 12

### 7 Dec 2022

* *5 hours* Transforming the snake game mode to standrad Royale for all players, testing different baselines against each other
* *1.5 hours* Read articles about experience replay and TD-lambda learning for value function approximation

### 8 Dec 2022

* *0.5 hours* Supervisor meeting
* *3 hours* Research (looking back at David Silver Reinforcement learning lectures about value function approximation)

### 9 Dec 2022

* *5.5 hours* Transforming the snake game mode to standrad Royale, altering the tree search, deployig on the server
* *1 hours* Finding the best player combinaiton to play in a tournament (one step lookahead for 4 players, tree search for 2 players)

### 10 Dec 2022
* *3.5 hours* Reading about Gaussian Processes for reinforcement learning, realising I don't understand Gaussian Processes

## Week 13

### 12 Dec 2022

* *2 hours* Researched and read articles about Gaussian Processes for value funciton approximaiton
* *2 hours* Watched a lecture on Gaussian Processes: https://www.youtube.com/watch?v=4vGiHC35j9s

### 13 Dec 2022

* *2 hours* Watched a lecture on Gaussian Processes and linear regression: https://www.youtube.com/watch?v=MfHKW5z-OOA

### 14 Dec 2022

* *2 hours* Watched a lecture on Gaussian Processes: https://www.youtube.com/watch?v=92-98SYOdlY
* *0.5 hours* Implemented a LCB-UCB miminam tree search and ran parameter tuning
* *1 hours* End of semester report writing

### 15 Dec 2022

* *4 hours* Read articles about value function approximation and backward view TD lambda, came up with a plan of implementation for my project
* *1 hour* Read hall of fame projects and thought about the structure of my dissertation

### 16 Dec 2022

* *0.5 hours* Supervisor meeting
* *2 hours* End of semester report writing
* *3.5 hours* Value function approximation implementation

## Week 14

### 11 Jan 2023
* *2 hours* code rearrangement and inspection, value function approximaiton

### 12 Jan 2023
* *0.5 hours* td lambda research
* *1 hours* td_target calculation
* *2 hours* Gaussian process research and training

### 13 Jan 2023
* *0.5 hours* supervisor meeting

## Week 15

### 17 Jan 2023
* *2 hours* value function approximation -  making it run for for several learning episodes
* *2 hours* evaluation of the learned value function against the heuristic baseline

### 18 Jan 2023
* *1.5 hours* value function approximation - evaluation and decay of the noise term

### 19 Jan 2023
* *1 hours* value function plotting of a one-dimensional slice and analysis of the results

### 20 Jan 2023
* *0.5 hours* analysis of the results
* *0.5 hours* supervisor meeting

### Week 17

### 01 Feb 2023
* *5 hours* value function training and analysis

### 02 Feb 2023
* *4 hours* disseration outline and background section writing

### 03 Feb 2023
* *0.5 hours* supervisor meeting

### Week 19

### 06 Feb 2023
* *2 hours* Background section writing
* *0.5 hours* research question formulation

### 07 Feb 2023
* *1 hours* Background section writing
* *1 hours* Experiment design

### 08 Feb 2023
* *3 hours* Value function evaluation experiments

### 10 Feb 2023
* *0.5 hours* supervisor meeting

### Week 20

### 13 Feb 2023
* *4 hours* Background section writing

### 15 Feb 2023
* *1 hours* Background section writing
* *1 hours* Experiment running

### 17 Feb 2023
* *0.5 hours* supervisor meeting

### Week 21

### 20 Feb 2023
* *2 hours* Trying the linear kernel for the value function, evaluation

### 21 Feb 2023
* *2 hours* Running experiments, plot design, confedence interval design

### 22 Feb 2023
* *4 hours* Background section writing

### 24 Feb 2023
* *0.5 hours* supervisor meeting

### Week 22

### 27 Feb 2023
* *2 hours* Experiment coding and running

### 28 Feb 2023
* *2 hours* Experiment coding and running

### 01 Mar 2023
* *3 hours* Background section writing

### 03 Mar 2023
* *0.5 hours* supervisor meeting

### Week 23

### 06 Mar 2023
* *2 hours* Background section writing

### 07 Mar 2023
* *0.5 hours* last plot creation

### 08 Mar 2023
* *3 hours* Problem statement writing

### 09 Mar 2023
* *3 hours* Evaluation writing

### 10 Mar 2023
* *0.5 hours* supervisor meeting

### Week 24

### 13 Mar 2023
* *3 hours* Evaluation writing

### 18 Mar 2023
* *7 hours* Design writing, making implementation diagrams

### 19 Mar 2023
* *6 hours* Implementation writing

### Week 25

### 20 Mar 2023
* *3 hours* abstract, conclusion writing

### 21 Mar 2023
* *5 hours* Analysis writing and plots

### 22 Mar 2023
* *0.5 hours* supervisor meeting
* *5 hours* Presentation making and recording

### 23 Mar 2023
* *2 hours* Review
* *1 hours* Codebase cleanup and readme creation



