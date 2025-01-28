import json
import os
from openai import OpenAI

def load_api_providers():
    providers = []
    api_providers_dir = "api-providers"  # 指定文件夹名称
    for file_name in os.listdir(api_providers_dir):
        if file_name.endswith(".json") and file_name != "api_providers.json":
            file_path = os.path.join(api_providers_dir, file_name)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    provider = json.load(f)
                    providers.append(provider)
            except json.JSONDecodeError as e:
                print(f"解析 JSON 文件 {file_name} 时出错：{e}")
            except Exception as e:
                print(f"读取文件 {file_name} 时出错：{e}")
    return providers

def get_ai_response(provider, model, prompt, user_message):
    try:
        client = OpenAI(
            api_key=provider["api_key"],
            base_url=provider["base_url"]
        )
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ],
            top_p=0.7,
            temperature=0.9
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"网络错误，请检查您的 API 地址和密钥。错误信息：{e}"