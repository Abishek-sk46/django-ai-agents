from django.db.models import Q
from documents.models import Document
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig




@tool
def search_query_documents(query: str ,limit:int=5, config: RunnableConfig= {}):
    """
    Search the most recent 5 documents for the current user

    arguments:
    query: string  or lookup search across title or content of document
    limit: number of resultk   
    """

    if limit>25:
        limit = 25
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')

    default_lookups = {
        "owner_id": user_id,
        "active":True,

    }

    qs = Document.objects.filter(**default_lookups).filter(
        Q(title__icontains=query) | 
        Q(content__icontains = query)
    )
    response_data = [
        {"id": obj.id, "title": obj.title}
        for obj in qs[:limit]
    ]
    return response_data

@tool
def list_documents(limit: int = 5, config: RunnableConfig = {}):
    """
    List the most recent active documents for the current user.
    Use this tool whenever the user asks what documents they have,
    requests to see available files, or asks for document titles.

    Arguments:
    - limit: maximum number of documents to return (default 5)
    """
    # Safety cap so LLM can't request too many
    if limit > 25:
        limit = 25

    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')

    if not user_id:
        raise Exception("Invalid request: user_id not provided.")

    qs = Document.objects.filter(
        active=True,
        owner_id=user_id
    ).order_by("-created_at")[:limit]

    if not qs.exists():
        return {"message": "No active documents found for this user."}

    # Format in a way that LLM can present easily
    titles = [obj.title for obj in qs]
    return {
        "count": len(titles),
        "titles": titles
    }

@tool
def get_document(document_id: int, config: RunnableConfig):
    """
    Get a document by its ID for the current user.
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')

    if user_id is None:
        raise Exception("Invalid request for user")

    try:
        obj = Document.objects.get(id=document_id, owner_id=user_id, active=True)
    except Document.DoesNotExist:
        raise Exception("Document not found, try again")
    except Exception:
        raise Exception("Invalid request for document detail, try again")

    return {
        "id": obj.id,
        "title": obj.title,
        "content": obj.content,
        "created_at": obj.created_at
    }


@tool
def create_document(title: str, content: str, config: RunnableConfig):
    """
    Create a new document to store for the user.

    Arguments:
    - title: string, max 120 characters
    - content: long form text
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')

    if user_id is None:
        raise Exception("Invalid request for user")

    obj = Document.objects.create(
        title=title,
        content=content,
        owner_id=user_id,
        active=True
    )

    return {
        "id": obj.id,
        "title": obj.title,
        "content": obj.content,
        "created_at": obj.created_at
    }


@tool
def delete_document(document_id: int, config: RunnableConfig):
    """
    Delete the details of a document for the current user.
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')

    if user_id is None:
        raise Exception("Invalid request for user")

    try:
        obj = Document.objects.get(id=document_id, owner_id=user_id, active=True)
    except Document.DoesNotExist:
        raise Exception("Document not found, try again")
    except Exception:
        raise Exception("Invalid request for document detail, try again")

    obj.delete()
    return {
        "message": "Successfully deleted",
    }


@tool
def update_document(document_id: int, title: str = None, content: str = None, config: RunnableConfig = {}):
    """
    Update an existing document for the current user.
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')

    if user_id is None:
        raise Exception("Invalid request for user")

    try:
        obj = Document.objects.get(id=document_id, owner_id=user_id, active=True)
    except Document.DoesNotExist:
        raise Exception("Document not found, try again")
    except Exception:
        raise Exception("Invalid request for document detail, try again")

    if title is not None:
        obj.title = title
    if content is not None:
        obj.content = content

    if title or content:
        obj.save()

    return {
        "id": obj.id,
        "title": obj.title,
        "content": obj.content,
        "created_at": obj.created_at
    }




# Register tools for LangChain agent
documents_tools = [
    search_query_documents,
    list_documents,
    get_document,
    create_document,
    update_document,
    delete_document
]
