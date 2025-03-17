from fetch_llm import get_llm_response

def main():
    # 示例调用
    prompt = "Hello"
    response = get_llm_response(prompt)
    print(response)

if __name__ == "__main__":
    main()