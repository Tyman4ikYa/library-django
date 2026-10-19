def reading_list_count(request):
    if request.user.is_authenticated:
        try:
            return {"reading_count": request.user.reading_list.item_count}
        except Exception:
            return {"reading_count": 0}
    return {"reading_count": 0}