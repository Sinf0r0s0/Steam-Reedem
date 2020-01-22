# Steam-Reedem 0.1


Automates the Steam key redeem process.
             
This code was entirely based on the Steam module: https://github.com/ValvePython/steam
and this snipet by Liam: https://gist.github.com/snipplets/2156576c2754f8a4c9b43ccb674d5a5d
thanks!

how to use:

To make the login process easier you should **turn off SteamGuard**:
1. In the browser go to: https://store.steampowered.com/account/
2. In the account security item click on 'Manage Steam Guard'
3. Select 'Disable Steam Guard'         

**Important Consideration**:
* This program saves session cookies in the 'cookie.session' file. Therefore:
**NEVER SHARE THIS FILE WITH ANYONE!** at the risk of losing your account.
                   


**requiriments**:

* requests
* Pycryptodome

**Installation:**

    pip install git+git://github.com/Sinf0r0s0/Steam-Reedem.git
    or
    pip install --upgrade https://github.com/Sinf0r0s0/Steam-Reedem/tarball/master


**exemple**:

    from steamreedem import Steamreedem

    user_name = 'myusername'
    password = 'mypassword'
    key = 'X6NIK-65Z2E-AWV5X'

    sr = Steamreedem(user_name, password)

    #  In the first run, cookies are saved in 'cookies.session' file.
    sr.reedem(key)
