from langchain.prompts import PromptTemplate
from langchain.output_parsers.regex import RegexParser
from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

class Judge:
    def __init__(self, model_name, api_provider, temperature):
        self.model_name = model_name
        self.api_provider = api_provider
        self.model = self._initialize_model(model_name, api_provider, temperature)

        self.scoring_prompt = PromptTemplate(
            input_variables=["context", "argument"],
            template="""
            You are an AI judge evaluating the following response based on the criteria of relevance, coherence, and fact-checking. 
            Provide a score from 0 to 100 for the response considering the context.

            Context: {context}

            Response: {argument}

            Criteria:
            1. Relevance: How relevant is the response to the context and the current argument?
            2. Coherence: How logically structured and clear is the response?
            3. Fact-check: How accurate and reliable are the facts and information presented in the response?

            Only Provide a score (0-100) as ouput for the response based on the above criteria:
            """,
        )
        self.score_parser = RegexParser(regex=r"(\d+)", output_keys=["score"])
        self.chain = self.scoring_prompt | self.model | self.score_parser

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

    def return_score(self, argument, context):
        response = self.chain.invoke({"context": context, "argument": argument})
        score = response["score"]

        try:
            return int(score.strip())
        except ValueError:
            print(f"Can't calculate score as output is {response}")
            return 0