Do you think Shakespeare is too readable?
Are you a fan of reading illogical prose?
Do you want plays with all the coherence of a drunk parrot?

If you answered "yes" to any of those questions (or you like Markov chains and think they generate funny text), then `fakespeare` is for you!

# What it is

Fakespeare is a Markov chain implemented in C which is intended to generate fake text that vaguely resembles Shakespeare's plays.
Here's an example of fakespeare's text:

> II. The prison
>  Scene II. Rotty, gentle Tybalt, for ever so his offense.
> 
> FIRST Cour studience, where all.
> 
> [Exc'd. Thus leaving bot!
> No word makes thee hang TAVILLO.
> O, let me have so it
> were more pity dman, look you see referment

## A brief explanation

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

If you want a particular amount of tokens, you use `./fakespeare n`, where `n` is an integer representing the number of tokens.
Please make sure to provide a positive integer.
It does not work for any other text.

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

# Some more text

> die;
> And thereby your hand Queen to tell you know little urg'd forth to me,
> The enedie!
> What's more. If this day my access fear,
> Which you are truth had some more repeal themselvessel of Very tomorrow night's day:
> This venants bit will.
>
> LADY Clife's wife.
> You are the argumus, Pardon'd rach'd together, calls for
> Enter Calen thousand difound,
> Whilst I left me stew me the crowned with kward to cing,
> WOS.
> Go bid the hours upon him, then?
>
> GLOUCESTER.
> [_Aside_.] Ay, who (as your shrending confounds shall controdwell
> From this rend it to alives
> Lands hold him have you wranatio
> CINS.
> VIUS.
> O, would it not for th' douglae envius and Menas a fery JOY.
> But if thy old and the rule grace in.
>
> GLOUCESTER.
> Confrow,
> To have held of Timon speak so ill-burnt and guer foreom of his chase her face. Pripped her: more good,
> Daup to luded and
> ducating him to
> counsel.
>
> FI;
>    OUTIO.
> Here's monstery sailorid. Pray you, I'll rifluous in the complexascaught a,
> And for his peac.
>
> SICINIUS.
> He's weak word than
> Those labour
> Of Charm to that? Thou shalt be the light contents
> Hath pardon as a proppa and cowardship, nierry and brid;
> The grewsbury and Talbot, how choly,
> The reason ruit.
>
> DUKE.
> Play onight to him. Her heart forsworn
>     All flamion.
> On a knightwaintainted thus?
> I will give place I did think, you shall hear him, and that which I thought to 't so,
> Go you,
> The ser'st our plot, 'tis fancell-worthy usiness.
>
> Enter the guid'st with challows the first I will vented third's poor been've my liege! We must give myself?
> Or elder,
> Couse
> requit fire-wooer-emble shall not abrib in this? Why then, have coxity?
> Your father's said,
>     And what lies hends with the found
> Is't back to the fight,
> To compound but such defit
> His madness took his be" royal mind you, sir, three attendingerece
> You will servant.
> Pades.
> This shall be prayers of Harrof heaven
> That they wit. And so trikes me live, alamonalone go, h, whened
>   44
>
> ADRIANCE.
> O, BUTIO.
> And on his life.
>
> BEROWNE.
> Sweet friends.
>
> EDWARD.
> My Lord Timon's fortunes; is not tombents, I look when I am an act a post, O Lord, forsword, what hath usance their comeleither, come in and fire.
>
> OTHELLO.
> Nodrum! this before, our mouth. Enter three of yourself, cocketition
> Is now to bed,
> AYOR.
> Our generate of harms,
> Willible.
>
>  Enter Timon Deeped was
> That touches you live in pure goodly beastepent your hor drument ouglassists
> Are then enter Cutch gentlemen in me.
>
> DOLONIUS.
> Inia and ceed upon the grimage,
> And thereiner ne'er so much monthorn to thee. OOL.
> Come on, dreamt with him.
>
> O, give me an untice be many eviding thus quent clad ght forth? swears;
> For fill'd with confirm
> The large of prey is giveth nay, come before there present foreignibelin so should come to soever I shall off, and you prets,
> And then,
> For thou shrif, and for work the charact of Butense.
>
> MACBETH.
> Then let her friends and ne'er love says, be turned thy wife;
> If she come hill!
> Herein doubting strate of Milor will I myself have forty ins buy legion,
> He's eyes of this metal acquaintive hows is nature. You seem but a bire.
>
> SERVANT.
> He and his phan,
> Come aways,
> Ahends some pitchant pil
> As if you will, to exclament,
> FOxurst not fall in arm
> Th' name speaks, how
> To make him very welcomposition,
>
> belly,
> Tremed.
>
> LUCIUS.
> He wayment of Mistress Antispatter'd him a les, springs, ladder of my way, and to ford, a young No.
>
> THESEUS.
> Go to; honour is sures.
> Your heart th' bid her eyes are their blood, and be one sph France,
> To one tombuckleek'st
>          Duke.
>
> [_Exeunt Cynoon?
>
> ITHATUR.
> This is hem_.]
>
> Salice shame
> ne'er believe we shall
> When se."
>
> Here come
> To call for?
>
> COND.
> Why do nall there is the fembl

