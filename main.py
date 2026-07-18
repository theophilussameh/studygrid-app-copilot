from config import agent

def main():

    print("GridMind is ready!")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            break

        answer = agent.chat(question)

        print("\nGridMind:", answer)
        print()

if __name__ == "__main__":
    main()