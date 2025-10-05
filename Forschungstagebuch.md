Bachelorarbeit Statistical Privacy
---

# Fragen


- Muss ich bei der Definition von Differential Privacy für Subsampling seperat von Noise definieren oder klappt es wenn ich von Queryantworten spreche?
- Gerade implementiert unterscheiden sich die Datenbanken darin, dass eine Datenbank das kritische Element enthält und die andere nicht. Ist es relevant, dass die beiden gleich groß sind?

# Einträge

## Vorlage

### Datum

#### Thema: Recherche | Implementierung | Schreiben

#### Inhalt:

---

## Einträge

### Nachtrag 09.07 - 13.07.2025

#### Thema: Recherche 

#### Inhalt:

- Statistical Privacy Paper
  - Paper gelesen, ohne die Beweise und Definitionen zu erarbeiten.
  - Definition erarbeitet: Statistical Privacy, Differential Privacy, Databases, Queries
- fertig Blog: Differential Privacy: https://desfontain.es/blog/friendly-intro-to-differential-privacy.html


### Nachtrag 14.07 - 20.07.2025

#### Thema: Recherche

#### Inhalt: 

- Statistical Privacy Paper:
  - Definition erarbeitet: Subsampling
  - Wengenroth: Wahrscheinlichkeitstheorie: 


### Nachtrag 21.07 - 28.07.2025

#### Thema: Recherche + Implementierung

#### Inhalt:

- Satistical Privacy Paper: Pure Statistical Privacy, Noise, Utility Loss, Statistical Utility Loss
- Aufsetzen Latex Thesis Vorlage
- Erstellen Git Projekt
- Erstellen Forschungstagebuch

### 29.07-08.08.2025

#### Thema: Recherche + Implementierung

#### Inhalt: 

- Implementierung simple synthethische Datenbank
- Implementierung Noise Mechanismen: Gauss und Laplace, Subsampling
- Implementierung: Vorgefertigte Mittelwertquery für Angreifer 
- Recherche: Max-liklihood, synthethische Datenbanken

#### Datenbank: 
A database consists of a sequence of $n$ entries $I_1, ..., I_n$. A database entry $I$ is made of $d$ attributes and can be viewed at as a vector of space $A = A^{(1)}\times ... \times A^{(d)}$. An attribute $a_i$ can take different values from $A^{(i)}$, formally $a_i \in A^{(i)}$. The attributes together make up an database entry $I = (a_1, ..., a_d)$. 
For each database the only available information is the distribution of the attributes. 


For testing purposes each database also includes an entry $I_{critical}$ which is a fixed entry and not included in the previous distribution. 

#### Density function / Distribution $\mu$ 
More specifically the distribution is $\mu = (\mu_1,...,\mu_n)$ for $A^n$ and $\mu_i$ is the marginal distribution for the attributes in $A^{(i)}$.
The fixed entry $I_{critical}$ is a special case of entry where $\mu_{j} \equiv a$, with $j$ being the index number of $I_{critical}$ and $a$ being a constant value of $supp(\mu_j)$.


##### Neighborhood
All neighboring databases $D$ and $D'$ are neighbors if there exists an index $j \in \{1,...,n\}$ such that
$$I_j \neq I'_j\;and\;I_k=I'_k\;for\;all\;k\neq j$$
That is, they differ in one entry, where $I_j = \alpha$ and $I'_j=\beta$ for $\alpha,\beta \in A$. 
#### Binäre-Datenbank: 
For a simple binary database a database entry $I$ consists only of one attribute a with $A = A^{(1)} := \{0,1\}$. The attribute $a$ is selected at random where $p = Pr(a=1)$ is the probability that $a = 1$.


The critical entry the Database receives is a fixed additional entry $I_{critical}$, where the attributes $\alpha,\;resp.\; \beta \in A$ are not selected at random and instead are predefined. 


