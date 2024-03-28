from assistant import listen_wake_word, listen, send_query

if __name__ == '__main__':
    while True:
        if listen_wake_word():
            print(listen())

    # while True:
    #     response = send_query(input("Ask bard: "))
    #
    #     if response:
    #         # Print out the response as it is retrieved
    #         for chunk in response:
    #             print(chunk.text, end='')
    #
    #         print()
    #     else:
    #         print('An unexpected error has occurred. Please try again.')
