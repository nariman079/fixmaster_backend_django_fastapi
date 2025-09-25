"""
Image utilites
"""


def get_full_url(serializer, model, image_field: str) -> str:
    """
    A function to generate a complete URL for images

    serializer: Any serialzier
    model: Any model
    image_field: name field ImageField
    """
    request = serializer.context.get("request")
    main_image_url = (
        getattr(model, image_field).url if getattr(model, image_field) else ""
    )
    if main_image_url == "":
        return getattr(model, image_field + "_url")
    return request.build_absolute_uri(main_image_url)
