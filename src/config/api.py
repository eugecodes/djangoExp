from ninja import NinjaAPI
from ninja.security import HttpBearer

from addresses.api.routers import router as addresses_router
from channels.api.routers import router as channels_router
from clients.api.routers import router as clients_router
from commissions.api.routers import router as commissions_router
from contacts.api.routers import router as contacts_router
from contracts.api.routers import router as contracts_router
from costs.api.routers import router as costs_router
from energy_costs.api.routers import router as energy_costs_router
from invoices.api.routers import router as invoices_router
from margins.api.routers import router as margins_router
from marketers.api.routers import router as marketers_router
from rate_types.api.routers import router as rate_types_router
from rates.api.routers import router as rates_router
from roles.api.routers import router as roles_router
from saving_studies.api.routers import router as saving_studies_router
from suggested_rates.api.routers import router as suggested_rates_router
from supply_points.api.routers import router as supply_points_router
from users.api.routers import router as users_router
from users.services.login import get_user_by_token


class GlobalAuth(HttpBearer):
    openapi_scheme: str = "token"

    def authenticate(self, request, token):
        user = get_user_by_token(token)
        request.user = user
        return token


api = NinjaAPI(auth=GlobalAuth())

api.add_router("/addresses/", addresses_router)
api.add_router("/users/", users_router)
api.add_router("/clients/", clients_router)
api.add_router("/channels/", channels_router)
api.add_router("/contracts/", contracts_router)
api.add_router("/roles/", roles_router)
api.add_router("/marketers/", marketers_router)
api.add_router("/rate_types/", rate_types_router)
api.add_router("/rates/", rates_router)
api.add_router("/margins/", margins_router)
api.add_router("/commissions/", commissions_router)
api.add_router("/studies/", saving_studies_router)
api.add_router("/supply_points/", supply_points_router)
api.add_router("/costs/", costs_router)
api.add_router("/contacts/", contacts_router)
api.add_router("/invoices/", invoices_router)
api.add_router("/suggested-rates/", suggested_rates_router)
api.add_router("/energy_costs/", energy_costs_router)
