from typing import Dict, Optional

from django.http import HttpRequest

from apps.site_setup.models import Setup


def setup_context_processor(request: HttpRequest) -> Dict[str, Optional[Setup]]:
    try:
        setup = Setup.objects.first()
    except Exception:
        setup = None
    return {'site_setup': setup}
