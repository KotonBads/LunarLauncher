# LunarLauncher

Launcher for Lunar Client written in Python. Currently only works on Linux and is CLI only (atm).

# Installation

Clone this repository
```bash
git clone https://github.com/KotonBads/LunarLauncher.git
```

Install all requirements
```bash
pip install -r requirements.txt
```

Run `main.py`
```bash
chmod +x main.py
# or
python3 main.py
```

# Usage

Enter any path, you can't use `~` for `$HOME`, it has to be the full path you want to download Lunar's files onto.
![Lunar Files](https://i.imgur.com/CuQsY3C.png)

You can use any JVM for this, you still need to enter the full path here.
By default, it's going to try to use `.lunarclient/jre/zulu17*/bin/java` unless you specify a different executable
![Java Executable](https://i.imgur.com/4wDvslt.png)

It should look something like this when you're done. I personally use graal-vm since it gives me the most performance
![](https://i.imgur.com/ndXM7R3.png)

After all of that, it should download Lunar's files (if it isn't already there or isn't up to date)

# Contributing

I don't really have any guidelines, just have clear commit messages and open a PR.