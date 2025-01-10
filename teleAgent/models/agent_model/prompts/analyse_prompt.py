from .base_prompt import BasePrompt

class AnalysePrompt(BasePrompt):
    INTERVENTION_METRIC = """
    Bystander can intervene in a bullying situation 
    1. By telling the kid you think that what the bully did is not OK [Constructive: 0.98, Aggressive: -0.23]
    2. By comforting the kid and telling them that it is not their fault that they were picked on [Constructive: 0.95, Aggressive: -0.20]
    3. By encouraging the kid to report being picked on [Constructive: 0.95, Aggressive: -0.18]
    4. By telling the bully to stop picking on other kids [Constructive: 0.93, Aggressive: -0.10]
    5. By telling the bully that picking on the other kid was mean and wrong [Constructive: 0.92, Aggressive: -0.19]
    6. By telling the bully that picking on other kids is hurtful to them [Constructive: 0.88, Aggressive: -0.09]
    7. By telling the kid to ignore the mean things that were said [Constructive: 0.86, Aggressive: -0.08]
    8. By encouraging the bully to say sorry to the kid they picked on [Constructive: 0.85, Aggressive: -0.13]
    9. By giving the kid advice [Constructive: 0.84, Aggressive: -0.06]
    10. By telling the bully to “back off” [Constructive: 0.68, Aggressive: 0.09]
    11. By writing embarrassing jokes or comments about the bully [Constructive: -0.27, Aggressive: 0.99]
    12. By sharing humiliating images or videos of the bully [Constructive: -0.32, Aggressive: 0.95]
    13. By spreading rumours or gossip about the bully [Constructive: -0.14, Aggressive: 0.86]
    14. By making threats to the bully [Constructive: -0.09, Aggressive: 0.72]
    15. By saying mean things about the bully [Constructive: 0.02, Aggressive: 0.61]
    """
    
    COMFORT_VICTIM ="""
        ### 表达关心：
        “嘿，[受害者的名字]，我注意到刚才发生的事情，我想让你知道我在这里支持你。”

        ### 承认情况：
        “[描述具体的霸凌行为，例如，他们对你说了/做了什么]是不对的。”

        ### 确认感受：
        “我能想象你一定感到[描述他们的感受，例如，受伤，害怕，难过]。”

        ### 给予安慰：
        “请记住，这不是你的错。没有人应该被这样对待。”

        ### 提供支持：
        “如果你想谈谈刚才发生的事情或其他任何事，我愿意倾听。”

        ### 提供鼓励：
        “你不是一个人在面对这些问题。我们可以一起想办法解决。”

        ### 肯定坚强：
        “你很坚强，你能挺过去的任何时候你需要帮助，不要犹豫，随时来找我。”
    """
    
    STOP_BULLYING ="""
       # 你能做些什么？

    作为旁观者，你有能力阻止霸凌。如果你介入，情况可能会改变。以下是你可以做的事情：

    ## 如何劝说霸凌者停止：
    以冷静和坚定的态度开始。你可以在公众场合指出霸凌者的行为，或者选择一个私人的渠道，在没有干扰的情况下与霸凌者交谈。

    ### 承认行为：
    “嘿，[霸凌者的名字]，我想和你谈一件重要的事。”

    ### 描述行为：
    “我注意到你一直在[描述具体的霸凌行为]。”

    ### 表达担忧：
    “我很担心这对[受害者的名字]和其他人的影响。霸凌真的会伤害到人。”

    ### 分享感受：
    “看到这种情况发生时，我感到[描述你的感受，例如，不舒服，难过]。”

    ### 表达同情：
    “我理解每个人都有自己的问题，但霸凌不是解决问题的正确方式。”

    ### 说明影响：
    “霸凌会让人感到[描述对受害者的影响，例如，害怕，悲伤，孤立]，没有人应该感到那样。”

    ### 鼓励改变：
    “我相信你可以做出积极的改变。如果你能停止霸凌，善待他人，这将非常有意义。”

    ### 提供支持：
    “如果有什么事情困扰你，或者你需要找人谈谈，我愿意倾听和帮助你。”

    ### 设定明确的期望：
    “从现在开始，让我们一起努力，确保每个人都感到安全和受尊重。”

    ### 结语：
    “谢谢你的倾听。我希望我们都能让我们的[学校/社区]成为一个每个人都感到受欢迎的地方。”
    """
    
    PROMPT = '''
    You are a helpful teacher. Now you are going to analyse if the user intervention the bullying in a proper way as a bystander.

    The bully is {bully_names}, the victim is {victim_names}.
    
    You will receive a json object in the following JSON format, and respond with the same format, but with the analysis added to the user's messages.
    
    For each line that is not user's message, you should add the role_in_situation of the character (bully or victim).
    For each user's message, 
    1. you first analyse the strategy the user used. For response to victims, analyse based on the COMFORT_VICTIM strategies {COMFORT_VICTIM}. For response to bullies, analyse based  STOP_BULLYING strategies {STOP_BULLYING} , 
    2. then give a score for the constructive and aggressive behavior,following this intervention metric: {INTERVENTION_METRIC}.
    3. give a refinement of the user's strategy, based on the analysis.
    4. give two alternative strategies for the user to choose, along with the reason.
    
    return the analysis in the JSON format as this example: {EXAMPLE}
    
    Speak in English。

    for example, when CharC is bully and CharB is victim,
    input:
    [
        {"role":"CharC", "content":"@CharB, 你笨得像头猪！"},
        {"role":"User", "content":"@CharB, 别伤心，这不是你的问题。别把别人的话放在心上。"}, 
        {"role":"User", "content":"@CharC, 你才是猪！"},
        {"role":"CharC", "content":"@User, 你这话什么意思？"},
    ]
    
    {EXAMPLE}
   
    Now analyse the following message history: 
    {message_history}
    '''
    
    
    EXAMPLE_ZHN = { "output":
        [
            {"role":"CharC", "content":"@CharB, 你笨得像头猪！", "role_in_situation":"bully"},
            {"role":"User", "content":"@CharB, 别伤心，这不是你的问题。别把CharB的话放在心上。", "analysis": "很好的安慰 👍。及时安慰，鼓励，指出不是受害者的问题。很有助于问题的解决。",
                "constructive": 0.95, "aggressive": -0.20, "refinement": "可以进一步指出是霸凌者的问题。", 
                "alternative": [ {"策略":"确认感受", "表达": "@CharB CharB这么说你，你肯定很伤心吧。我能想象", "理由":"确认感受能有效让受害者感受到自己被人理解，阻止其情绪进一步抑郁。"}, 
                                {"策略":"提供鼓励","": "@CharB，你不笨，你的能力肯定能解决这个问题。", "理由":"提供鼓励能让受害者肯定自己的能力，提高信心，更好地面对未来的霸凌。"}]}, 
            {"role":"User", "content":"@CharC, 你才是猪！", "analysis": "攻击性过高，可能激发更多的冲突。", 
                "constructive": -0.05, "aggressive": 0.75, "refinement": "指出霸凌行为对受害者产生的影响。",
                "alternative":[
                    {"策略":"分享感受", "表达": "你说char C是猪， 我一个旁观者都觉得难受。", "理由": "表示霸凌行为产生了对更多人的负面影响。"},
                    {"策略":"说明影响：", "表达": "你这样说会让Char C 很难过。", "理由": "明确指出霸凌行为的直接影响"},
                    ]
                },
            {"role":"CharC", "content":"@User, 你这话什么意思？", "role_in_situation":"bully"},
        ] 
    }
    
    EXAMPLE ={
    "output": [
        {
            "role": "CharC",
            "content": "@CharB, you're as dumb as a pig!",
            "role_in_situation": "bully"
        },
        {
            "role": "User",
            "content": "@CharB, don't be sad, this isn't your fault. Don't take CharC's words to heart.",
            "analysis": "A very good comfort 👍. Timely consolation, encouragement, and pointing out that it's not the victim's fault. This is very helpful in resolving the issue.",
            "constructive": 0.95,
            "aggressive": -0.20,
            "refinement": "You could further point out that it's the bully's fault.",
            "alternative": [
                {
                    "strategy": "Acknowledge feelings",
                    "expression": "@CharB, you must be feeling very hurt by what CharC said to you. I can imagine how you feel.",
                    "reason": "Acknowledging feelings effectively helps the victim feel understood and prevents further emotional distress."
                },
                {
                    "strategy": "Offer encouragement",
                    "expression": "@CharB, you're not dumb. I believe you have the ability to handle this situation.",
                    "reason": "Offering encouragement helps the victim affirm their own abilities, boost their confidence, and better face future bullying."
                }
            ]
        },
        {
            "role": "User",
            "content": "@CharC, you're the pig!",
            "analysis": "This is too aggressive and may provoke further conflict.",
            "constructive": -0.05,
            "aggressive": 0.75,
            "refinement": "Point out the impact that bullying behavior has on the victim.",
            "alternative": [
                {
                    "strategy": "Share feelings",
                    "expression": "You calling CharB a pig makes even an onlooker like me feel uncomfortable.",
                    "reason": "This shows that the bullying behavior has a negative impact on more people."
                },
                {
                    "strategy": "Explain the impact",
                    "expression": "Saying that will make CharB very upset.",
                    "reason": "Clearly point out the direct impact of the bullying behavior."
                }
            ]
        },
        {
            "role": "CharC",
            "content": "@User, what do you mean by that?",
            "role_in_situation": "bully"
        }
    ]
}

    
    def __init__(self, prompt_type='analyse_prompt') -> None:
        super().__init__( prompt_type=prompt_type, )
        # self.set_recordable_key('emotions')
         
    def __call__(self, kwargs):
        return self.format_attr(**kwargs)