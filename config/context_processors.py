from datetime import datetime


def year_processor(request):
    return {'year': datetime.now().year}
