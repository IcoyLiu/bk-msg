import uvicorn

from core.bootstrap import BootStrap
from core.settings import settings
from server.apps.example.url import test_api

bootstrap = BootStrap(
    app_name="Weops-Extension-Api",
    app_version="0.1.0",
    routers=[test_api],
)
bootstrap.boot()

if __name__ == "__main__":
    if settings.env == "dev":
        uvicorn.run(
            app="main:bootstrap.application", host=settings.app_host, port=settings.app_port, reload=True, debug=True
        )
    else:
        uvicorn.run(
            app="main:bootstrap.application",
            host=settings.app_host,
            port=settings.app_port,
            reload=False,
            debug=False,
            log_level="info",
        )
