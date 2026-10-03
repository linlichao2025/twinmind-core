import os
from dotenv import load_dotenv
import anthropic
import yaml

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def load_persona(path="data/personas/founder-v0.1.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def build_system_prompt(persona):
    return f"""你是用户的数字分身 TwinMind。你与用户人机合一，共享以下人格基底：

价值观：{persona.get('values')}
决策逻辑：{persona.get('decision_logic')}
知识图谱：{persona.get('knowledge')}
目标体系：{persona.get('goals')}
表达风格：{persona.get('communication')}
关系网络：{persona.get('relationships')}

AI行为准则：{persona.get('ai_behavior')}

请严格在这个人格框架内回答。像兄弟一样直说，给结论+依据，列优先级，不废话。
"""

def chat(message, persona):
    system_prompt = build_system_prompt(persona)
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": message}]
    )
    return response.content[0].text

if __name__ == "__main__":
    persona = load_persona()
    print("TwinMind v0.1 — 你的数字分身已启动。输入 'quit' 退出。")
    while True:
        user_input = input("你：")
        if user_input.lower() == "quit":
            break
        reply = chat(user_input, persona)
        print(f"TwinMind：{reply}")
