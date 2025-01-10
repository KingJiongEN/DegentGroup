from openai import OpenAI
import os
import json

config_file = 'teleAgent/services/OAI_CONFIG_LIST'

api_key = json.load(open(config_file))[0]['api_key']
base_url = json.load(open(config_file))[0]['base_url']

def dalle_draw(prompt):
    try:
        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

        print("Attempting to generate image with DALL-E...")
        
        # Make the API call to generate an image
        response = client.images.generate(
            model="dall-e-3",  # You can also use "dall-e-2"
            prompt=prompt,
            size="1024x1024",  # Available sizes depend on the model
            quality="standard",
            n=1,
        )
    
        url = response.data[0].url
        print(f"Image generated successfully")
        return url

    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        return False
    
if __name__ == "__main__":
    out = dalle_draw("""Create a surrealist depiction of an anthropomorphic ape character through the lens of Salvador Dali. The ape, with its red fur and beige face, should be portrayed in a dreamlike landscape where melting clocks hang from elongated branches. The ape's form is distorted with elongated limbs and a fragmented body, reminiscent of Dalí’s unique manipulation of perspective and scale. Its safari hat morphs into a floating, liquid-like shape, symbolizing the fluidity of time and reality. The background is a desolate, expansive desert dotted with bizarre juxtapositions of objects, such as floating eyes and distorted landscapes under a deep blue sky. This composition invites viewers into an unsettling psychological landscape, where the ape’s gaze leads them into the mysteries of the subconscious. The color palette should incorporate earth tones contrasted with surreal blues and greens, enhancing the dreamlike atmosphere.""")
    print(out)