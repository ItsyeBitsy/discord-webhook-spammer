import aiohttp
import asyncio
import os
import random
import time

# ^ import our library's

asciiart = """

$$\   $$\                                                                           $$\       $$\                           $$\                                                         
\__|  $$ |                                                                          $$ |      $$ |                          $$ |                                                        
$$\ $$$$$$\    $$$$$$$\ $$\   $$\  $$$$$$\   $$$$$$$\       $$\  $$\  $$\  $$$$$$\  $$$$$$$\  $$$$$$$\   $$$$$$\   $$$$$$\  $$ |  $$\        $$$$$$$\  $$$$$$\   $$$$$$\  $$$$$$\$$$$\  
$$ |\_$$  _|  $$  _____|$$ |  $$ |$$  __$$\ $$  _____|      $$ | $$ | $$ |$$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$ | $$  |      $$  _____|$$  __$$\  \____$$\ $$  _$$  _$$\ 
$$ |  $$ |    \$$$$$$\  $$ |  $$ |$$$$$$$$ |\$$$$$$\        $$ | $$ | $$ |$$$$$$$$ |$$ |  $$ |$$ |  $$ |$$ /  $$ |$$ /  $$ |$$$$$$  /       \$$$$$$\  $$ /  $$ | $$$$$$$ |$$ / $$ / $$ |
$$ |  $$ |$$\  \____$$\ $$ |  $$ |$$   ____| \____$$\       $$ | $$ | $$ |$$   ____|$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$  _$$<         \____$$\ $$ |  $$ |$$  __$$ |$$ | $$ | $$ |
$$ |  \$$$$  |$$$$$$$  |\$$$$$$$ |\$$$$$$$\ $$$$$$$  |      \$$$$$\$$$$  |\$$$$$$$\ $$$$$$$  |$$ |  $$ |\$$$$$$  |\$$$$$$  |$$ | \$$\       $$$$$$$  |$$$$$$$  |\$$$$$$$ |$$ | $$ | $$ |
\__|   \____/ \_______/  \____$$ | \_______|\_______/        \_____\____/  \_______|\_______/ \__|  \__| \______/  \______/ \__|  \__|      \_______/ $$  ____/  \_______|\__| \__| \__|
                        $$\   $$ |                                                                                                                    $$ |                              
                        \$$$$$$  |                                                                                                                    $$ |                              
                         \______/                                                                                                                     \__|                              

"""


# set our ascii art to be called whenever using print(asciiart)

async def send(webhookurl, message, proxies):
    proxy = random.choice(proxies) if proxies else None  # choose a random proxy if there are any
    connector = aiohttp.ClientSession(connector=proxy) if proxy else None  # use it if there is one
    async with aiohttp.ClientSession(connector=connector) as session:
        payload = {"content": message}  # Message we want to send
        async with session.post(webhookurl, json=payload) as response:  # send the message
            if response.status == 204:  # checks if it went through
                print("sent")
            else:  # if it failed
                print(f"failed: {response.status}")


async def delete(webhookurl):  # set up our deleting function
    async with aiohttp.ClientSession() as session:
        async with session.delete(webhookurl) as response:
            if response.status == 204:
                print("deleted yay")
            else:
                print(f"uh oh: {response.status}")


def loadproxies():  # this is our loadproxies function
    if os.path.exists("proxies.txt"):  # checks if proxies.txt exists
        with open("proxies.txt", "r") as file:  # opens it and reads the content
            return [line.strip() for line in file if line.strip()]  # puts it into format
    else:
        return []


def saveproxies(proxies):  # this is our saveproxies function
    with open("proxies.txt", "w") as file:  # makes the proxies.txt
        file.write("\n".join(proxies))  # writes the proxies inside it


async def main():  # this is our main function that has our menu
    print(asciiart)
    webhookurl = input("webhook: ").strip()  # set our webhook url
    proxies = loadproxies()  # load our proxies

    while True:
        print("1. spam webhook")
        print("2. delete webhook")
        print("3. load proxies")
        print("4. exit")
        choice = input("choose: ").strip()
        # display our menu and set our choice

        if choice == "1":  # this is our first option, it asks for the message
            message = input("message: ").strip()

            pingeveryone = input("want to ping @everyone? y/n: ").strip().lower()
            # this asks if you want to ping everyone in the message
            if pingeveryone in ["yes", "y"]:
                message = "@everyone " + message
            try:
                while True:
                    await send(webhookurl, message, proxies)  # trys to send the message

            except KeyboardInterrupt:
                print("\nstopped")

        elif choice == "2":
            # this is our second option, it asks if your sure you want to delete the webhook,
            # some people accidentally do this
            confirm = input("are you sure? y/n").strip().lower()
            if confirm in ["yes", "y"]:
                await delete(webhookurl)
                #   ^ this is deleting the webhook
                break
            #   ^ this is closing the program
        elif choice == "3":  # this is our third option in the menu, where you can save proxies
            print("paste proxies one per line")
            print("dont forget your http:// or https:// !!!")
            loggedproxies = []
            while True:
                proxy = input().strip()
                if not proxy:  # wait until enter is pressed
                    break
                loggedproxies.append(proxy)
            proxies.extend(loggedproxies)
            proxies = list(set(proxies))  # remove duplicate proxies from the list
            saveproxies(proxies)
            print("proxies saved")

        elif choice == "4":  # this is our fourth option in the menu, aka exit
            print("closing")
            break  # this is closing the program if they selected 3
        else:
            print("that doesnt exist")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nended")
# this is running the whole thing
