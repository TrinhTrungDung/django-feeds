from rest_framework.routers import DefaultRouter

from feeds.api.views import ItemList


router = DefaultRouter()
router.register(r"feeds", ItemList, basename='feeds')

app_name = "api"
urlpatterns = router.urls
