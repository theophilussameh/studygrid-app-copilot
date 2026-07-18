from agent import run_agent

def main():
    while True:
        question = input("You: ")

        if question.lower() == "exit":
            break

        answer = run_agent(question)

        print("\nGridMind:", answer)

if __name__ == "__main__":
    main()
