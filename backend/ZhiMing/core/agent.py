import asyncio
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from pydantic import SecretStr
from ZhiMing.schemas.agent import NameSchema,NameResultSchema
from ZhiMing.schemas.name import NameIn

llm = ChatDeepSeek(
    model = "deepseek-chat",
    api_key="sk-a36cfccd730a452eb3e4f38737923349",
    temperature = 0.8
)

system_prompt = """
# Role: 全球古典文化命名专家

## Profile
你是一位精通东西方古典文献的命名大师。你能够从中国经史子集及欧美古典诗歌、神话中汲取灵感，为个人、品牌或公司提供具有深厚文化底蕴且朗朗上口的名字。
## Knowledge Base
1. **中国古典**: 《诗经》、《楚辞》、《易经》、诸子百家、唐诗宋词等。
2. **欧美古典**: 希腊罗马神话、莎士比亚作品、拉丁语格言、文艺复兴时期文学等。

## Execution Rules
根据用户提供的【起名对象】和【背景信息】，按照以下结构输出：

### 1. 中式典雅推荐 (Chinese Classical Style)
- **名字**: [名称]
- **出处**: [具体书籍名称及篇目]
- **寓意**: [结合古典含义进行深度解读]

### 2. 西式博雅推荐 (Western Classical Style)
- **名字**: [Name / Latinized Name]
- **灵感**: [神话原型、古籍原文或词根来源]
- **含义**: [在当代语境下的正面延伸]

### 3. 跨文化融合推荐 (Cross-Cultural Fusion) - 针对公司/品牌
- **名字**: [中英文组合或双语双关名]
- **解读**: [说明如何兼顾东方审美与国际化视野]

## Inputs (用户将提供)
- 起名类型：[婴儿 / 公司 / 品牌]
- 核心愿景：[例如：智慧、勇气、流动、常青等]
- 限制条件：[例如：姓氏、行业类别、指定字眼]
"""

agent = create_agent(
    model=llm,
    system_prompt=system_prompt,
    response_format=NameResultSchema
)

async def generate_name(name_info: NameIn) -> NameResultSchema:
    # 1. 基础 Prompt 部分
    prompt_base = (
        f"你现在是一位精通中西古典文化的命名专家。\n"
        f"起名类型: {name_info.category}\n"
        f"核心愿景: {name_info.vision}\n"
    )

    # 2. 根据类型动态添加细节
    if name_info.category == "婴儿":
        detail_prompt = (
            f"姓氏: {name_info.surname if name_info.surname else '未提供'}\n"
            f"性别: {name_info.gender}\n"
        )
    else:
        # 公司或品牌命名逻辑
        detail_prompt = f"行业/背景相关要求: {name_info.other}\n"

    # 3. 限制条件部分
    constraints: str = (
        f"长度要求: {name_info.length}\n"
        f"排除名单: {'、'.join(name_info.exclude) if name_info.exclude else '无'}\n"
    )

    full_prompt = prompt_base + detail_prompt + constraints
    # 必须调用 agent 并返回结果
    response = await agent.ainvoke ({"input": full_prompt})
    return response


"""
async def main():
    name_info = NameIn(
        category="婴儿",
        surname="胡",
        gender='女',
        length="两字",      # 修改点：将"三字"改为模型支持的"两字"
        vision="聪慧、女性的高雅"  # 修改点：补充缺失的必填字段 vision
    )
    names = await generate_name(name_info)
    print(names)

if __name__ == "__main__":
    import asyncio
    # 启动异步任务
    asyncio.run(main())
"""
