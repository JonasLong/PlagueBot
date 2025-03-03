# PlagueBot
 This bot runs a minigame which simulates the spread of a fictional disease within a Discord server (think Plague Inc.)

 Users begin as Healthy and have a random chance to become Infected when chatting with an Infected user. Admins can configure the probability of transmission, recovery, and mortality using commands.

## Commands
- help: Displays help message
- prefix (str): Sets the prefix to begin bot commands (default `!`)
- Infection Commands:
  - heal (user): Marks the target user as Healthy
  - infect (user): Marks the target user as Infected
  - kill (user): Marks the target user as Dead
  - healall: Marks all users as Healthy
  - infectall: Marks all users as Infected
  - killall: Marks all users as Dead
- rolesetup: Creates each of the roles [Healthy, Infected, Dead] and binds them
- setrole: Bind a currently existing role as one of the bot roles
- viewroles: Display info about the current roles
- Statistics:
  - healc: Display or set probability that an Infected user will become Healthy after sending a message
  - infc: Display or set probability that a Healthy user will become Infected after sending a message
  - deathc: Display or set probability that an Infected user will become Dead after sending a message
  - stats: Display all of the above probabilities
