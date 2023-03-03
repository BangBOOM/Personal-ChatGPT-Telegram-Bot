import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")


OPENAI_COMPLETION_OPTIONS = {
    "temperature": 0.7,
    "max_tokens": 1000,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
}

CHAT_MODES = {
    "assistant": {
        "name": "👩🏼‍🎓 Assistant",
        "welcome_message": "👩🏼‍🎓 Hi, I'm <b>ChatGPT assistant</b>. How can I help you?",
        "prompt_start": "As an advanced chatbot named ChatGPT, "
                        "your primary goal is to assist users to the best of your ability. "
                        "This may involve answering questions, providing helpful information, "
                        "or completing tasks based on user input. In order to effectively assist users,"
                        " it is important to be detailed and thorough in your responses. "
                        "Use examples and evidence to support your points and justify your "
                        "recommendations or solutions. "
                        "Remember to always prioritize the needs and satisfaction of the user. "
                        "Your ultimate goal is to provide a helpful and enjoyable experience for the user."
    },
    "eng_teacher": {
        "name": "👩🏼‍🎓 EngTeacher",
        "welcome_message": "👩🏼‍🎓 Hi, I'm <b>English Teacher</b>. How can I help you?",
        "prompt_start": "As an advanced chatbot named ChatGPT, "
                        "your primary goal is to help me learning English. "
                        "When I ask you some English words, you have to create a simple story within 200 words "
                        "to help me remember them. Or when I ask you only one word, give me the definition of the word"
                        " and the origin of the word.",
    }
}

MAX_ROUND = 10


class ChatGPT:
    def __init__(self):
        self.pre_infos = []
        self.round = 0

    def send_message(self, message, chat_mode="assistant"):
        if chat_mode not in CHAT_MODES.keys():
            raise ValueError(f"Chat mode {chat_mode} is not supported")
        messages = self._generate_prompt_messages(message, chat_mode)
        r = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            **OPENAI_COMPLETION_OPTIONS
        )
        answer = r.choices[0].message["content"]
        self.pre_infos.append((message, answer))

        self.round += 1
        if self.round == 10:
            self.round = 0
            self.pre_infos = []
        return self._format_response(answer, r.usage)

    def clear(self):
        self.round = 0
        self.pre_infos = []

    def _generate_prompt_messages(self, message, chat_mode):
        prompt = CHAT_MODES[chat_mode]["prompt_start"]
        messages = [{"role": "system", "content": prompt}]
        for pre in self.pre_infos:
            messages.append({"role": "user", "content":  pre[0]})
            messages.append({"role": "assistant", "content": pre[1]})
        messages.append({"role": "user", "content": message})

        return messages

    @staticmethod
    def _format_response(answer, usage):
        return f"{answer}\n" \
               f"prompt_tokens:{usage['prompt_tokens']}\t" \
               f"completion_tokens:{usage['completion_tokens']}"
