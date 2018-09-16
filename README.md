Installation guide
==================

```
git clone <repo url>
cd loadimpact_assignment
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py test --exclude-tag=perfomance
```

Some thoughs about the implementation
--------------------------------------

My first solution was straightforward and based on intuition. It iterates over all cities, compares how many DE we need
with/without DM and in case it beats best score, we have new one.  
Then i decided that it wouldn't hurt to add some math. I explained the problem using system of inequations:  
![Image of Yaktocat](https://i.imgur.com/NbTbgfD.jpg)  
Where xi is a number of engineers, m is a DM capacity and e is DE capacity. I solved that problem by iteration over
all cases, calculating total number of engineers and picking the best one. It didnt work well in terms of perfomance
beause for n cities it had to iterate over n cases and each of them consisted of n calculations.  
Then i decided to rewrite it a bit so it became an equation with a number of constraints and treat the problem as
optimization problem so i could use third party optimizer and it looked like this:  
![Image of Yaktocat](https://i.imgur.com/gJqEJWg.jpg)  
Where xi and yi - number of managers and engineers accordingly. I started working with SciPy because it is kind of
default pick when it comes to math and python. It turned out that SciPy's optimizer cant provide integer results so i
had to find another libriry and i chose PuLP. For some reason it gave even worse perfomance. There are still some
options to improve this implementation though. At least i could generate extra inputs and compare results of different
algorithms. I put all the code i used for rhar in PerfomanceTestCase.
