Made a functional EmberBot using Discord.py

Current Admin commands (user invoking the command must have Administrator permissions within any of their roles):

- `!group new {name} {#}`
- `!group list` (Unavailable)
- `!group delete` (Unavailable)
- `!group clear` (Unavailable)

Name MUST include the wildcard character if you want to make more than one channel (currently ?)
Ex: `!group new saturday-? 22` will make 22 text + voice channels and roles from saturday-1 to saturday-22
Current user commands:

- `!group set {name}`
Name must match an existing channel AND role to be given out (will not match with key roles like Exec, Mentor or President no matter what)
- `!roll 2d6` (Fun dice roller I guess)