#### Query
 Given a database D with $I_1, ..., I_n$ entries, then a query $q$ is a measurable function which is part of the set $Q$ of queries the database can answer. All possible queries $F$ can be described by $q: A^n \rightarrow R$. $R \in \mathbb{Q}$ is the answer to the query.
 
 This set of queries is limited to queries that won't provide specific information about an entry or rather where the order of entries is irrelevant for the answer of the query. This means a query must be a symmetric function. Information of a database can be prompted by asking for properties $U \subseteq A$. ~ ~~The probability that an entry $I_j$ has the property $U$ is defined by $\mu_j (U) := \sum_{a \in U} \mu_j(a)$. As trivial properties $\mu_j(U)=0\; or\; 1$ would be obsolete they aren't considered in the following.~~ (And also aren't implemented in the query interface of the databases)
 Given a database $D$ of size $n$ with entries $I_1, ..., I_n$ a property query $q(D)$ would be a subset $A_q \subseteq A$. The answer to said query is ==$R_q(D) := |\{j|I_j \in A_q\}|$. For each entry it is checked whether $I_j$ is part of the subset of attributes $A_q$ and then the count of indexes, which satisfy this are returned.==  
 But as the database $D$ is not fixed, but rather distributed, the answer to our query needs to factor in the distribution $\mu$. The answer is in this case a random variable with Expectation $E[R_q(D)]=\sum_j \mu_j(A_F)$.   

#### Attack Model
An Attack Model describes the method by which an adversary is deciding on whether the critical entry $I_{critical}$ has value $\alpha$ in the result $R_q(D)$ returned by the query $q$.

##### Maximum Likelihood 
In this attack model, the adversary uses the a priori knowledge of the database distribution (and the size) to make the decision if the critical entry is contained in the query answer.


#### Mechanisms
To ensure data privacy a mechanism $M$ is used. This mechanism can be described as a function which, given database $D$ distorts the answer answer to a query $q(D)$. It is denoted by $M(D,q)$ and returns a random variable on $\mathbb{Q}$. 


#### Additive Noise
If mechanism $M$ is a noise function $N$ defined by a random variable V that has a mean of 0 and is independent of the database distribution $\mu$ then $N(D,q):= R_q(D) + V$ is the additive noise mechanism for query $q$.


##### Gaussian Noise
If $V = V(0,\psi^{2})$ it's a normal distributed distributed noise mechanism with standard deviation $\psi$ and indicated with $GAU_{\psi}$. 

###### Laplace Noise
If $V =Lap(\psi)$ the mechanism is Laplace distributing with scaling factor $\psi$ and variance $2\psi²$ and indicated with $LAP_{\psi}$  


#### Subsampling

Another possible mechanism is subsampling, which answers a query by randomly taking a sample of size $m << n$, where $n$ is the size of entries. In this case the adversary knows the total size n of entries for a database as well a the sample size m. This is necessary in the case of counting queries, where only counting the subsampled values would provide incorrect results. 
Given database $D$ and a subsampling mechanism $S$ then $S(D, q)$ is the query run on the subsampled database. 

The probability for all entries is the same. Thus each entry influences the result of a query $R$ by the same amount.


#### Monte-Carlo Simulation
To gain insight in the successfulness of the Attack Model a Monte-Carlo simulation is run. In this case for each run a new database is generated from the same distribution with a separate last element, which is the critical element. The result of the Monte-Carlo Simulator is the success rate over all runs.

#### Privacy



###### Differential Privacy
The setting that an adversary knows all entries $I_1,...,I_n$ except for the critical entry $I_{critical}$ of a Database $D$ has been described by Differential Privacy. 
The answer to a mechanism $M$ applied to a query $q$ is ($\epsilon, \delta$)-differential private for all Databases $D\;\in\;A^n$ and $D'\;\in\;A^n$ where $D=(I_1,...,I_n,I_{critical}=\alpha)$ and $D'=(I_1,...,I_n,I_{critical}=\beta)$ and $S \subseteq R$ if
$$\mathbb{P}[M(q,D)\in S]\leq e^{\epsilon}\mathbb{P}[M(q,D')\in S] + \delta $$.



### Class UML

Live Preview: [via Mermaid UML](https://www.mermaidchart.com/app/projects/b80c2df0-1bca-45cd-8f53-25c680fc314d/diagrams/86edd248-3445-4139-b59f-528f4c1daefd/share/invite/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkb2N1bWVudElEIjoiODZlZGQyNDgtMzQ0NS00MTM5LWI1OWYtNTI4ZjRjMWRhZWZkIiwiYWNjZXNzIjoiVmlldyIsImlhdCI6MTc1Nzg3MTQ4MX0.yNxpuWSvHQucBJNJxyAvLu4g_FF21MGXlNF1T7qTJhw)

![[Builder _ Mermaid Chart-2025-09-18-195614.jpg|440]]
The system is based around a builder to easily create different types of experiment setups. The observer is used to handle all the end presentation as well as to provide logging as needed. 
Currently the setup is as follows, the Tester is created and is used to construct the experiment. To construct the $Experiment$ the $Experiment \;Builder$ creates a $\text{Attack Model, Mechanism and a Database configuration}$. The database configuration is passed to the experiment which ensures that new data is created but with the same configuration.  

Afterwards each Experiment is passed to a $Runner$, which in this case is a Monte Carlo Simulator and determines the success rate of the adversary correctly deciding on the existence of the critical element. Therefore each run returns either true, if the adversary decided correctly or false if it did not. 


##### Tester
Tester is the object resembling the User / Tester, this can later be used to include f.e. a CLI interaction or implementing the user interface. Here the Experiment class is built/configured and handed to the Simulator / Runner.

##### Simulator / Runner
The Simulator is an interface which in turn is inherited/implemented by the MonteCarloSimulator. The Simulator is run the preconfigured experiment a certain amount of times. It's connected to observers, which are notified at the end of every run and can be used to include logging and create graphics. The current implementation of the runner doesn't provide multi-threading, however this is a planned change to make running multiple experiments quicker. 


##### Experiment Builder
Is handling the creation process of the Experiment, and used to configure the Attack Model, the Database type and Query and the Mechanism. It receives the necessary information to create each part of the experiment needed. 

##### Attack Model
The decision process used by the adversary to conclude/decide on whether the critical element was included in the processed query. 

##### Database
A interface for the later used synthetic databases used in the experiment, because of different values the databases are different in the queries they provide. Currently there are the following databases provided: a binary database where each entry has either the value 0 or 1. There is also a numeric database where each entry can be a value between 0 and 10, this allows for more queries  

