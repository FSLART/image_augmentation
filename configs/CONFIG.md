# CONFIG DIRECTORY

### SubDirectory to keep ini/cfg/conf config files for each augmentation run

**This directory can only be changed on a configuration branch**

Any ***configuration files*** should be placed here and need to follow the set of rules defined here.
A template configuration file with all configutations possible is present in [TEMPLATE](template.ini).

Rules to follow on a configuration file:
 - 1. It's required to exist two configuration categories [IO] and [GENERATOR] even if one is not changed
 - 2. All configurations of a category need to stay in that category. Do not switch them up.
 - 3. Any configuration to leave as default should not be written
 - 4. Any commentaries about a configuration need to be written atop the specific configuration