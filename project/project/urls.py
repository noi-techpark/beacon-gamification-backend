from django.contrib import admin
from django.urls import path

from main.views import auth, beacons, quest_finder, quests, users

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/api-token-auth/',
         auth.CustomObtainAuthToken.as_view(), name='api_token_auth'),

    # auth
    path('api/v1/check-token/', auth.CheckTokenView.as_view(), name='check-token'),

    # user
    path('api/v1/users/<int:pk>/',
         users.UserDetailsView.as_view(), name='user-details'),
    path('api/v1/users/',
         users.UserListView.as_view(), name='user-list'),
    path('api/v1/users/add-points/',
         users.AddPoints.as_view(), name='user-add-points'),
    path('api/v1/users/modify-points/',
         users.AddPoints.as_view(), name='user-modify-points'),

    # beacons
    path('api/v1/beacons/<int:pk>/',
         beacons.BeaconsDetailsView.as_view(), name='beacons-details'),
    path('api/v1/beacons/', beacons.BeaconsView.as_view(), name='beacons'),

    # User registration
    path('api/v1/create-user/',
         users.UserCreateAPIView.as_view(), name='create-user'),
    path('api/v1/groups/<int:pkGroup>/add-user/<int:pkUser>/',
         users.AddUserToGroupView.as_view(), name='add-user-to-group'),

    # quests
    path('api/v1/quest/<int:pk>/',
         quests.QuestDetailsView.as_view(), name='quest-details'),
    path('api/v1/quest/', quests.QuestListView.as_view(), name='quest'),

    path('api/v1/quest-steps/<int:pk>/',
         quests.QuestStepDetailsView.as_view(), name='quest-step-details'),
    path('api/v1/quest-steps/',
         quests.QuestStepListView.as_view(), name='quest-step'),

    # Starting from a beacon id you will obtain every quest that use this beacon
    path('api/v1/quest-finder/',
         quest_finder.QuestFinderView.as_view(), name='quest-finder'),
]
