import pytest
from unittest.mock import patch, MagicMock
from app.services.llm import get_english_translation, get_rag_prompt

def test_get_english_translation():
    # Because LangChain constructs pipelines using `|` operator, mocking the inner elements 
    # without triggering internal validation checks is notoriously difficult.
    # The best practice for Unit Testing RAG/LangChain functions is to patch the outermost method
    # when testing services that consume it, or patch the runnable's `invoke` if testing the function itself.
    
    with patch("app.services.llm.translation_prompt") as mock_prompt, \
         patch("app.services.llm.llm") as mock_llm, \
         patch("app.services.llm.StrOutputParser") as mock_parser:
         
        # Create a mock chain
        mock_chain = MagicMock()
        mock_chain.invoke.return_value = "Translated Text"
        
        # When `translation_prompt | llm | StrOutputParser()` is executed, 
        # let's just mock the whole pipe return by patching the first object's __or__
        mock_prompt.__or__.return_value.__or__.return_value = mock_chain
        
        result = get_english_translation("안녕하세요")
        
        assert result == "Translated Text"
        mock_chain.invoke.assert_called_once_with({"query": "안녕하세요"})

def test_get_rag_prompt():
    prompt = get_rag_prompt()
    
    # Ensure it's a PromptTemplate
    from langchain_core.prompts import PromptTemplate
    assert isinstance(prompt, PromptTemplate)
    
    # Ensure it has the correct input variables
    assert "context" in prompt.input_variables
    assert "query" in prompt.input_variables

from app.services.llm import get_response_stream

def test_get_response_stream():
    # Test RAG prompt generator with LLM streaming correctly
    with patch("app.services.llm.get_rag_prompt") as mock_prompt, \
         patch("app.services.llm.llm") as mock_llm, \
         patch("app.services.llm.StrOutputParser") as mock_parser:
         
        mock_chain = MagicMock()
        # the stream method returns a generator
        mock_chain.stream.return_value = (chunk for chunk in ["안녕하세요", " ", "철학자", "입니다."])
        
        # Patch the pipe operator to return our mock chain
        mock_prompt.return_value.__or__.return_value.__or__.return_value = mock_chain
        
        stream_gen = get_response_stream(context="Philosophical quote here", query="Who am I?")
        
        results = list(stream_gen)
        assert results == ["안녕하세요", " ", "철학자", "입니다."]
        mock_chain.stream.assert_called_once_with({"context": "Philosophical quote here", "query": "Who am I?"})
