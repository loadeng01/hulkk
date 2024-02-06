from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import SimpleRouter
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from apps.category.views import CategoryViewSet
from apps.room.views import RoomViewSet, UserFavoritesListView

schema_view = get_schema_view(
   openapi.Info(
      title="GREEN API",
      default_version='v1',
   ),
   public=True,
)

router = SimpleRouter()
router.register('category', CategoryViewSet)
router.register('room', RoomViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger')),
    path('api/account/', include('apps.account.urls')),
    path('api/', include(router.urls)),
    path('api/your_likes/', UserFavoritesListView.as_view())
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)

