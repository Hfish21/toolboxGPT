import os
import openai
from pprint import pprint
openai.api_key = "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"


# Takes in a message log and has the agent take a step, returns the message log containing the fix
def take_step(message_log, request):

    message_log.append({
                "role": "user", 
                "content": request
            })
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        messages=message_log,   # The conversation history up to this point, as a list of dictionaries
        max_tokens=1000,        # The maximum number of tokens (words or subwords) in the generated response
        stop=None,              # The stopping sequence for the generated response, if any (not used here)
        temperature=0.1,        # The "creativity" of the generated response (higher temperature = more creative)
    )

    message_log.append({"role": "assistant", "content": response.choices[0].message.content})
    return message_log

input_data = {
    'firstname' : 'Hayden', 
    'lastname' : 'Salmon',
    'address' : "3227 Gardner Road, Lakeland Florida 33810"

}

output_data = {
    'firstName' : "Hayden", 
    'lastName' : "Salmon",
    'fullname' : "Hayden Salmon",
    'address' : {
        "street" : "3227 Gardner Road",
        "city" : "Lakeland",
        "state" : "Florida",
        "zip" : "33810"
    }
}

message_log = [
    {
        "role": "system", 
        "content": ''' 
            You are an AI which writes python scripts to extract transform and load input data into output data. 
            I will give you an example of input data and output data. 
            You will give me only the code written as a function called data_transform
        '''
    }
]

request = f'''
        Input = {str(input_data)}
        Ouput = {str(output_data)}
    '''


message_log = take_step(message_log, request)


# Run the exec code
correct = False
layers = 10
i = 0
while correct == False and  i < layers:
    print(f"<----- Running Layer {i} ----->")
    try: 
        # Run the suggested code
        code = message_log[-1]['content'].split("```")[1].replace("python", '')
        exec(code)
        new_output = data_transform(input_data)

        if new_output != output_data:
            request = f'''
                The script you wrote for me did not give the correct output, 
                please re-write the script so it has the following output:
                {output_data}
            '''
            message_log = take_step(message_log, request)
            print("OUTPUT INCORRECT")
            i += 1 
        else:
            correct = True
            print("CORRECT!!!")
            i += 1 

    except Exception as e:
        request = f'''
            The script you wrote for me gave me an error when I ran it, the error it gave is:
            {str(e)}
            re-write the script with the error fixed
        '''
        message_log = take_step(message_log, request)
        print("EXECUTION ERROR")
        i += 1 
