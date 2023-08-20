Use **{person}** to mention a person in the flavor text.

Eg. `{person} has great muzzling skills.`
> **@Carmine** has great muzzling skills.

Use **{person.Pronoun}** or **{person.pronoun}** to output the relevant pronoun.

Eg. `{person.He} has a muzzle. {person.His} muzzle is tight. {person.He} put it on {person.himself}.`
> **She** has a muzzle. **He**r muzzle is tight. **She** put on herself.

Because English is a stupid language, '**heis**' and '**s**' pronouns have been provided.
This is so that 'they' does not mangle grammar for enbys on present tense verbs.

Eg. `{person} is a good sub. {person.Heis} handling {person.his} muzzle very well.`
> **@Carmine** is a good sub. **She is** handling **her** muzzle very well.
> **@Ernest** is a good sub. **They are** handling **their** muzzle very well.

Eg. `Watch out for {person}. {person.He} muzzle{person.s} lots of people.`
> Watch out for **@Carmine**. **She** muzzle**s** lots of people.
> 
> Watch out for **@Ernest**. **They** muzzle lots of people.

See `Pronouns/pronouns.py` for a complete list.
