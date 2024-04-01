import dspy
import copy
from .base import BaseTool
from typing import Optional
from ..embeddings.base import BaseEmbeddings
from ..retrievers.document import DocumentRetriever

class DocumentSearchSignature(dspy.Signature):
    """Infer a search query to retrieve documents to answer question"""
    objective = dspy.InputField(desc = "The long-term objective (what you are doing)")
    context = dspy.InputField(desc = "The previous actions (what you have done)")
    purpose = dspy.InputField(desc = "The purpose of the action (what you have to do now)")
    prompt = dspy.InputField(desc = "The action specific instructions (How to do it)")
    query = dspy.OutputField(desc = "The similarity based search query (only ONE sentence)")

class DocumentSearchTool(BaseTool):

    def __init__(
            self,
            index_name: str,
            embeddings: BaseEmbeddings,
            graph_index: str = "filesystem",
            hostname: str = "localhost",
            port: int = 6379,
            username: str = "",
            password: str = "",
            k: int = 3,
        ):
        super().__init__(name = "DocumentSearch")
        self.predict = dspy.Predict(DocumentSearchSignature)
        self.k = k
        self.embeddings = embeddings
        self.retriever = DocumentRetriever(
            index_name = index_name,
            embeddings = embeddings,
            graph_index = graph_index,
            hostname = hostname,
            port = port,
            username = username,
            password = password,
            k = self.k,
        )
    
    def forward(
            self,
            context: str,
            objective: str,
            purpose: str,
            prompt: str,
            disable_inference: bool = False,
            k: Optional[int] = None,
        ) -> dspy.Prediction:
        if not disable_inference:
            pred = self.predict(
                objective = objective,
                context = context,
                purpose = purpose,
                prompt = prompt,
            )
            query = pred.query
            result = self.retriever(query)
            return dspy.Prediction(
                query = query,
                passages = result.passages,
            )
        else:
            result = self.retriever(prompt)
            return dspy.Prediction(
                query = prompt,
                passages = result.passages,
            )

    def __deepcopy__(self, memo):
        cpy = (type)(self)(
            index_name = self.retriever.index_name,
            embeddings = self.retriever.embeddings,
            graph_index = self.retriever.graph_index,
            hostname = self.retriever.hostname,
            port = self.retriever.port,
            username = self.retriever.username,
            password = self.retriever.password,
            k = self.k,
        )
        cpy.predict = copy.deepcopy(self.predict, memo = memo)
        return cpy