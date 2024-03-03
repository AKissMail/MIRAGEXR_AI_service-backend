from .gpt_open_ai import gpt
from .llm_lama import lama
from rest_framework import serializers
from .models import Document


class ThinkRAGSerializer(serializers.Serializer):
    model = serializers.CharField()
    message = serializers.CharField()
    context = serializers.CharField()


def jaccard_index(prompt, corpus_document):
    # Check if corpus_document is None
    if corpus_document is None:
        return 0  # Return a default score of 0 or consider throwing an exception

    query = prompt.lower().split(" ")
    document = corpus_document.lower().split(" ")
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection) / len(union)


def get_best_document(validated_data):
    prompt = validated_data.get("message")
    best_document = ["Kein Dokument gefunden", 0]
    for document in Document.objects.all():
        current_score = jaccard_index(prompt, document.content)
        if best_document[1] < current_score:  # Compare scores correctly
            best_document = [document.content, current_score]
    best_jaccard = {
        'user_prompt': prompt,
        'best_jaccard_score': best_document[1],
        'best_document_text': best_document[0]
    }
    return best_jaccard


def norwegian_on_the_web(validated_data):
    best_document = get_best_document(validated_data)
    gpt_prompt = validated_data
    gpt_prompt['message'] = (
        "Using the user input provided as 'User Input', along with the surrounding 'User Context', your task is to "
        "generate a comprehensive response as a Norwegan Teacher. Leverages information from the 'document' field. "
        "This document contains details out of a Norwegan Textbook that relevant to the user's query, specifically "
        "found within a designated page and chapter. It's imperative to accurately incorporate these details into "
        "your response. Ensure that the information from the specified page and chapter is clearly referenced and "
        "seamlessly integrated into your answer. Aim to provide a well-rounded and informed response that directly "
        "addresses the user's initial query.\n\n"
        "User Message: {}\n\n"
        "User Context: {}\n\n"
        "Databases Document: {}\n\n"
        "Please incorporate the above details into your response, focusing on extracting and utilizing the most "
        "relevant information from the specified sections of the document to address the user's needs effectively."
        "Your answer must be in Norwegian or in Englisch depending on the User Message language."
    ).format(validated_data['message'], validated_data['context'], best_document['best_document_text'])
    gpt_prompt['context'] = (
        "In this task, you are required to synthesize information from multiple sources to provide a detailed "
        "and relevant response to the user's query. The user has provided specific input that outlines their "
        "question or need. Accompanying this is a contextual background that gives additional insight into the "
        "user's situation or the nature of their inquiry. Furthermore, you have access to a document containing "
        "key information pertinent to addressing the user's query. This document includes critical details located "
        "within a specified page and chapter, which are especially relevant to the user's request."
        "Your response should integrate the user's input, the contextual background, and the targeted information "
        "from the document. It is essential to accurately reference and incorporate the relevant details from the "
        "designated page and chapter of the document. This comprehensive approach will ensure that the generated "
        "response is not only well-informed and precise but also tailored to the user's specific context and query."
        "The goal is to utilize the synthesis of these elements to provide a clear, concise, and informative answer "
        "that directly addresses the user's needs."
    )
    gpt_prompt['model'] = 'gpt-3.5-turbo'
    result = gpt(gpt_prompt)
    print(result)
    return result


def rag_manager(data):
    serializer = ThinkRAGSerializer(data=data)
    if serializer.is_valid():
        if serializer.validated_data['model'] in 'norwegian-on-the-web':
            return norwegian_on_the_web(serializer.validated_data)
        else:
            return {"error": "RAG model not found"}
    else:
        return {"error": "Input data is invalid.", "details": serializer.errors}
