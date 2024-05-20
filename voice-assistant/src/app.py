from interface import AudioInterface
from agents import SimpleAIAssistant, AdvancedAIAssistant

# Create an instance of the AudioInterface and AIAssistant classes
interface = AudioInterface()
# assistant = SimpleAIAssistant()
assistant = AdvancedAIAssistant()


# To facilitate a conversation with the assistant, we will create a loop that listens to the user's input
while True:
    # Get the text from the user
    text = interface.listen()
    print(text)

    # If the user says 'exit' or 'quit', the loop will break and the chat will end
    if text.lower() == 'exit' or text.lower() == 'quit':
        break 

    # Pass the query from the user to the assistant and get the response
    response = assistant.run(text)
    print(response)

    # Play the agent response as audio
    print('Playing audio...')
    interface.speak(response)
    print('Done!')