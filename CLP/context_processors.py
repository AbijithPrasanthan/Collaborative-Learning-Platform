def add_admin_rights(request):
    admin = False
    if request.user.is_active and request.user.is_superuser:
        admin = True
    return {'isadmin': admin}
