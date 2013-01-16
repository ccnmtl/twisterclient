# Introduction

TwisterClient is a simple python client interface to a
[https://github.com/ccnmtl/twister/](Twister) server.

# Installation

grab the code from git, do 'easy_install .'

# Examples

Here's a sample interactive session showing basically how
twisterclient is used:

    >>> from twisterclient import TwisterClient as TC
    >>> tc = TC("http://twister.example.com/")
    >>> tc.randint(a=0,b=100,n=10).values
    [16, 6, 30, 82, 93, 22, 36, 32, 5, 93]
    >>> tc.beta(alpha=1,beta=2,n=10).values
    [0.125162457172, 0.34501814743300002, 0.045099459151500002, 0.124022881902, 0.22895619015099999, 0.51336343612500002, 0.15387998667899999, 0.88984285971699995, 0.39228822764600002, 0.103056072043]
    >>> r = tc.uniform(a=0,b=100,n=10)
    >>> r.seed
    u'0.359850996471'
    >>> r.n
    10
    >>> r.params
    {u'a': u'0', u'b': u'100'}
    >>> r.values
    [0.38161708464400002, 27.8083811887, 72.668781842300007, 75.801429652899998, 31.938623311899999, 54.471519895299998, 13.424383519499999, 53.451658934400001, 52.446634499200002, 61.475240338100001]
    >>> r2 = tc.uniform(a=0,b=100,n=10,seed=r.seed)
    >>> r2.seed
    u'0.359850996471'
    >>> r2.values
    [0.38161708464400002, 27.8083811887, 72.668781842300007, 75.801429652899998, 31.938623311899999, 54.471519895299998, 13.424383519499999, 53.451658934400001, 52.446634499200002, 61.475240338100001]

# API

First, create a new TwisterClient object, specifying the Twister
server's base URL:

    from twisterclient import TwisterClient
    tc = TwisterClient("http://twister.example.com/")

then, you can call the distributions on that object. The distributions
available (and their params) are:

* beta: alpha, beta
* expo: lambd
* gamma: alpha, beta
* gauss: mu, sigma
* lognormal: mu, sigma
* pareto: alpha
* uniform: a, b
* randint: a, b
* vormises: mu, kappa
* weibull: alpha, beta

They correspond to the equivalent functions defined in the python
standard random library.

each can also accept `seed`, and `n` arguments, which default to `None`,
and `1`, respectively.

They all return a TwisterResponse object which has the following attributes:

* seed: the seed used to generate the numbers
* values: list of random numbers generated
* n: the n parameter
* params: params specified
* json: raw json string that the Twister server returned
* next_seed: a new seed randomly generated. used for seed chaining (see below)

# Seed Chaining

If an application is making repeated requests for random values from
twister and needs to be able to repeat the sequence of results (eg,
for a scientific simulation), you need to be able to specify a
different seed for each request. Twister now supports chaining
seeds. On each request to a twister server, it will return a
`next_seed` value which is a randomly generated value appropriate to
use for a seed. If you enable chaining in a TwisterClient object, it
will transparently take care of using these `next_seed` values as the
seed for the next request it makes.

    tc = TwisterClient("http://twister.example.com/",chain=True)
    >>> r = tc.randint(a=0,b=10,seed="an initial seed")
    >>> r.seed
    u'an initial seed'
    >>> r.values
    [0]
    >>> r.next_seed
    u'0.279126552632'
    >>> r2 = tc.randint(a=0,b=10)
    >>> r2.values
    [8]
    >>> r2.seed
    u'0.279126552632'
    >>> r2.next_seed
    u'0.459606127637'
    >>> r3 = tc.randint(a=0,b=10)
    >>> r3.seed
    u'0.459606127637'
    >>> r3.values
    [0]

Since the next_seed values are generated by twister from the random
generator seeded with the previous seed value, the sequence will be
repeatable. So you can replay the entire sequence from only the
initial seed.
