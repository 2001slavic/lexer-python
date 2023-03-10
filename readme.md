# Lexer
Un lexer este un program care imparte un sir de caractere in subsiruri
numite *lexeme*, fiecare dintre acestea fiind clasificat ca un *token*, pe baza
unei specificatii.

## Input
Inputul unul lexer consta in doua componente:
1. o **specificatie**
2. un *text* care va fi analizat lexical, mai precis, impartit in lexeme.

Specificatia are urmatoarea structura:

```
TOKEN1 : REGEX1;

TOKEN2 : REGEX2;

TOKEN3 : REGEX3;

...
```
unde fiecare ``TOKENi`` este un nume dat unui token, iar ``REGEXi`` este un regex
ce descrie acel token. Se poate imagina aceasta specificatie ca un *fisier
de configurare* care descrie modul in care va functiona lexerul pe diverse
fisiere de text.

## Output
Lexer-ul are ca output o lista de forma : ``[(lexema1, TOKEN_LEXEMA_1), (lexema2, TOKEN_LEXEMA_2), …]``, unde ``TOKEN_LEXEMA_N`` este numele token-ului
asociat lexemei n, pe baza specificatiei.

## Exemplu
Fie urmatoarea specificatie:
```
TOKEN1 -> abbc*;
TOKEN2 -> ab+;
TOKEN3 -> a*d;
```
si input-ul ``abbd``. Analiza lexicala se va opri la caracterul ``d`` (AFD-ul
descris anterior va ajunge pe acest caracter in sink state). Subsirul ``abb``
este cel mai lung care satisface atat ``TOKEN1`` cat si ``TOKEN2``, iar ``TOKEN1`` va fi raportat, intrucat il preceda pe ``TOKEN2`` In specificatie
Ulterior, lexerul va devansa cu un caracter pozitia curenta in input, si va identifica subsirul ``d`` ca fiind ``TOKEN3``.

## AFN si AFD
Pentru a implementa functionalitatea lexer-ului am folosit Automate Finite
Nondeterministe (AFN) si Automate Finite Deterministe (AFD), astfel, proiectul
include si alte functionalitati.

### Forma Prenex a expresiilor regulate
Avantajul notatiei prenex este ca parantezele nu mai sunt necesare. De exemplu,
``(1 + 2) * 3`` este scrisa in notatie prenex astfel: ``* + 1 2 3``.
Expresiile regulate in forma Prenex sunt formate din:
1. **atomi**
2. numele **operatiilor** (``UNION``, ``STAR``, ``CONCAT``, ``PLUS``, ``MAYBE``) urmate direct de alte sub-expresii.

Un **atom** poate fi:
* un caracter alfanumeric (e.g. ``0`` sau ``a``)
* un caracter oarecare inclus intre ghilimele simple (e.g. ``'a'`` sau ``';'``)
* unul din cuvintele cheie ``eps`` (pentru sirul vid) sau ``void`` (pentru limbajul vid)

Operatiile:
* ``PLUS e`` (in notatie standard *e*<sup>+</sup>) desemneaza regexul *ee**
* ``MAYBE e`` (in notatie standard *e*?) desemneaza regexul *e*∪*ϵ*
* iar restul operatiilor au semnificatia lor standard.

Urmatoarele sunt exemple valide de expresii Prenex:

* ``UNION a b``, echivalent cu *a*∪*b*
* ``UNION CONCAT a b STAR c``, echivalent cu (*ab*)∪(*c**)
* ``CONCAT UNION a b UNION c d``, echivalent cu (*a*∪*b*)(*c*∪*d*)
* ``CONCAT STAR UNION a b UNION b c``, echivalent cu (*a*∪*b*)*(*b*∪*c*)
* ``STAR UNION CONCAT a b CONCAT b STAR d``, echivalent cu ((*ab*)∪(*b*(*d**)))*
* ``CONCAT PLUS c UNION a PLUS b``, echivalent cu *c*<sup>+</sup>(*a*∪(*b*<sup>+</sup>))
* ``UNION ' ' '@'``, accepta limbajul { `` `` , ``@`` }
* ``UNION eps a``, ``MAYBE a``, echivalente cu *a*∪*ϵ*
* ``void``

### Prenex -> AFN
Thompson's construction.

### AFN -> AFD
Subset construction.

### Regex -> Prenex
Infix to prefix.

### Testare
```
python3 -m unittest
```

## Credits
Enuntul proiectului, testele si scheletul de cod au fost date de echipa materiei
*Limbaje formale si Automate* 2022-2023 din *Facultatea de Automatica
si Calculatoare, Universitatea Politehnica din Bucuresti*.