Do you think Shakespeare is too readable?
Are you a fan of reading illogical prose?
Do you want plays with all the coherence of a drunk parrot?

If you answered "yes" to any of those questions (or you like Markov chains and think they generate funny text), then `fakespeare` is for you!

# What it is

Fakespeare is a Markov chain implemented in C which is intended to generate fake text that vaguely resembles Shakespeare's plays.

It is well-known that a monkey typing at a typewriter will *eventually* produce all of Shakespeare's plays.
Imagine we have an ideal monkey (which might be frictionless and spherical).
Them monkey is illiterate, as all monkeys are.
However, it clearly has not been drinking *that* much, since it is capable of remembering the last key it pressed.
Therefore, we can say that the next key it presses is dependent on the previous key it pressed.

Furthermore, this monkey is sitting at a "macro-typewriter", or perhaps just a PC running EMACS.
The typewriter has a very interesting gimmick.
Atop all the usual keys, it also has a large set of "macro keys".
A macro key can do only one thing: It presses two other keys in a fixed order.

As it turns out, this simple model is sufficient to make vaguely-Shakespearean text.
By having these "macro keys" represent sufficiently large concepts, such as whole words or even phrases, we can significantly increase the likelihood that the monkey generates legible text.
If we further assume that our ideal monkey has been educated in order to press keys in the most optimal probability distribution possible (so that the text produced by the two keys is very likely to make sense), then we increase this chance even more.

In this program, `generate.py` creates the typewriter in the most optimal way possible, and `main.c` is an implementation of the ideal monkey.
The monkey's brain is stored inside of `markov.h`.
Even though the monkey decides what key to press next based only on the last key it pressed, it is still capable of making very decent text.

# How to use it

Fakespeare is very easy to use and modify.

## Generating text

If you just want to get some fake Shakespeare, then that's easy.
Just run `./fakespeare` and await your text.

## Training a custom model

The model essentially has 2 inputs you can screw with:

- The training text
- The number of tokens

The more text you have, or the more tokens you allow, the longer it'll take to train.
However, this additional time is not wasted. It will allow the model to generate better text.
Note that having more tokens does more good than does having more text.
Since this is a Markov chain and not a GPT, it is not capable of learning nuance even if you let it run for a million years.

You can alter the number of tokens by just altering that integer inside `train.sh`.
That integer is passed to `generate.py`, and just specifies the number of tokens to generate.
It's a very literal parameter.

You can alter the training text in an equally literal way: Just replace `trainingdata.txt` with whatever content you want.
Note that the name must stay the same.
Also, the language you are training on must be a Latin-based language.
This training model currently does not support charsets for languages like Chinese and Greek.
Sorry.

Summary:

- Use `generate.py` to generate `markov.h` and then `cc main.c` to create an executable.
- The executable includes a hard-coded markov table stored inside `markov.h`.

# How it works

We split this into two parts, including `main.c` and `generator.py`.
I'll start with `main.c` first, since it's simpler.

## How `main.c` works

Let's think about the monkey from earlier.
Suppose we have some integer `x`, where `x` represents a key.
We could just take a probability distribution function which corresponds to `x`, defined for the integers `0..n-1` (where `n` is the number of keys we have), and use that to randomly select a subsequent key to press.
If that probability distribution is well-designed, it will often come up with sequences of keys that generate somewhat-sensible text.

By taking the above idea and running it in a loop, we produce our monkey-typewriting program!

Of course, we need to somehow map these keys to the output text.
This is accomplished using a big array of char pointers.
Since all keys are represented as integers `0 <= x < n`, then we can just get the string as `table[x]`.

## How `generate.py` works

The vague formula for `generate.py` is quite simple.
First, take in some input text as a corpus.
Next, split it into tokens in the most optimal way, so that each token represents a large amount of text, but is also not used only once.
You can think of this as akin to a compression scheme.
Finally, use a regular Markov analysis to create a probability distribution for each token which indicates what tokens are likely to come next.

The thing is, the goal of "split it into tokens optimally" is a very hard thing to do.
One modern strategy is called [byte-pair encoding](https://en.wikipedia.org/wiki/Byte-pair_encoding).
Essentially, you start with an array of integers.
It is likely that some pairs of integers occur frequently, and some occur infrequently.
If we assume that "a" and "b" represent integers, then "ababababbaba" has many repeats of "ab" and far fewer repeats of "ba" or "bb".
Hence we would create a token that represents this sequence "ab", and replace each "ab" by that token.
Let's call the new token "c".
So now we have text "ccccbaba".
The next most freqent pair is "cc", which occurs three times.
We replace these by a token "d".
By repeating this, and creating a table of what each new token maps to, we are able to create a very good tokenization of real text.

This algorithm is what I used to tokenize the text for training.
First, I load and pre-process `trainingdata.txt`.
Next, I convert each char into an integer.
I execute the above algorithm, and am left with some tokenized text and an array defining each token.
I can then conduct a typical Markov analysis by calculating `P(next = x | this = y)` for every pair of tokens `x` and `y`.

That's how `generate.py` creates an ideal monkey and it's typewriter.

# Credit to Project Gutenberg

Training data courtesy of Project Gutenberg.
Thanks for [all the good reads](https://www.gutenberg.org/cache/epub/100/pg100.txt), yall.

I used to read a lot of those books when I was younger.
I don't read them as often now, because I read a lot more non-fiction, but those books are still really nice.
You should check out Project Gutenberg if you're into cool books!
After you play with this repo, that is.

