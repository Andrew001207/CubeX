def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''