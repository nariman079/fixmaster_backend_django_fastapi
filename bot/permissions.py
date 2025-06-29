def api_key_permission(request) -> bool:
    api_key = request.headers.get("Api-Key")
    if api_key and api_key == "test":
        return True
    else:
        return False
