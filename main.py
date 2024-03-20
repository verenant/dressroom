# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from Bot import bot_src
import replicate
import base64
import asyncio

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
#https://replicate.com/viktorfa/oot_diffusion_with_mask?prediction=2heuwstbcqosx7xtgo56s23lb4
    #https://huggingface.co/spaces/levihsu/OOTDiffusion


    with open("images/bad_model.jpg", 'rb') as file:
        data = base64.b64encode(file.read()).decode('utf-8')
        model_image = f"data:application/octet-stream;base64,{data}"
    with open("images/jacket.jpg", 'rb') as file:
        data = base64.b64encode(file.read()).decode('utf-8')
        garment_image = f"data:application/octet-stream;base64,{data}"
    input = {
        "seed": 99999,
        "model_image": model_image,
        "garment_image": garment_image,
        "garment-category": "Upper-body"
    }

    output = replicate.run(
        "viktorfa/oot_diffusion_with_mask:c890e02d8180bde7eeed1a138217ee154d8cdd8769a29f02bd51fea33d268385",
        input=input
    )
    print(output)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run( bot_src.start_bot() )
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
