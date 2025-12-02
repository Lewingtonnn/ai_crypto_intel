from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from app.config_loader import load_config
from typing import List, Dict
import torch
from ut1ls.logger import setup_logging

logger = setup_logging()


class LLMEngine:
    def __init__(self):
        self.cfg = load_config()
        self.repo_id = self.cfg.llm["model_id"]
        self.chain = None  # Start as None
        self.pipeline = None

    def _load_model(self):
        """Lazy load the model only when needed."""
        if self.chain:
            return

        logger.info(f"⏳ Lazy Loading LLM: {self.repo_id}...")
        try:
            tokenizer = AutoTokenizer.from_pretrained(self.repo_id)
            model = AutoModelForSeq2SeqLM.from_pretrained(self.repo_id)

            pipe = pipeline(
                "text2text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=self.cfg.llm["max_new_tokens"],
                temperature=self.cfg.llm["temperature"],
                model_kwargs={"torch_dtype": torch.bfloat16}
            )

            self.llm = HuggingFacePipeline(pipeline=pipe)

            template = """
            You are an expert Crypto Intelligence Analyst. Your goal is to answer questions based ONLY on the provided news context.

            Instructions:
            1. Use the context below to answer the question.
            2. If the answer is not in the context, say "I cannot answer this based on the available intelligence."
            3. Keep your answer concise, professional, and direct.
            4. Cite the specific article titles or dates if relevant.

            Context:
            {context}

            Question:
            {question}

            Analyst Answer:
            """

            self.prompt = PromptTemplate(
                template=template,
                input_variables=["context", "question"]
            )

            self.chain = self.prompt | self.llm
            logger.info("✅ Local LLM Engine loaded successfully.")

        except Exception as e:
            logger.error(f"❌ FATAL LOCAL LLM LOADING ERROR: {e}")
            raise

    def generate_answer(self, query: str, context_documents: List[Dict]) -> str:
        # Check if loaded, if not, load now
        if self.chain is None:
            self._load_model()

        context_text = "\n\n".join([doc['content'] for doc in context_documents])

        try:
            response = self.chain.invoke({"context": context_text, "question": query})
            return response.strip()
        except Exception as e:
            logger.error(f"❌ LLM Generation Error during inference: {e}")
            return "Error generating intelligence report."