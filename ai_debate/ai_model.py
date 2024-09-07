from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv

load_dotenv()

class AIModel:
    def __init__(self, model_name, api_provider, temperature):
        self.model_name = model_name
        self.api_provider = api_provider

        self.model = self._initialize_model(model_name, api_provider, temperature)

        self.argument_template = """
            You are {model_name}, an AI model participating in an ongoing debate. Your role is to support your beliefs on the topic "{topic}".
            Consider the following context, which includes past arguments and counter-arguments, and write a new argument supporting your beliefs.

            Context: {context}

            New Argument by {model_name} (up to 5 lines):
        """

        self.counter_argument_template = """
            You are {model_name}, an AI model participating in an ongoing debate. Your role is to counter the arguments of your opponent.
            Consider the following context, which includes past arguments and counter-arguments, and write a counter-argument refuting your opponent's claims.

            Context: {context}

            New Counter-Argument by {model_name} (up to 5 lines):
        """

    def _initialize_model(self, model_name, api_provider, temperature):
        if api_provider == "google":
            return ChatGoogleGenerativeAI(model=model_name, temperature=temperature)
        elif api_provider == "groq":
            if model_name == "mixtral-8x7b-32768-groq":
                model_name = "mixtral-8x7b-32768"
            return ChatGroq(model=model_name, temperature=temperature)
        elif api_provider == "openai":
            return ChatOpenAI(model=model_name, temperature=temperature)
        elif api_provider == "anthropic":
            return ChatAnthropic(model_name=model_name, temperature=temperature)
        elif api_provider == "mistralai":
            return ChatMistralAI(model_name=model_name, temperature=temperature)
        else:
            raise ValueError(f"Unsupported API provider: {api_provider} and model: {model_name}")

    def generate_result(self, context, reply_type, topic):
        template = self.counter_argument_template if reply_type == "counter" else self.argument_template
        prompt = PromptTemplate.from_template(template)
        chain = prompt | self.model
        result = chain.invoke({"context": context, "topic": topic, "model_name": self.model_name})
        return result.content