from django.urls import path
from . import views, authviews

urlpatterns = [
    path("", views.index, name="index"),
    path("shows/", views.shows, name="shows"),
    path("login/", authviews.LoginAccountView.as_view(), name="login"),
    path("register/", authviews.CreateAccountView.as_view(), name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/account/edit", authviews.EDAccountView.as_view(), name="account"),
    path("dashboard/update-password/", authviews.CHPasswordView.as_view(), name="change-password"),
    path("reset-password/", authviews.PWDResetView.as_view(), name="reset-password"),
    path("delete-account/", authviews.DLAccountView.as_view(), name="delete-account"),
    path("logout/", authviews.log_out, name="logout"),

    path("dashboard/shows/", views.dashboard_shows, name="dashboard-shows"),
    path("overview/", views.overview, name="overview"),
    path("dashboard/episodes/", views.episodes, name="dashboard-episodes"),
    path("dashboard/account/", views.account, name="account"),

    path("dashboard/shows/<int:pk>/edit/", views.edit_show, name="edit-show"),
    path("dashboard/shows/create/", views.add_show, name="create-show"),
    path("dashboard/episodes/<int:pk>/edit/", views.edit_episode, name="edit-episode"),
    path("dashboard/episodes/create/", views.add_episode, name="create-episode"),

    path("dashboard/shows/<int:pk>/rss/", views.dashboard_rss, name="show-feed"),
    path("shows/<int:pk>/rss/", views.show_rss, name="show-feed"),
    
]