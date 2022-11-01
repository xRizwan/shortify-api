def form_valid_url(long: str):
    if "http" in long:
        return long
    else:
        return f"https://{long}"
