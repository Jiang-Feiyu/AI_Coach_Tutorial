import os
import openai
from dotenv import load_dotenv

def get_llm_response(prompt, system_message="You are a helpful assistant"):
    """
    获取LLM模型响应的函数
    
    Args:
        prompt (str): user input
        system_message (str): system prompt, default is "You are a helpful assistant"
    
    Returns:
        str: output of LLM
    """
    load_dotenv()
    api_key = os.environ.get("SAMBANOVA_API_KEY")
    
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.sambanova.ai/v1",
    )
    
    response = client.chat.completions.create(
        model="Meta-Llama-3.1-70B-Instruct",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        top_p=0.1
    )
    
    return response.choices[0].message.content

def main():
    # 示例调用
    prompt = "Hello"
    response = get_llm_response(prompt)
    print(response)

if __name__ == "__main__":
    main()