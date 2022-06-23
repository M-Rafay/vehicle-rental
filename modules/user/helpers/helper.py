def get_headers(headers):
    # Returns header medium and portal if not found in headers
    default_value = 'Not Found'
    if 'HTTP_MEDIUM' in headers: header_medium = headers['HTTP_MEDIUM']
    else: header_medium = default_value
    if 'HTTP_PORTAL' in headers: header_portal = headers['HTTP_PORTAL']
    else: header_portal = default_value
    return header_medium, header_portal