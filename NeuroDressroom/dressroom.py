from Bot import bot_src
import replicate
import base64
import asyncio

def send_model(user_name:str)->str:
    # Use a breakpoint in the code line below to debug your script.
#https://replicate.com/viktorfa/oot_diffusion_with_mask?prediction=2heuwstbcqosx7xtgo56s23lb4
    #https://huggingface.co/spaces/levihsu/OOTDiffusion

    #Добавить в имя открываемого файла "images/"+user_name+"/1.jpg"
    #with open("images/bad_model.jpg", 'rb') as file: # для тестов нейросети
    with open("images/"+user_name+"/1.jpg", 'rb') as file:
        data = base64.b64encode(file.read()).decode('utf-8')
        model_image = f"data:application/octet-stream;base64,{data}"
    #with open("images/jacket.jpg", 'rb') as file: # для тестов нейросети
    with open("images/"+user_name+"/2.jpg", 'rb') as file:
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
    print("Dataset - OK")
    return output[0]

# Press the green button in the gutter to run the script.


#send_model()