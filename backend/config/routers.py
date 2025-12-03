from rest_framework.routers import DefaultRouter

from payouts.viewsets import PayoutViewSet

router: DefaultRouter = DefaultRouter()

router.register("payouts", PayoutViewSet, "payouts")
