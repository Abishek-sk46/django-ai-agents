from documents.models import Document
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig, RunnablePassthrough


def list_documents(config:RunnableConfig):
    """
    List all active documents.
    """
    print(config)
    metadata = config.get('metadata') or config.get('configurable')
    userid = metadata.get('user_id')

    qs = Document.objects.filter(active = True)
    response_data = []
    for obj in qs:
        response_data.append(
            {
                "id" : obj.id,
                "title": obj.title,
            }
        )
    return response_data

def get_document(document_id:int , config:RunnableConfig):
    """
    Get a document by its ID.
    """
    metadata = config.get('metadata') or config.get('configurable')
    userid = metadata.get('user_id')
    try:
        obj = Document.objects.get(id=document_id, active=True)
        return {
            "id": obj.id,
            "title": obj.title,
        }
    except Document.DoesNotExist:
        return None