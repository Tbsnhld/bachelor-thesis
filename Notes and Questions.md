# Questions
---
- Latex Setup not working with Overleaf 
- 


# Notes for Statistical Privacy Paper
---

## The relevant 3 W: Who, What, Why
- Who: Dennis Breutigam and Rüdiger Reischuk
- Why: Differential Privacy is not a "realistic" scenario, as it's a pessimistic worst-case scenario which is rarely occuring. 
        It modeling the case that an adversary knows everything about a database except for one entry.
        Statistical Privacy instead models the case where an adversaries previous knowledge is limited and they just know the distribution of the database 
        (and perhaps some more noise information, which is ignored in this paper)
- What: Presents new Definition called (pure) Statistical Privacy and afterwards it defines privacy bounds. It also analyzes different mechanisms for said privacy function: Subsampling, Laplace noise and gaussian noise
    Privacy axioms: 
    - Post-processing: If query and mechanism are statistical-private then a function on that random output is also statistical-private.
    - Convexity: Nochmal erklären
        


What is meant with delta >= max(j)... on page 7. (3)?
P.8 4.1: Adjustment for counting queries -> means total number of entries, so you can calculate it up?
P.9 shortly above Lemma 4. What does Q_+(j) mean? Is it the likelihoodratio?
P.11 4.2 shortly above Theorem2: Subsampling between 0 and 1? Why assuming epsilon <= ln 2?

