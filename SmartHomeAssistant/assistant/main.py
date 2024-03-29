from assistant import listen_wake_word, listen, speech_to_text, send_query


if __name__ == '__main__':
    while True:
        if listen_wake_word():
            audio = listen()

            if audio is not None:
                print("Processing speech to text")

                query = speech_to_text(audio)
                response = None

                if query is None:
                    # TODO: Respond with error message
                    print("Could not understand")
                else:
                    response = send_query(query)

                if response is not None:
                    for chunk in response:
                        print(chunk.text, end='')

                    print()
