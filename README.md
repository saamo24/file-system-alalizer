# file-system-analizer
This is a command-line tool that analyzes and reports on the file system structure and usage on a Linux system.

## First Step
Clone the repository
- Open the Terminal and paste the following command
```
git clone https://github.com/saamo24/file-system-analizer.git
```
## Second step
Create the alias for the script.
- In your terminal open `.zshrc` OR `.bashrc` files using this command
```
vim .zshrc
```
OR
```
vim .bashrc
```
- In the openend Document create the alias (just copy and paste the following)
```
alias analize="python3 ~/file-system-analizer/analizer.py"
```
- Save and Quit
- Reopen the Terminal
- Use the following command
```
analize Desktop/
```

Example of usage:
![Preview](readme_gif/file-analizer.gif)


## Enjoy!
