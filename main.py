import aiohttp
import asyncio

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


# set our ascii art to be called whenever using print(ascii)


async def send(webhookurl, message):
    async with aiohttp.ClientSession() as session:
        payload = {"content": message}
        async with session.post(webhookurl, json=payload) as response:
            if response.status == 204:
                print("sent")
            else:
                print(f"failed: {response.status}")


# set up our sending function
async def delete(webhookurl):
    async with aiohttp.ClientSession() as session:
        async with session.delete(webhookurl) as response:
            if response.status == 204:
                print("deleted yay")
            else:
                print(f"uh oh: {response.status}")


# set up our deleting function

# this is our main function that has our menu
async def main():
    print(asciiart)
    webhookurl = input("webhook: ").strip()
    # set our webhook url

    while True:
        print("1. spam webhook")
        print("2. delete webhook")
        print("3. exit")
        choice = input("choose: ").strip()
        # display our menu and set our choice

        if choice == "1":
            # this is our first option, it asks for the message
            message = input("message: ").strip()

            pingeveryone = input("want to ping @everyone? y/n: ").strip().lower()
            # this asks if you want to ping everyone in the message
            if pingeveryone in ["yes", "y"]:
                message = "@everyone " + message
            # trys to send the message
            try:
                while True:
                    await send(webhookurl, message)

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
        elif choice == "3":
            # this is our third option in the menu, aka exit
            print("closing")
            break
        #   ^ this is closing the program if they selected 3
        else:
            print("that doesnt exist")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nended")
# this is running the whole thing
